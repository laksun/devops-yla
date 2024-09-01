import os
import sys
import logging
import time
import subprocess
import platform
from subprocess import Popen, PIPE

sys.path.append("/usr/local/myenv/aws/lib/python/site-packages")
from logmon_common import LogmonCommon

# Configuration constants
S3_CONFIG_FILE = "/usr/local/s3.conf"
CHMOD_LIST = ["o+rx /var/log/amazon/"]
CHMOD_RECURSIVE = ["o=r"]
CHMOD_DIR_RECURSIVE = ["a=rx"]

# Paths for certificates
CERT_BUNDLE_UBUNTU = "/etc/ssl/certs/a.crt"
CERT_BUNDLE_DEFAULT = "/etc/ssl/certs/b.crt"


def set_environ():
    """Set the environment variables for SSL certificates based on the platform."""
    cert_bundle = (
        CERT_BUNDLE_UBUNTU if "Ubuntu" in platform.version() else CERT_BUNDLE_DEFAULT
    )
    os.environ["REQUESTS_CA_BUNDLE"] = cert_bundle
    os.environ["SSL_CERT_FILE"] = cert_bundle


def is_agent_running(program, arg):
    """Check if the specified agent is running."""
    try:
        with Popen([program, arg], stdin=PIPE, stdout=PIPE, stderr=PIPE) as p:
            output, _ = p.communicate(b"input data that is passed to subprocess' stdin")
            return b"OK" in output
    except Exception as e:
        logging.error(f"Error checking if agent is running: {e}")
        return False


def restart_agent(path, name):
    """Restart the specified agent."""
    logging.info(f"Stopping {name}...")
    subprocess.run([path, "stop"], check=True)
    time.sleep(10)

    logging.info(f"Force killing {name} process if any...")
    subprocess.run(["pkill", "-9", "-f", name], check=False)
    time.sleep(10)

    logging.info(f"Starting {name}...")
    return subprocess.run([path, "start"], check=True)


def apply_permissions(chown_list, chmod_list, chmod_recursive, chmod_dir_recursive):
    """Apply chown and chmod permissions as specified."""
    for entry in chown_list:
        user, path = entry.split(" ")
        if os.path.exists(path):
            logging.info(f"Changing ownership of {path} to {user}")
            subprocess.run(["chown", "-cR", user, path], check=True)

    for entry in chmod_list:
        if os.path.exists(entry.split(" ")[1]):
            logging.info(f"Applying chmod {entry} recursively")
            subprocess.run(["chmod", "-R", entry], check=True)

    # Additional permission application logic can be added here as needed


def main():
    logmon_common = LogmonCommon()
    fluentd_config = logmon_common.fluentd_config

    chown_list = [
        f"{fluentd_config.fluentd_user} {fluentd_config.var_log_path}",
        f"{fluentd_config.fluentd_user} {fluentd_config.etc_path}",
    ]

    set_environ()
    fluentd_check_counter = 0

    while True:
        try:
            if not is_agent_running(
                f"/etc/init.d/{fluentd_config.fluentd_user}", "status"
            ):
                fluentd_check_counter += 1
                logging.info(f"{fluentd_config.fluentd_user} is stopped")
                if fluentd_check_counter >= 3:
                    restart_agent(
                        f"/etc/init.d/{fluentd_config.fluentd_user}",
                        fluentd_config.fluentd_user,
                    )
                    fluentd_check_counter = 0

                apply_permissions(
                    chown_list, CHMOD_LIST, CHMOD_RECURSIVE, CHMOD_DIR_RECURSIVE
                )
            else:
                fluentd_check_counter = 0  # Reset counter if agent is running
        except Exception as e:
            logging.error(f"Error in main loop: {e}")
        time.sleep(60)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
