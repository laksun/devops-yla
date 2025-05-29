# handler.py
import json
from ddb_repository import RoleConfigurationRepository
from validation import validate_payload, ROLE_SCHEMA

repo = RoleConfigurationRepository()

def lambda_handler(event, context):
    method = event["httpMethod"]
    path_params = event.get("pathParameters") or {}
    body = json.loads(event.get("body") or "{}")

    if method == "GET":
        role_id = path_params.get("roleId")
        if role_id:
            item = repo.get_role(role_id)
            return respond(200 if item else 404, item or {"message": "Not found"})
        else:
            return respond(200, repo.scan_roles())

    if method == "POST":
        validate_payload(body, operation="create")
        created = repo.put_role(body)
        return respond(201, created)

    if method == "PATCH":
        role_id = path_params.get("roleId")
        if not role_id:
            return respond(400, {"message": "Missing roleId in path"})
        validate_payload(body, operation="update")
        updated = repo.update_role(role_id, body)
        return respond(200, updated)

    return respond(405, {"message": "Method Not Allowed"})

def respond(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }
