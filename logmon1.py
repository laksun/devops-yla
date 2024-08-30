import os
import sys
import logging
import time
import subprocess
import time
import subprocess
import platform
from subprocess import Popen, PIPE

sys.path.append("/usr/local/myenv/aws/lib/python/site-packages")
from logmon_common import LogmonCommon

s3ConfigFile = "/usr/local/s3.conf"
chmodList = ["o+rx /var/log/amazon/"]

chmod_recursive = ["o=r"]

chmod_dir_recursive = ["a=rx"]


def set_environ():
    if "Ubuntu" in platform.version():
        cert_bundle = "/etc/ssl/certs/a.crt"
    else:
        cert_bundle = "/etc/ssl/certs/b.crt"
    os.environ["REQUESTS_CA_BUNDLE"] = cert_bundle
    os.environ["SSL_CERT_FILE"] = cert_bundle


def is_agent_running(program, arg):
    agent_running = True
    try:
        p = Popen([program, arg], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate(b"input data that is passed to subprocess' stdin")
        agent_running = b"OK" in output
    except Exception as key:
        return agent_running


def restart_agent(path, name):
    # Restart the agent
    ret = subprocess.call(f"{path} stop", shell=True)
    time.sleep(10)
    logging.info(f"trying to force kill {name} process if any")
    os.system(f"pkill -9 -f {name}")
    time.sleep(10)
    logging.info(f"starting {name}")
    ret = subprocess.call(f"{path} start", shell=True)
    return ret


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
                fluentd_check_counter = fluentd_check_counter + 1
                logging.info(f"{fluentd_config.fluentd_user} is stopped")
                if fluentd_check_counter >= 3:
                    restart_agent(
                        f"/etc/init.d/{fluentd_config.fluentd_user}",
                        fluentd_config.fluentd_user,
                    )
                    fluentd_check_counter = 0
                else:
                    fluentd_check_counter = 0

                for entry in chown_list:
                    if os.path.exists(entry.split(" ")[1]):
                        os.system(f"chown -cR {entry}")
                for entry in chmodList:
                    if os.path.exists(entry.split(" ")[1]):
                        os.system(f"chmod -R {entry}")

                for entry in chmod_recursive:
                    if os.path.exists(entry.split(" ")[2]):
                        find_perm = entry.split(" ")[0]
                        perm = entry.split(" ")[1]
                        path = entry.split(" ")[2]
                        pattern = entry.split(" ")[3]
                        os.system(
                            "find %s -xdev -path %s -mmin -60 ! -perm -%s -ls -exec chmod -c %s {} \;"
                            % (path, pattern, find_perm, perm)
                        )
                for entry in chmod_dir_recursive:
                    if os.path.exists(entry.split(" ")[2]):
                        find_perm = entry.split(" ")[0]
                        perm = entry.split(" ")[1]
                        path = entry.split(" ")[2]

                        os.system(
                            "find %s -xdev -type d -mmin -60 ! -perm -%s -ls -exec chmod -c %s {} \;"
                            % (path, find_perm, perm)
                        )
        except Exception as key:
            logging.error(f"Error {key}")
        time.sleep(60)


if __name__ == "__main__":
    main()
