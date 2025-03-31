from enum import Enum
from typing import Type

import pandas as pd
from pydantic import BaseModel
from sklearn.preprocessing import MultiLabelBinarizer


class PydanticOneHotEncoder:
    def __init__(self, model: Type[BaseModel]):
        self.model = model
        self.multi_label_fields, self.single_label_fields = self._get_enum_fields()
        self.mlb_encoders = {
            field: MultiLabelBinarizer(classes=[e for e in enums])
            for field, enums in self.multi_label_fields.items()
        }
        self.all_columns = self._get_all_columns()

    def _get_enum_fields(self) -> tuple[dict[str, list[Enum]], dict[str, list[Enum]]]:
        """Extracts multi-label (List[Enum]) and single-label (Enum) fields dynamically."""
        multi_label_fields = {}
        single_label_fields = {}

        for field_name, field in self.model.__pydantic_fields__.items():
            main_type = field.annotation.__args__[0]
            if (
                hasattr(main_type, "__origin__") and main_type.__origin__ is list
            ):  # Multi-label List[Enum]
                enum_type = main_type.__args__[0]
                if issubclass(enum_type, Enum):
                    multi_label_fields[field_name] = list(enum_type)
            elif issubclass(main_type, Enum):  # Single-label Enum
                single_label_fields[field_name] = list(main_type)

        return multi_label_fields, single_label_fields

    def _get_all_columns(self):
        """Generates all possible column names to ensure a fixed schema."""
        columns = [
            f"{field}_{e.value}"
            for field, values in self.multi_label_fields.items()
            for e in values
        ]
        columns += [
            f"{field}_{e.value}"
            for field, values in self.single_label_fields.items()
            for e in values
        ]
        return columns

    def transform(self, instances: list[BaseModel]) -> pd.DataFrame:
        """Encodes a batch of Pydantic instances into a consistent one-hot encoded DataFrame."""
        encoded_results = []

        for instance in instances:
            data = instance.model_dump()
            encoded_data = {}

            # Multi-label encoding
            for field, mlb in self.mlb_encoders.items():
                values = data.get(field, [])
                encoded = mlb.fit_transform([values])  # Encode
                encoded_data.update(dict(zip(mlb.classes_, encoded[0])))

            # Single-label encoding
            for field, all_classes in self.single_label_fields.items():
                value = data.get(field)
                all_classes = [e for e in all_classes]
                for class_value in all_classes:
                    encoded_data[f"{class_value}"] = 1 if class_value == value else 0

            encoded_results.append(encoded_data)

        df = pd.DataFrame(encoded_results)
        df.columns = self.all_columns  # Ensure all columns are present
        return df
