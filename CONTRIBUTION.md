# Contributing to MLCosting

A quick guide for the development team.

## Getting Started

1. **Clone the repo:**
   ```bash
   git clone https://github.com/thinhngo-x/mlcosting.git
   cd mlcosting
   ```

2. **Set up environment:**
   ```bash
   uv sync --locked
   pre-commit install
   ```

## Workflow

1. **Create feature branch:**
   ```bash
   git checkout -b feature/your-feature
   ```

2. **Commit changes:**
   ```bash
   git commit -m "Descriptive message"
   ```

3. **Keep updated:**
   ```bash
   git fetch origin
   git rebase origin/master
   ```

4. **Submit PR** when ready

## Standards

- Use [Ruff](https://github.com/astral-sh/ruff) for linting/formatting
- Add type hints
- Document new functions
- Keep line length < 88 chars

## Adding Features

- For new datasets: Add JSON schema + generate Pydantic model
- For new ML models: Update `ModelName` enum and classifier logic
- Manual testing required for all changes

## Before PR

- Rebase on latest main
- Ensure pre-commit checks pass
- Document changes clearly

Questions? Ping the team in Slack.