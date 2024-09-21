Here's a step-by-step guide to creating an SSH key for GitHub on your Mac and configuring it:

### 1. **Generate a New SSH Key:**

1. **Open Terminal** on your Mac.

2. **Generate SSH Key** using the following command:

   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```
   - Replace `your_email@example.com` with your GitHub email address.
   - If you are using an older system that doesn't support `ed25519`, you can use `rsa` instead:

   ```bash
   ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
   ```

3. **Follow the Prompts:**
   - It will ask you to enter a file to save the key. Press `Enter` to accept the default location.
   - It will then prompt you to enter a passphrase. You can either choose a passphrase (recommended for security) or press `Enter` for no passphrase.

4. **Start the SSH Agent:**
   
   Start the SSH agent in the background with the following command:

   ```bash
   eval "$(ssh-agent -s)"
   ```

5. **Add the SSH Key to the Agent:**

   Use this command to add your SSH private key to the ssh-agent:

   ```bash
   ssh-add -K ~/.ssh/id_ed25519
   ```
   - If you used `rsa`, the file will be `id_rsa` instead of `id_ed25519`.

### 2. **Add SSH Key to GitHub:**

1. **Copy the SSH Key** to your clipboard:

   ```bash
   pbcopy < ~/.ssh/id_ed25519.pub
   ```
   - If you used `rsa`, use this instead:

   ```bash
   pbcopy < ~/.ssh/id_rsa.pub
   ```

2. **Go to GitHub** and log in.

3. **Navigate to Settings:**
   - Click on your profile photo in the top-right corner and go to `Settings`.
   
4. **Go to SSH and GPG Keys:**
   - On the left sidebar, click on `SSH and GPG keys`.
   
5. **Add a New SSH Key:**
   - Click the `New SSH key` button.
   - Title your key (e.g., "MacBook Pro").
   - Paste the key you copied into the "Key" field.
   - Click `Add SSH key`.

6. **Confirm Your Password:**
   - If prompted, enter your GitHub password to confirm the action.

### 3. **Test SSH Connection:**

1. In your terminal, type:

   ```bash
   ssh -T git@github.com
   ```

2. You should see a message like this:

   ```bash
   Hi username! You've successfully authenticated, but GitHub does not provide shell access.
   ```

This confirms that your SSH key is correctly configured and you can now use it to interact with GitHub repositories securely.

If you have any issues or need further configuration, feel free to ask!

## Gotcha
This warning is informing you that the `-K` and `-A` flags are deprecated in the `ssh-add` command on macOS. Instead, you should use the new flags `--apple-use-keychain` and `--apple-load-keychain`.

### Updated Instructions for Adding SSH Key to macOS Keychain:

1. **Add the SSH Key with the New Flags:**
   
   Instead of using the deprecated `-K` flag, use the following command:

   ```bash
   ssh-add --apple-use-keychain ~/.ssh/id_ed25519
   ```
   - If you used `rsa`, use this command:

   ```bash
   ssh-add --apple-use-keychain ~/.ssh/id_rsa
   ```

2. **Suppress the Warning (Optional):**
   
   To suppress the warning, you can set the environment variable `APPLE_SSH_ADD_BEHAVIOR`. You can do this temporarily for your current terminal session with:

   ```bash
   export APPLE_SSH_ADD_BEHAVIOR="Apple"
   ```

   If you want to make this change permanent, add the above line to your `~/.bash_profile` or `~/.zshrc` file, depending on the shell you are using.

3. **Verify Key is Added:**

   You can check if your key was successfully added with:

   ```bash
   ssh-add -l
   ```

   It should list your SSH key, indicating it has been added to the SSH agent and the macOS keychain.

Using these updated commands will prevent the warning from appearing again. Let me know if you need any more help!

## session issue

The issue you're facing is likely because the SSH key is not being loaded into the SSH agent automatically when you open a new terminal session. When you start a new terminal, the SSH agent does not remember the key added in a previous session, so you get a "Permission denied" error.

### Steps to Fix the Issue

1. **Ensure the SSH Agent is Started Automatically:**
   Add the following lines to your shell configuration file (`~/.bashrc`, `~/.bash_profile`, or `~/.zshrc`, depending on your shell):

   ```bash
   # Start the ssh-agent and load the SSH key
   eval "$(ssh-agent -s)"
   ssh-add --apple-use-keychain ~/.ssh/sep_21_id
   ```

   This ensures that every time you open a new terminal, the SSH agent starts and the key is added automatically.

2. **Add the Key to the macOS Keychain Permanently:**
   
   If you are on macOS, you can use the following command to permanently add the key to the keychain so that it persists across reboots:

   ```bash
   ssh-add --apple-use-keychain ~/.ssh/sep_21_id
   ```

3. **Modify the `config` File for Automatic Key Loading:**
   
   You can also create or modify your `~/.ssh/config` file to automatically use your SSH key when accessing GitHub:

   1. Open or create the `~/.ssh/config` file:

      ```bash
      nano ~/.ssh/config
      ```

   2. Add the following lines to specify your key for GitHub:

      ```bash
      Host github.com
        User git
        HostName github.com
        IdentityFile ~/.ssh/sep_21_id
        UseKeychain yes
        AddKeysToAgent yes
      ```

   3. Save and exit the file (press `Ctrl + X`, then `Y`, and `Enter`).

4. **Check for Correct File Permissions:**
   
   Make sure that your SSH key files have the correct permissions. Run the following command to set the appropriate permissions:

   ```bash
   chmod 600 ~/.ssh/sep_21_id
   ```

5. **Restart the Terminal:**
   
   After making these changes, restart your terminal and try connecting to GitHub again.

### Summary

Adding the SSH key to the SSH agent in each terminal session is necessary because the SSH agent doesn’t persist keys across new terminal sessions by default. By adding the key to the macOS keychain or configuring it in the `~/.ssh/config` file, you ensure that the key is available in new sessions without needing to re-run the `ssh-add` command.