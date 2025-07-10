Great question!

### 🔍 Does Flask (`awsgi`) Expect `queryStringParameters` in the API Gateway Payload?

**Short Answer:**
**No**, Flask itself doesn’t expect or directly access `queryStringParameters` — but **`awsgi`** uses it internally to construct the correct `request.args` dictionary.

---

### 🔧 How It Works Under the Hood

* `awsgi` translates the **API Gateway event format** (including `queryStringParameters`) into a **WSGI-compatible environment**.
* Then, Flask accesses the query parameters via `request.args`, just like in a normal Flask app.

So if your API Gateway event includes:

```json
"queryStringParameters": {
  "user": "alice",
  "id": "123"
}
```

You can access it in your Flask route like this:

```python
from flask import request

@app.route("/example", methods=["GET"])
def example():
    user = request.args.get("user")
    user_id = request.args.get("id")
    return jsonify({"user": user, "id": user_id})
```

---

### 🧪 Example Payload with `queryStringParameters`

```json
{
  "resource": "/example",
  "path": "/example",
  "httpMethod": "GET",
  "queryStringParameters": {
    "user": "alice",
    "id": "123"
  },
  "requestContext": {
    "identity": {
      "sourceIp": "192.168.1.1"
    }
  },
  "headers": {
    "Content-Type": "application/json"
  },
  "isBase64Encoded": false
}
```

---

### ✅ Conclusion

* ✅ Yes, `queryStringParameters` should be present in the **API Gateway event payload** if you expect query strings.
* ✅ `awsgi` handles this for you and maps them to `request.args` in Flask.
* ❌ Flask doesn’t see `queryStringParameters` directly — only the result of it via `request.args`.

Would you like a full working Lambda test with both `queryStringParameters` and `body` in one payload?
