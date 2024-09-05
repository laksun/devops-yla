To configure IntelliJ IDEA so that it automatically converts CRLF (Carriage Return Line Feed) line endings to LF (Line Feed) and ensures that pushes to the repository use LF, follow these steps:

### Step 1: Configure Git in IntelliJ IDEA
1. **Open IntelliJ IDEA** and go to **File > Settings** (or **IntelliJ IDEA > Preferences** on macOS).
2. Navigate to **Version Control > Git**.
3. Under the **Git** settings, make sure that the path to Git is correctly configured.

### Step 2: Configure Git Settings for Line Endings
You need to adjust Git's configuration to handle line endings. Specifically, you want Git to always use LF for the repository, even if you’re working on a system (like Windows) that uses CRLF locally.

#### 1. **Global Git Config** (for all repositories)

Run the following Git commands in your terminal to configure line endings globally:

```bash
git config --global core.autocrlf input
```

This setting ensures that:
- **input**: Converts CRLF to LF when committing changes, and doesn't modify line endings when checking out code.

#### 2. **Per-Repository Git Config** (for a specific repository)

If you only want to enforce this behavior for a specific project, go to the root of your project directory and run:

```bash
git config core.autocrlf input
```

### Step 3: Configure IntelliJ IDEA to Use LF Line Endings
To ensure that IntelliJ IDEA consistently uses LF line endings in the editor and when saving files, follow these steps:

1. **Open IntelliJ IDEA** and go to **File > Settings** (or **IntelliJ IDEA > Preferences** on macOS).
2. Navigate to **Editor > Code Style**.
3. Under **Code Style**, select the specific language (or **General** for all file types).
4. In the **Line Separator** dropdown, select `LF - Unix and macOS (\n)`.

This setting ensures that all new files created in IntelliJ IDEA will use LF as the line ending.

### Step 4: Verify and Check Line Endings
After making these configurations, it’s a good practice to verify that your files are using LF line endings.

1. Go to the bottom-right corner of the IntelliJ window, where the line ending type is displayed (usually CRLF or LF).
2. If you find any file using CRLF, you can convert it manually to LF by clicking on the line ending and selecting `LF - Unix and macOS (\n)`.

### Step 5: Commit and Push Changes
When you push changes to the repository, Git will now automatically convert any CRLF line endings to LF before committing.

By following these steps, your IntelliJ IDEA environment and Git configuration will ensure that all files pushed to the repository use LF line endings, avoiding the issue of CRLF being pushed.