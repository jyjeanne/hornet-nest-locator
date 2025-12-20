# 🎨 Code Style Guide

This document describes the coding standards and style guidelines for the Hornet Nest Locator project.

## 🔧 Tools & Configuration

### Ruff Linter

We use **[Ruff](https://github.com/astral-sh/ruff)** as our primary linting and formatting tool. Ruff is an extremely fast Python linter that combines the functionality of Flake8, isort, pyupgrade, and many other tools.

**Configuration**: See `pyproject.toml` for the complete Ruff configuration.

### Key Features Enabled

```toml
[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "F",      # Pyflakes
    "W",      # pycodestyle warnings
    "I",      # isort
    "N",      # pep8-naming
    "UP",     # pyupgrade
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "T20",    # flake8-print
    "PYI",    # flake8-pyi
    "PT",     # flake8-pytest-style
    "Q",      # flake8-quotes
    "RUF",    # Ruff-specific rules
    "SIM",    # flake8-simplify
    "TID",    # flake8-tidy-imports
    "ARG",    # flake8-unused-arguments
    "PLC",    # pylint-convention
    "PLE",    # pylint-error
    "PLW",    # pylint-warning
]
```

## 📏 Formatting Rules

### Line Length
- **Maximum**: 100 characters
- **Rationale**: Balances readability with modern screen sizes

### Indentation
- **Style**: 4 spaces (no tabs)
- **Consistency**: Enforced by Ruff formatter

### Quotes
- **Strings**: Double quotes (`""`) preferred
- **Docstrings**: Double quotes (`""""""`)
- **Multiline**: Double quotes

### Imports
- **Organization**: Automatic sorting by isort
- **Grouping**: Standard library → Third-party → First-party → Local
- **Combining**: Related imports combined when possible

## 🎯 Code Quality Rules

### Naming Conventions

```python
# Variables and functions
snake_case = "use_snake_case"

# Constants
CONSTANT_NAME = "UPPER_SNAKE_CASE"

# Classes
class ClassName:
    pass

# Methods
class MyClass:
    def method_name(self):
        pass

# Modules
module_name.py
```

### Function Guidelines

1. **Single Responsibility**: Each function should do one thing
2. **Length**: Keep functions focused and concise
3. **Documentation**: Use docstrings for public functions
4. **Type Hints**: Use Python type hints where appropriate

### Error Handling

```python
# Good: Specific exception handling
def safe_divide(a: float, b: float) -> float:
    try:
        return a / b
    except ZeroDivisionError:
        logger.error("Division by zero attempted")
        return float('inf')

# Avoid: Bare except clauses
def bad_example():
    try:
        risky_operation()
    except:  # Too broad!
        pass
```

## 🔍 Linting Rules

### Common Issues to Avoid

| Rule | Description | Example |
|------|-------------|---------|
| `F401` | Unused import | `import unused_module` |
| `E501` | Line too long | `very_long_line = "..." * 200` |
| `F841` | Unused variable | `x = 42` (never used) |
| `B008` | Function call in default | `def func(arg=expensive_call()):` |
| `C901` | Complex function | Functions with high cyclomatic complexity |

### Best Practices

```python
# ✅ Good: Use context managers
with open("file.txt") as f:
    content = f.read()

# ❌ Bad: Manual resource management
f = open("file.txt")
content = f.read()
f.close()

# ✅ Good: List comprehensions
squares = [x**2 for x in range(10)]

# ❌ Bad: Unnecessary loops
squares = []
for x in range(10):
    squares.append(x**2)

# ✅ Good: f-strings (Python 3.6+)
message = f"Value: {value}"

# ❌ Bad: Old-style formatting
message = "Value: %s" % value
```

## 🧪 Testing Standards

### Test Organization

```python
# Good test structure
class TestCalculator:
    def test_empirical_method(self):
        """Test empirical distance calculation."""
        observation = Observation(latitude=48.8584, longitude=2.2945, 
                                 bearing=45.0, round_trip_time=390)
        assert observation.estimated_distance_empirical == 650.0

    def test_theoretical_method(self):
        """Test theoretical distance calculation."""
        observation = Observation(latitude=48.8584, longitude=2.2945, 
                                 bearing=45.0, round_trip_time=300, speed=7.0)
        assert observation.estimated_distance_theoretical == 1050.0
```

### Test Naming

- **Test classes**: `Test*` prefix (e.g., `TestCalculator`)
- **Test methods**: `test_*` prefix (e.g., `test_empirical_method`)
- **Descriptive names**: Clearly indicate what's being tested

## 📝 Documentation Standards

### Docstrings

```python
"""
Calculate hive location from hornet observations.

Uses the professional empirical method from Vespawatchers:
100 meters = 1 minute round trip time

Args:
    observation: Single hornet observation with all required data
    method: "empirical" (recommended) or "theoretical"

Returns:
    HiveLocation with estimated coordinates and confidence

Raises:
    ValueError: If method is unknown or speed is missing for theoretical method
"""
```

### Module Docstrings

```python
"""
Geographic calculation utilities using haversine formula.

This module provides functions for:
- Calculating destination points given bearing and distance
- Computing great circle distances between coordinates
- Formatting geographic coordinates for display
- Converting between different coordinate representations
"""
```

## 🛠️ Development Workflow

### Pre-commit Checks

```bash
# Check formatting
ruff format --check .

# Run linter
ruff check .

# Fix formatting issues automatically
ruff format .

# Run tests
pytest tests/ -v
```

### CI/CD Integration

The project uses GitHub Actions for continuous integration:

1. **Format Check**: Ensures code follows formatting rules
2. **Linting**: Catches code quality issues
3. **Testing**: Runs all unit tests
4. **Type Checking**: Optional mypy type checking

### Editor Integration

**VS Code**:
```json
{
  "python.linting.enabled": true,
  "python.linting.lintOnSave": true,
  "python.linting.provider": "ruff",
  "python.formatting.provider": "ruff",
  "editor.formatOnSave": true
}
```

**PyCharm**:
1. Install Ruff plugin
2. Set as default linter and formatter
3. Enable "Reformat on Save"

## 📚 Resources

- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [PEP 8 Style Guide](https://peps.python.org/pep-0008/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

## 🤝 Contributing

To maintain code quality:

1. **Run Ruff before committing**: `ruff check . && ruff format .`
2. **Write tests**: For new features and bug fixes
3. **Follow conventions**: Use existing code as reference
4. **Document changes**: Update docstrings and comments
5. **Keep it simple**: Prefer readability over cleverness

---

> "Code is read more often than it is written. Write for readability first."

This style guide helps maintain consistency across the codebase, making it easier for conservation workers and developers to understand, maintain, and extend the Hornet Nest Locator application.