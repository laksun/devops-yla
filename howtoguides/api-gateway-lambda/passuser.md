To pass user roles and user ID from a **Lambda authorizer** to your **backend API**, you can embed these details into the **`context`** object in the **Lambda authorizer's response**, and then access them in your **backend** via **custom headers** (e.g., `event.requestContext.authorizer` in API Gateway).

---

### ✅ Overview

1. **Lambda Authorizer (Node.js)**: Verify the user, determine their roles/user ID, and return them via the `context` object.
2. **API Gateway**: Automatically injects the `context` values as headers into the `event.requestContext.authorizer` for your backend.
3. **Backend API (Python)**: Access `authorizer` context data from the `event` object (if using Lambda) or from HTTP headers (if a regular web server).

---

## 🧠 Step-by-Step

---

### 1. ✅ Lambda Authorizer in Node.js

```js
exports.handler = async (event) => {
    const token = event.authorizationToken;

    // Validate the token (JWT or custom) and extract user info
    const decoded = verifyToken(token);  // Your function
    const userId = decoded.sub;
    const roles = decoded.roles;  // E.g., ['admin', 'editor']

    return {
        principalId: userId,
        policyDocument: {
            Version: '2012-10-17',
            Statement: [
                {
                    Action: 'execute-api:Invoke',
                    Effect: 'Allow',
                    Resource: event.methodArn
                }
            ]
        },
        context: {
            userId: userId,
            roles: roles.join(',')  // Send as comma-separated string
        }
    };
};
```

* `context.userId` and `context.roles` are injected into the `requestContext.authorizer` object in downstream APIs.

---

### 2. ✅ API Gateway Configuration

Nothing special needed if you return `context` — API Gateway will add this under:

```json
event.requestContext.authorizer.userId
event.requestContext.authorizer.roles
```

---

### 3. ✅ Backend Python (Lambda or Flask-style)

#### Option A: If backend is an AWS Lambda

```python
def handler(event, context):
    authorizer = event['requestContext']['authorizer']
    user_id = authorizer.get('userId')
    roles = authorizer.get('roles', '').split(',')

    # Your logic here
    return {
        "statusCode": 200,
        "body": json.dumps({
            "user_id": user_id,
            "roles": roles
        })
    }
```

#### Option B: If backend is an HTTP service behind API Gateway (e.g., Flask)

API Gateway will map the `context` into HTTP headers using the format:

```
x-authorizer-userid
x-authorizer-roles
```

Use middleware to extract them:

```python
from flask import request

@app.route('/example', methods=['GET'])
def example():
    user_id = request.headers.get('x-authorizer-userid')
    roles = request.headers.get('x-authorizer-roles', '').split(',')

    return jsonify({
        "user_id": user_id,
        "roles": roles
    })
```

---

## 🛠️ Tips

* **Avoid large data** in `context` — there's a 6 KB limit.
* Use `roles.join(',')` to simplify transmission of array-like data.
* Always sanitize/validate input from `authorizer`.

---

If you're using **Terraform or AWS Console**, ensure your API Gateway **Integration Request** has `Use Lambda Proxy Integration = true`, so all headers and context pass automatically.

Let me know if you're using HTTP API or REST API — implementation details differ slightly.
