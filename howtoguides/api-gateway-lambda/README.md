The error you're encountering in all your test cases is:

```
AttributeError: __name__
```

This error comes from this line in your Lambda `handler` function:

```python
print(f"DEBUG: Matched route: {method} {resource}, calling function: {route_func.__name__}")
```

When you use a `Mock()` (like in your test), it does **not** have a `__name__` attribute by default — hence the error.

---

### ✅ Fix #1: Use a `Mock` with a `__name__` Attribute

Update each test like this:

```python
mock_func = Mock()
mock_func.__name__ = "mocked_func"
index.routes[("GET", "/role_configurations")] = mock_func
```

Example in context:

```python
def test_get_role_configurations():
    mock_func = Mock()
    mock_func.__name__ = "mocked_get_role_configurations"
    index.routes[("GET", "/role_configurations")] = mock_func

    event = {"httpMethod": "GET", "resource": "/role_configurations"}
    context = {}

    index.handler(event, context)

    mock_func.assert_called_once_with(event)
```

Do this for **every test function** where you insert a mock into `routes`.

---

### ✅ Fix #2: Make the handler print statement more robust (optional)

You can also make the handler code more test-friendly:

```python
print(f"DEBUG: Matched route: {method} {resource}, calling function: {getattr(route_func, '__name__', str(route_func))}")
```

This would prevent crashes even if the function has no `__name__` (like mocks do).

---

### Summary

You need to **set `__name__` on your mocks** or make the production code more resilient. Fixing it in the test is better practice in this case since your real route functions do have `__name__`.

Would you like me to update all 7 test cases with the proper mock name fixes?
