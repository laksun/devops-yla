To retrieve the version of a specific file from the `origin/main` branch (the remote version of the main branch) and update it in your current branch, you can use:

```bash
git fetch origin main
git checkout origin/main -- path/to/your/file
```

### Explanation:

1. `git fetch origin main`: This updates your local knowledge of the `origin/main` branch without merging any changes.
2. `git checkout origin/main -- path/to/your/file`: This retrieves the specified file from `origin/main` and places it in your current working directory.

If you want to keep this change, you should stage and commit it:

```bash
git add path/to/your/file
git commit -m "Updated file from origin/main branch"
```

This will update your current branch’s version of the file with the latest from `origin/main`.