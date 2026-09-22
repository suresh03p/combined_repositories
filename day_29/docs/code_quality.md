# Code Quality Checks

The project uses a simple but effective quality layer in CI:

- Ruff for linting and basic static checks
- Black for formatting consistency
- Python syntax and test execution validation

These checks ensure the code remains maintainable and reduces obvious mistakes before the application is packaged.

## Why these tools

- Ruff finds unused imports, unused variables, and common quality issues quickly
- Black enforces a consistent format across developers and CI
- pytest confirms runtime behavior remains correct

This combination creates a lightweight quality gate suitable for a production-ready pipeline without excessive complexity.
