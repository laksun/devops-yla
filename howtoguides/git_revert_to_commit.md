To **list the commits** in a Git branch and **reset your local branch** to a given commit from the remote (e.g., `origin`), you can follow these steps:

### 1. **List Commits in a Branch**:
To list the commits in the current branch, use:

```bash
git log
```

This will show the commit history of the current branch, including commit hashes, commit messages, authors, and dates.

#### Example Output:
```
commit f3b3b1d5e0a9c8fbc0d2bf34f2a6dc688f2e6e9a
Author: John Doe <johndoe@example.com>
Date:   Tue Oct 19 12:34:56 2023 +0100

    Fix issue #123

commit 5e6b9f3b423c8a4ab3c1fd256a1e58b8a2cd1234
Author: Jane Doe <janedoe@example.com>
Date:   Mon Oct 18 10:12:34 2023 +0100

    Add new feature
```

If you want a **one-line summary** of commits with just the commit hashes and messages, you can use:

```bash
git log --oneline
```

#### Example Output:
```
f3b3b1d5e Fix issue #123
5e6b9f3b4 Add new feature
```

### 2. **Reset Local Branch to a Given Commit from `origin`**:
To reset your local branch to a specific commit from the remote repository (`origin`), you can do the following:

#### Steps:

1. **Fetch the Latest Changes from `origin`**:
   Before resetting, make sure you have the latest updates from the remote branch:

   ```bash
   git fetch origin
   ```

2. **Reset to a Specific Commit**:
   To reset your local branch to a specific commit from `origin`, you need to use `git reset --hard` along with the commit hash.

   **Option 1: Reset to the Latest Commit from `origin`**:
   To reset your branch to the most recent commit from the remote:

   ```bash
   git reset --hard origin/branch_name
   ```

   This will move your local branch to match exactly what is on `origin/branch_name`.

   **Option 2: Reset to a Specific Commit**:
   If you want to reset to a specific commit (you should have the commit hash ready from the `git log` output):

   ```bash
   git reset --hard <commit_hash>
   ```

   For example:
   ```bash
   git reset --hard f3b3b1d5e0a9c8fbc0d2bf34f2a6dc688f2e6e9a
   ```

### Important Notes:
- **`git reset --hard`**: This command will reset your working directory, index, and HEAD to the specified commit, discarding any changes or commits that occurred after that commit in your local branch.
- **Make sure** to use this command carefully, as it will overwrite your local changes. If you want to keep uncommitted changes, you might want to use `git reset --soft` or `git stash` before resetting.

### 3. **Push the Reset Local Branch (if needed)**:
If you want to force-push your reset local branch back to the remote repository:

```bash
git push origin branch_name --force
```

This will overwrite the remote branch with your newly reset local branch.

### Summary of Commands:
1. **List commits**:
   ```bash
   git log             # Full commit history
   git log --oneline   # One-line commit history
   ```

2. **Fetch updates from `origin`**:
   ```bash
   git fetch origin
   ```

3. **Reset to the latest commit from `origin`**:
   ```bash
   git reset --hard origin/branch_name
   ```

4. **Reset to a specific commit**:
   ```bash
   git reset --hard <commit_hash>
   ```

5. **Push the reset branch to `origin` (if necessary)**:
   ```bash
   git push origin branch_name --force
   ```