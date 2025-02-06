Renaming a Git branch (whether hosted on Bitbucket, GitHub, or another Git remote) involves creating a new branch name locally, deleting the old branch on the remote, and then pushing the new branch name. Bitbucket doesn’t currently offer a built-in “rename” button in its UI to do this automatically, so you’ll do it via Git commands.

Below is a step-by-step guide:

---

## 1. Make Sure Your Local Repo Is Up to Date

```bash
git fetch
git pull
```
- **`git fetch`** updates your local list of remote branches (but does not merge them).
- **`git pull`** merges any updates from the remote into your currently checked-out branch.

---

## 2. Check Out the Old Branch Locally

```bash
git checkout old-branch
```
If you don't have `old-branch` locally, you can create a local copy that tracks the remote branch:
```bash
git checkout -b old-branch origin/old-branch
```

---

## 3. Rename the Local Branch

Use the **`-m`** (move/rename) option:
```bash
git branch -m old-branch new-branch
```

If you are **already on** `old-branch` when you run this, you can also do:
```bash
git checkout old-branch
git branch -m new-branch
```
Either way, this changes the local branch name from `old-branch` to `new-branch`.

---

## 4. Delete the Old Branch on the Remote

To remove the old branch reference from Bitbucket:
```bash
git push origin --delete old-branch
```
(Or equivalently, `git push origin :old-branch`.)

---

## 5. Push the Newly Renamed Branch

Now push the new branch name to Bitbucket:
```bash
git push origin new-branch
```

If you want the local branch to track the remote automatically, you can also do:
```bash
git push -u origin new-branch
```
The **`-u`** (or `--set-upstream`) sets the remote tracking branch so future `git pull` and `git push` commands work without specifying `origin new-branch`.

---

## 6. Verify on Bitbucket

1. Go to your Bitbucket repository and check **Branches**.
2. You should now see `new-branch` and no longer see `old-branch` (unless it’s still referenced by another user’s fork or an open Pull Request).

---

## 7. Update Any Open Pull Requests or References

- If you had an open Pull Request (PR) on `old-branch`, you may need to update the PR to use `new-branch` or create a new PR from `new-branch`.  
- Communicate with your team or collaborators so they know the branch name changed.

---

### Summary

1. **Fetch and check out** the old branch locally.  
2. **Rename** it using `git branch -m old-branch new-branch`.  
3. **Delete** the old remote branch with `git push origin --delete old-branch`.  
4. **Push** the new branch name with `git push -u origin new-branch`.  
5. **Update references** in PRs or CI systems accordingly.

Following these steps effectively “renames” your branch in Bitbucket, even though it’s done via Git commands rather than a Bitbucket UI action.