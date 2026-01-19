## Project description: trend analysis from a table of messages, dates and channels

## Project structure:
- src/
- test/
- data/
- notebooks/

## Guidelines
- Use Python 3.13.XX. 
- Use type hints 
- Always follow PEP 8 style guidelines.
- Use DI patterns


## Helpers 
- **Pylint** for syntax and style checking
- **Conda** package manager 

## Libraries
- **duckdb** for in memory database management
- **pandas** for data manipulation and analysis

## Testing Instructions
- **Framework:** Always use `pytest`.
- **Location:** All tests must go in the `tests/` directory.
- **Mocking:** Use `pytest-mock` for API or database calls.
- **Execution:** Run `run pytest`.
