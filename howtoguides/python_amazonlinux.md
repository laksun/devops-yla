Currently, Amazon Linux 2023 (AL2023) does not have an RPM package for Python 3.12 in its default repositories. The default system version is Python 3.9, and while Python 3.11 is available as an additional version, there is no official support for Python 3.12 at the moment【6†source】【9†source】.

However, you can install Python 3.12 from source on Amazon Linux 2023 by following these steps:

1. **Update your system**:
   ```bash
   sudo dnf update -y
   ```

2. **Install required development tools and libraries**:
   ```bash
   sudo dnf groupinstall "Development Tools" -y
   sudo dnf install gcc openssl-devel bzip2-devel libffi-devel -y
   ```

3. **Download Python 3.12 source code**:
   ```bash
   cd /usr/src
   sudo wget https://www.python.org/ftp/python/3.12.2/Python-3.12.2.tgz
   sudo tar xzf Python-3.12.2.tgz
   ```

4. **Configure and compile Python**:
   ```bash
   cd Python-3.12.2
   sudo ./configure --enable-optimizations
   sudo make -j 8
   ```

5. **Install Python 3.12**:
   ```bash
   sudo make altinstall
   ```

6. **Verify the installation**:
   ```bash
   python3.12 --version
   ```

This method compiles Python from source, allowing you to run Python 3.12 alongside the system Python without interfering with the default version【7†source】【9†source】.

If you want official RPM support, it's worth tracking updates on package requests from the community, but for now, compiling from source is the best option.

**a.** Would you like instructions on setting up virtual environments with Python 3.12 after installation?

**b.** Are you interested in automating this process in a Docker container or ECS task?