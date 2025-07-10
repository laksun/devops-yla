Here’s a complete example of using **Flask with AWS Lambda via API Gateway** using the `awsgi` package. This example handles a **POST request**, parses the `body` and `requestContext`, and returns a response.

---

### ✅ 1. Lambda Function (Python) with Flask and `awsgi`

```python
# lambda_function.py
from flask import Flask, request, jsonify
import awsgi

app = Flask(__name__)

@app.route("/process", methods=["POST"])
def process_post():
    data = request.get_json()
    request_context = request.environ.get("awsgi.event", {}).get("requestContext", {})

    user_agent = request.headers.get("User-Agent")
    source_ip = request_context.get("identity", {}).get("sourceIp", "unknown")
    path = request.path

    return jsonify({
        "message": "Data received successfully.",
        "received_data": data,
        "request_info": {
            "source_ip": source_ip,
            "user_agent": user_agent,
            "path": path
        }
    })

def lambda_handler(event, context):
    return awsgi.response(app, event, context)
```

---

### ✅ 2. Sample Event (Payload from API Gateway) for Testing

This is how API Gateway sends data when triggering a POST:

```json
{
  "resource": "/process",
  "path": "/process",
  "httpMethod": "POST",
  "headers": {
    "Content-Type": "application/json",
    "User-Agent": "PostmanRuntime/7.28.4"
  },
  "requestContext": {
    "resourcePath": "/process",
    "httpMethod": "POST",
    "identity": {
      "sourceIp": "192.168.1.1",
      "userAgent": "PostmanRuntime/7.28.4"
    }
  },
  "body": "{\"name\": \"Alice\", \"email\": \"alice@example.com\"}",
  "isBase64Encoded": false
}
```

---

### ✅ 3. Explanation of How It Works

* `request.get_json()` — extracts the JSON body from the POST request.
* `request.environ.get("awsgi.event")` — gives you access to the original AWS Lambda `event` for headers, requestContext, etc.
* `request.headers.get("User-Agent")` — standard way to extract headers.
* `request_context["identity"]["sourceIp"]` — gives you the caller's IP address.

---

### ✅ 4. Example Response from the Lambda Function

```json
{
  "message": "Data received successfully.",
  "received_data": {
    "name": "Alice",
    "email": "alice@example.com"
  },
  "request_info": {
    "source_ip": "192.168.1.1",
    "user_agent": "PostmanRuntime/7.28.4",
    "path": "/process"
  }
}
```

---

Would you like a version that runs locally for testing with `sam local invoke` or `flask run` as well?
