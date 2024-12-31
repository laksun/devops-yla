Below is an example of how you might write a pytest test for the exception handling in `my_access_token` using mocks. The key points are:

- We use `unittest.mock.patch` to simulate an exception in one of the calls inside the `try` block.  
- We capture logs with `caplog` to ensure the error message is logged.  
- We verify that the exception is indeed propagated (i.e., re-raised).

> **Note**: Make sure to replace `path.to` with the correct import paths for your actual module structure.  

```python
import pytest
import logging
from unittest.mock import patch, MagicMock

from your_module import MyApp  # adjust import path to your MyApp class


@pytest.mark.parametrize("environment", ["dev", "test", "prod"])
def test_myapp_my_access_token_exception_handling(caplog, environment):
    """
    Test that an exception raised inside the my_access_token property
    is logged and then re-raised.
    """
    # Instantiate MyApp. Note that _token is left as None,
    # so the logic in my_access_token attempts to get a token.
    app = MyApp(environment=environment)

    # We mock AWSTokenProvider.get_identity_assertion so it raises an Exception
    with patch("path.to.AWSTokenProvider.get_identity_assertion", side_effect=Exception("Mocked exception")):
        # We expect the exception to propagate up
        with pytest.raises(Exception, match="Mocked exception"):
            # Accessing the property triggers the code in my_access_token
            _ = app.my_access_token

    # Verify that the error message was logged
    assert any("Token not retrieved - Mocked exception" in message for message in caplog.text.splitlines())
```

### Explanation

1. **Parameterize environments**  
   We use `pytest.mark.parametrize("environment", ["dev", "test", "prod"])` to ensure the test logic works for each of those environments. Adjust as needed for your actual environment strings (e.g., `"local"`, `"dev"`, `"test"`, `"prod"`).

2. **`caplog` fixture**  
   The [caplog](https://docs.pytest.org/en/stable/how-to/capture-logs.html#caplog-fixture) fixture is used to capture log messages, so we can assert that the correct message was logged.

3. **Mocking**  
   - We mock `AWSTokenProvider.get_identity_assertion`. You could also mock any part of the chain that raises the exception, such as:
     - `EndpointManager.get_environment_config`
     - `AWSTokenProvider.__init__`
     - `token_provider.get_identity_assertion()`
     - `identity_assertion.get_access_token()`

   - We set `side_effect=Exception("Mocked exception")` to simulate a failure.

4. **Exception Verification**  
   - We wrap the property access (`app.my_access_token`) in `pytest.raises(Exception, match="Mocked exception")` to confirm the exact exception is raised with our custom message.

5. **Log Message Verification**  
   - We assert the presence of `Token not retrieved - Mocked exception` in the captured log output.

With this setup, you’re ensuring that your error handling code path is tested: the exception occurs, it’s logged, and it’s re-raised so that the caller is aware of the problem.