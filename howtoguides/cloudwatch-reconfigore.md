Below are common steps to **stop the Amazon CloudWatch Agent** on a Linux instance and then **reconfigure it**:

---

## 1. Stop the CloudWatch Agent

Depending on how you installed or started the agent, you typically stop it via **systemd** or by using the agent’s built-in control script:

<details>
<summary><strong>Method A: Systemd (Amazon Linux 2, Ubuntu, etc.)</strong></summary>

```bash
sudo systemctl stop amazon-cloudwatch-agent
```
</details>

<details>
<summary><strong>Method B: Amazon CloudWatch Agent Control Script</strong></summary>

```bash
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
    -a stop
```
</details>

Either method should successfully terminate the agent process.

---

## 2. Reconfigure the CloudWatch Agent

### Option A: Use the Configuration Wizard

1. **Run the wizard** to interactively set up metrics and logs:
   ```bash
   sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard
   ```
2. The wizard will generate or update your configuration file (often located under `/opt/aws/amazon-cloudwatch-agent/etc`).

3. **Start the agent** with your updated config:
   ```bash
   sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
       -a start \
       -c file:/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json \
       -m ec2
   ```
   *(If you’re on an on-prem server or different environment, use `-m onPremise` accordingly.)*

### Option B: Pull Configuration from Parameter Store or S3

If you store your config in Systems Manager Parameter Store or Amazon S3:

1. **Fetch and start** the agent:
   ```bash
   sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
       -a fetch-config \
       -m ec2 \
       -c ssm:AmazonCloudWatch-linux \
       --force
   ```
   > Adjust the `-c` argument to the correct path in SSM or S3. Add `--force` to overwrite the existing configuration.

2. This pulls the latest configuration and **starts** the agent with it.

---

## 3. Verify the Agent is Running

Once started, you can verify its status by running:

<details>
<summary><strong>Method A: Systemd</strong></summary>

```bash
sudo systemctl status amazon-cloudwatch-agent
```
</details>

<details>
<summary><strong>Method B: Agent Control Script</strong></summary>

```bash
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
    -a status
```
</details>

If everything is configured properly, you should see logs and metrics being sent to CloudWatch. You can check CloudWatch Logs in the AWS Console or verify metrics under **CloudWatch > Metrics** in the relevant namespace.

---

### Quick Recap

1. **Stop the agent** using `systemctl stop amazon-cloudwatch-agent` or `amazon-cloudwatch-agent-ctl -a stop`.  
2. **Reconfigure** via the **wizard** or by **pulling from Parameter Store/S3**.  
3. **Start** the agent with the new config, and **verify** it’s running.  

Following these steps ensures you cleanly stop and then restart the CloudWatch Agent with your updated configuration.