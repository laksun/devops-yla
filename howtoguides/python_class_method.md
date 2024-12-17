Below is an example of how you can implement a class with a class method `get_endpoint()` that looks up the correct endpoint based on the given environment. The method ignores case sensitivity by normalizing the environment string before performing the lookup.

```python
class EndpointManager:
    ENDPOINTS = {
        'development': 'http://localhost:5000/api',
        'staging': 'https://staging.example.com/api',
        'production': 'https://api.example.com',
    }

    @classmethod
    def get_endpoint(cls, environment: str) -> str:
        # Normalize the environment to lowercase to ensure case-insensitive lookup
        normalized_env = environment.lower() if environment else ''
        return cls.ENDPOINTS.get(normalized_env, cls.ENDPOINTS['production'])


# Example usage:
print(EndpointManager.get_endpoint('DEVELOPMENT'))  # http://localhost:5000/api
print(EndpointManager.get_endpoint('StAgInG'))       # https://staging.example.com/api
print(EndpointManager.get_endpoint('ProDucTion'))    # https://api.example.com
print(EndpointManager.get_endpoint('Unknown'))       # https://api.example.com (default)
```

# Check errors

Below is an updated version of the `EndpointManager` class that includes both type and value error handling. It will:

- Raise a `TypeError` if `environment` is not a string.
- Raise a `ValueError` if `environment` is an empty string or not a known environment.
- Perform a case-insensitive lookup by converting `environment` to lowercase.

```python
class EndpointManager:
    ENDPOINTS = {
        'development': 'http://localhost:5000/api',
        'staging': 'https://staging.example.com/api',
        'production': 'https://api.example.com',
    }

    @classmethod
    def get_endpoint(cls, environment):
        # Check type: ensure environment is a string
        if not isinstance(environment, str):
            raise TypeError(f"Expected environment to be a string, got {type(environment).__name__} instead.")
        
        # Normalize and verify environment
        normalized_env = environment.strip().lower()
        if not normalized_env:
            raise ValueError("Environment cannot be empty.")
        
        # Ensure environment is one of the known keys
        if normalized_env not in cls.ENDPOINTS:
            raise ValueError(
                f"Unknown environment '{environment}'. "
                f"Available environments are: {', '.join(cls.ENDPOINTS.keys())}."
            )

        return cls.ENDPOINTS[normalized_env]


# Example usage:
try:
    print(EndpointManager.get_endpoint('DEVELOPMENT'))  # http://localhost:5000/api
    print(EndpointManager.get_endpoint('UnknownEnv'))    # Will raise ValueError
except (TypeError, ValueError) as e:
    print(f"Error: {e}")

try:
    print(EndpointManager.get_endpoint(None))  # Will raise TypeError
except (TypeError, ValueError) as e:
    print(f"Error: {e}")
```