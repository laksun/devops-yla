Here's a simple shell script to find the installed packages related to a given service, uninstall those packages, and disable the service on Amazon Linux 2022.

```bash
#!/bin/bash

# Define the service name
SERVICE_NAME="$1"

if [ -z "$SERVICE_NAME" ]; then
  echo "Usage: $0 <service_name>"
  exit 1
fi

echo "Disabling the $SERVICE_NAME service..."

# Disable the service
sudo systemctl disable $SERVICE_NAME

# Stop the service if running
sudo systemctl stop $SERVICE_NAME

echo "Finding the installed packages related to $SERVICE_NAME..."

# Find installed packages related to the service
INSTALLED_PACKAGES=$(yum list installed | grep "$SERVICE_NAME")

if [ -z "$INSTALLED_PACKAGES" ]; then
  echo "No installed packages found related to $SERVICE_NAME."
else
  echo "Installed packages:"
  echo "$INSTALLED_PACKAGES"
  
  # Uninstall the packages
  echo "Uninstalling packages..."
  sudo yum remove -y $(echo "$INSTALLED_PACKAGES" | awk '{print $1}')
  
  echo "Packages related to $SERVICE_NAME have been uninstalled."
fi

echo "The $SERVICE_NAME service has been disabled and related packages have been removed (if found)."
```

### Explanation:
1. **Service Name Input**: The script expects the service name as an argument (`$1`).
2. **Disabling and Stopping the Service**: It disables and stops the service using `systemctl`.
3. **Finding Installed Packages**: It uses `yum list installed` to find the installed packages related to the service name.
4. **Removing Packages**: The packages are uninstalled using `yum remove`.
5. **Safety**: It checks if any packages are found before attempting to remove them.

### Usage:
1. Save the script as `manage_service.sh`.
2. Make it executable with:
   ```bash
   chmod +x manage_service.sh
   ```
3. Run the script with the service name:
   ```bash
   ./manage_service.sh <service_name>
   ``` 

For example, to disable and remove packages related to `httpd`:
```bash
./manage_service.sh httpd
```