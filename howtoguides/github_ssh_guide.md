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