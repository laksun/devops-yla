Using `os.system()` with string interpolation (e.g., `f"rpm -q {package_name}"`) can lead to **shell injection vulnerabilities** if the input, such as `package_name`, is not properly sanitized. An attacker could craft malicious input to inject additional commands. To resolve this and prevent potential shell injection, it's better to use safer alternatives like `subprocess` with the argument list approach, which avoids invoking a shell.

Here are safer ways to execute commands in Python:

### 1. **Using `subprocess.run()` with a List of Arguments**:
Instead of passing a command as a string (which invokes a shell), you can pass it as a list of arguments. This ensures that the command is executed directly without going through a shell, thereby preventing shell injection.

#### Example:
```python
import subprocess

package_name = "bash"  # Example package name
try:
    result = subprocess.run(
        ["rpm", "-q", package_name],  # Command and arguments as a list
        check=True,                   # Raises an exception if the command fails
        capture_output=True,           # Captures stdout and stderr
        text=True                      # Returns output as a string instead of bytes
    )
    print(result.stdout)  # Output of the command
except subprocess.CalledProcessError as e:
    print(f"Error occurred: {e}")
```

### Why This Is Safer:
- **No Shell Invocation**: By using a list of arguments, you're avoiding shell interpretation, so special characters (like `&`, `|`, `;`, etc.) in `package_name` will not be interpreted as shell commands. This prevents shell injection attacks.
- **Automatic Quoting**: Since you’re passing each argument as a list element, there’s no need to manually quote or escape arguments.

### 2. **Using `shlex.quote()` for Shell Input Sanitization** (If You Must Use `os.system`)
If you must use `os.system()` for some reason, you can escape the input to prevent shell injection. The `shlex.quote()` function safely quotes a string so it can be used in shell commands without risk of injection.

#### Example:
```python
import os
import shlex

package_name = "bash"
safe_package_name = shlex.quote(package_name)  # Safely escape input

os.system(f"rpm -q {safe_package_name}")  # Safe because the input is escaped
```

While this approach can mitigate the risk of injection, it's still recommended to use `subprocess.run()` to avoid shell invocation altogether.

### 3. **Using `subprocess.Popen()` for Advanced Use Cases**
If you need more control over the process, such as real-time output handling, you can use `subprocess.Popen()`. This also avoids shell injection when used properly with argument lists.

#### Example:
```python
import subprocess

package_name = "bash"
process = subprocess.Popen(
    ["rpm", "-q", package_name],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

stdout, stderr = process.communicate()

if process.returncode == 0:
    print(stdout)  # Command output
else:
    print(f"Error: {stderr}")
```

### Key Takeaways:
- **Avoid `os.system()`** whenever possible because it opens up risks for shell injection.
- Use **`subprocess.run()`** with a list of arguments to avoid passing commands through the shell.
- If shell invocation is required, **sanitize the input** with `shlex.quote()`, but this is generally not as safe as using `subprocess` without a shell.
