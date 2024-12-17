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