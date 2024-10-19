Python linting tools help analyze and improve code quality by identifying issues like coding style violations, potential bugs, and more. Here are some popular Python linting tools, along with examples of their usage:

### 1. **Pylint**
   - **Description**: One of the most comprehensive Python linting tools, `Pylint` checks for code style violations, errors, and even performance issues. It provides detailed reports on code quality, including suggestions for improvements.
   - **Features**:
     - Extensive style and error checking.
     - Can be customized with configuration files.
     - Reports code complexity.
   
   **Installation**:
   ```bash
   pip install pylint
   ```

   **Usage**:
   ```bash
   pylint my_script.py
   ```

   Example output:
   ```
   ************* Module my_script
   my_script.py:1:0: C0114: Missing module docstring (missing-module-docstring)
   my_script.py:3:4: C0103: Variable name "x" doesn't conform to snake_case naming style (invalid-name)
   ```

### 2. **Flake8**
   - **Description**: A lightweight linting tool that combines `PyFlakes`, `pycodestyle` (formerly `PEP8`), and `McCabe` complexity checker. It focuses on enforcing the PEP8 style guide.
   - **Features**:
     - Fast and minimal output.
     - Easily extendable with plugins.
     - Checks code style and complexity.

   **Installation**:
   ```bash
   pip install flake8
   ```

   **Usage**:
   ```bash
   flake8 my_script.py
   ```

   Example output:
   ```
   my_script.py:1:1: F401 'os' imported but unused
   my_script.py:3:5: E303 too many blank lines (2)
   ```

### 3. **Black (Code Formatter with Linting)**
   - **Description**: `Black` is an opinionated Python code formatter. While primarily a formatter, it also serves as a linter by enforcing consistent code style. It automatically reformats code to conform to PEP8.
   - **Features**:
     - Automatic code formatting.
     - Zero-config, consistent results.
     - Fast and deterministic output.

   **Installation**:
   ```bash
   pip install black
   ```

   **Usage**:
   ```bash
   black my_script.py
   ```

   Black will automatically format your code and print changes if needed:
   ```
   reformatted my_script.py
   ```

### 4. **Pyflakes**
   - **Description**: A fast and simple static analysis tool that checks for logical errors in Python code without enforcing style guide rules (unlike Flake8 or Pylint). It focuses on detecting code issues like unused imports or undefined variables.
   - **Features**:
     - Lightweight and fast.
     - Checks for common coding issues, such as unused variables or imports.
     - No configuration required.

   **Installation**:
   ```bash
   pip install pyflakes
   ```

   **Usage**:
   ```bash
   pyflakes my_script.py
   ```

   Example output:
   ```
   my_script.py:1: 'os' imported but unused
   ```

### 5. **Mypy (Static Type Checker)**
   - **Description**: `Mypy` is a static type checker for Python. It checks the types in your Python code based on annotations (Python’s type hints) and helps catch type errors before runtime.
   - **Features**:
     - Detects type-related bugs early.
     - Supports gradual typing (works with both typed and untyped code).
     - Integrates well with existing Python codebases.

   **Installation**:
   ```bash
   pip install mypy
   ```

   **Usage**:
   ```bash
   mypy my_script.py
   ```

   Example output:
   ```
   my_script.py:4: error: Argument 1 to "print" has incompatible type "int"; expected "str"
   ```

### 6. **Bandit (Security Linter)**
   - **Description**: `Bandit` is a security-focused linting tool that checks for common security issues in Python code. It is designed to find potential vulnerabilities in the code, such as hardcoded passwords or weak cryptographic methods.
   - **Features**:
     - Detects security issues in Python code.
     - Customizable with configuration files.
     - Works well in CI/CD pipelines.

   **Installation**:
   ```bash
   pip install bandit
   ```

   **Usage**:
   ```bash
   bandit -r my_project/
   ```

   Example output:
   ```
   [B101:assert_used] Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.
   ```

### 7. **pydocstyle (PEP257 Docstring Style Checker)**
   - **Description**: `pydocstyle` checks that your Python docstrings comply with the PEP 257 conventions. It focuses specifically on enforcing good docstring practices, such as having consistent descriptions and formats.
   - **Features**:
     - Enforces PEP257 docstring conventions.
     - Can be integrated into CI/CD processes.
     - Supports custom configuration.

   **Installation**:
   ```bash
   pip install pydocstyle
   ```

   **Usage**:
   ```bash
   pydocstyle my_script.py
   ```

   Example output:
   ```
   my_script.py:1 at module level:
   D100: Missing docstring in public module
   ```

### 8. **Ruff**
   - **Description**: Ruff is an extremely fast Python linter that is written in Rust. It aims to provide linting and code checks at high speeds, often outperforming other tools like Flake8. Ruff provides checks for style violations, unused imports, and even integrates some Flake8 plugins.
   - **Features**:
     - Blazing fast linting.
     - Supports a variety of linter rules, including some from Flake8, pyflakes, and more.
     - Configurable with pyproject.toml or ruff.toml.

   **Installation**:
   ```bash
   pip install ruff
   ```

   **Usage**:
   ```bash
   ruff my_script.py
   ```

   Example output:
   ```
   my_script.py:2:1: F401 `os` imported but unused
   ```

---

### Summary Table:

| Linter       | Primary Purpose                  | Usage Example                           |
|--------------|----------------------------------|-----------------------------------------|
| **Pylint**   | Comprehensive linting (style + errors) | `pylint my_script.py`                   |
| **Flake8**   | Style guide enforcement (PEP8)   | `flake8 my_script.py`                   |
| **Black**    | Code formatting                  | `black my_script.py`                    |
| **Pyflakes** | Lightweight error checking       | `pyflakes my_script.py`                 |
| **Mypy**     | Static type checking             | `mypy my_script.py`                     |
| **Bandit**   | Security analysis                | `bandit -r my_project/`                 |
| **pydocstyle**| Docstring style enforcement     | `pydocstyle my_script.py`               |
| **Ruff**     | Fast linting                     | `ruff my_script.py`                     |

Each of these tools has its strengths, depending on whether you need code style checks, type checking, security checks, or docstring validation. You can integrate them into your workflow either individually or together for comprehensive linting.