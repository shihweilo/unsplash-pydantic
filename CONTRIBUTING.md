# Contributing to Unsplash Pydantic

Thank you for your interest in contributing to `unsplash-pydantic`! We welcome contributions from everyone. By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## 🛠 Development Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/unsplash-pydantic.git
    cd unsplash-pydantic
    ```

2.  **Set up the environment**:
    We recommend using a virtual environment.
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -e ".[dev]"
    ```

4.  **Install pre-commit hooks**:
    ```bash
    pre-commit install
    ```

## 🧪 Running Tests

We use `pytest` for testing.

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=unsplash
```

## 📝 Coding Standards

- **Formatting**: We use `ruff` for formatting and linting.
- **Type Checking**: We use `mypy` for static type checking.
- **Style**: Python code should be typed and follow modern practices.

To check your code before submitting:

```bash
# Lint and format
ruff check .
ruff format .

# Type check
mypy unsplash
```

## 📬 Submitting a Pull Request

1.  Fork the repository and create your branch from `main`.
2.  If you've added code that should be tested, add tests.
3.  Ensure your code passes all linting and test checks.
4.  Update the documentation if necessary.
5.  Open a Pull Request!

## 🐛 Reporting Bugs

Please use the [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.md) when reporting bugs.
