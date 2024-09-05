To uninstall a service in Amazon Linux 2, you can follow these general steps:

### 1. **Stop the Service**
First, stop the service if it's running:

```bash
sudo systemctl stop <service_name>
```

### 2. **Disable the Service**
If you don’t want the service to start again on boot, disable it:

```bash
sudo systemctl disable <service_name>
```

### 3. **Uninstall the Package**
To remove the service, you can uninstall the package associated with it using `yum`, the package manager for Amazon Linux 2. Replace `<package_name>` with the name of the package you want to uninstall:

```bash
sudo yum remove <package_name>
```

If you're unsure of the package name, you can use the following command to list installed packages related to the service:

```bash
yum list installed | grep <service_name>
```

### 4. **Check the Service Removal**
Once uninstalled, you can check if the service has been completely removed:

```bash
systemctl list-units --type=service | grep <service_name>
```

This should uninstall the service from your Amazon Linux 2 system.