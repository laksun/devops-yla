Below is a minimal example of how to assume an AWS IAM role using `boto3` and then produce session credentials for it. After you have these temporary credentials, you can use them to create a new session and interact with various AWS services under the assumed role.

---

## 1. Basic Example with `sts.assume_role`

```python
import boto3

def assume_role_and_get_session(role_arn, session_name="mySession", duration_seconds=3600):
    """
    Assume the specified IAM role and return a new boto3 Session
    using temporary credentials.
    
    :param role_arn: The ARN of the role to assume (str).
    :param session_name: A name for the session, unique identifier (str).
    :param duration_seconds: The session duration in seconds (int).
    :return: A new boto3 Session object authenticated with the assumed role credentials.
    """
    sts_client = boto3.client('sts')

    # Assume the role
    response = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName=session_name,
        DurationSeconds=duration_seconds
    )
    
    # Extract temporary credentials
    temp_credentials = response['Credentials']
    access_key = temp_credentials['AccessKeyId']
    secret_key = temp_credentials['SecretAccessKey']
    session_token = temp_credentials['SessionToken']
    
    # Create a new session with the temporary credentials
    assumed_session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        aws_session_token=session_token
    )
    
    return assumed_session

if __name__ == "__main__":
    # Replace with your actual role ARN
    role_arn = "arn:aws:iam::123456789012:role/MyCrossAccountRole"
    
    # Assume the role
    session = assume_role_and_get_session(role_arn, session_name="ExampleSession")
    
    # Use the new session, for example, to list S3 buckets
    s3_client = session.client("s3")
    buckets = s3_client.list_buckets()
    print("Buckets under assumed role:")
    for bucket in buckets["Buckets"]:
        print(f"  {bucket['Name']}")
```

### Explanation

1. **Create STS Client**:  
   We first create a client for the **Security Token Service (STS)** via `boto3.client('sts')`.

2. **Assume Role**:  
   - We call `assume_role(...)` with the **Role ARN** we want to assume.  
   - We specify a **Role Session Name** (e.g., `"mySession"`) and a **DurationSeconds** (up to the maximum allowed by the role).

3. **Extract Temporary Credentials**:  
   The response from `sts.assume_role` contains temporary **AccessKeyId**, **SecretAccessKey**, and **SessionToken**, which we store in local variables.

4. **Create New Boto3 Session**:  
   We call `boto3.Session(...)` and pass in the temporary credentials. This new session is **scoped** to the assumed role, so any service clients created from it will operate under that role’s permissions.

5. **Use the Session**:  
   For example, we can create an S3 client using the new session and list buckets. The S3 calls will be made with the assumed role permissions.

---

## 2. Common Variations

- **Providing External ID**: If the role requires an external ID, you can include it:
  ```python
  response = sts_client.assume_role(
      RoleArn=role_arn,
      RoleSessionName=session_name,
      DurationSeconds=duration_seconds,
      ExternalId="some-external-id"
  )
  ```

- **Using the AWS CLI Profile**: If your environment uses profiles for cross-account access, you might not need to do an explicit `assume_role` in code. Instead, you could configure a named profile with a source profile and role ARN in `~/.aws/config`, then just do:
  ```python
  session = boto3.Session(profile_name="my_cross_account_profile")
  ```
  But that’s a different approach using AWS CLI’s built-in role assumption via config.

---

## 3. Troubleshooting Tips

- **Access Denied**: Ensure your **caller identity** (the entity calling `sts.assume_role`) has the `sts:AssumeRole` permission on the target role.
- **Role ARN vs. Role Name**: Remember, `sts.assume_role` expects the **full ARN** of the role, not just the name.  
- **Session Duration**: Some roles limit the **maximum session duration**. If you request a duration that exceeds that limit, you’ll receive an error.

That’s it! With these steps, you can confidently assume roles across AWS accounts or within the same account, and then use the returned credentials to make API calls with the appropriate permissions.
