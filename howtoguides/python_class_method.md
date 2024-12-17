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


# enhanced data structure

Below is an enhanced version of the `EndpointManager` class that stores both an endpoint and a client_id for each environment. The `get_environment_config()` class method returns both values together in a single dictionary. The method still includes type and value checks and is case-insensitive.

```python
class EndpointManager:
    ENV_CONFIG = {
        'development': {
            'endpoint': 'http://localhost:5000/api',
            'client_id': 'dev-client-id-123'
        },
        'staging': {
            'endpoint': 'https://staging.example.com/api',
            'client_id': 'staging-client-id-456'
        },
        'production': {
            'endpoint': 'https://api.example.com',
            'client_id': 'prod-client-id-789'
        }
    }

    @classmethod
    def get_environment_config(cls, environment):
        # Check type: ensure environment is a string
        if not isinstance(environment, str):
            raise TypeError(f"Expected environment to be a string, got {type(environment).__name__} instead.")
        
        # Normalize and verify environment
        normalized_env = environment.strip().lower()
        if not normalized_env:
            raise ValueError("Environment cannot be empty.")
        
        # Ensure environment is one of the known keys
        if normalized_env not in cls.ENV_CONFIG:
            raise ValueError(
                f"Unknown environment '{environment}'. "
                f"Available environments are: {', '.join(cls.ENV_CONFIG.keys())}."
            )

        # Return the entire configuration dictionary for the environment
        return cls.ENV_CONFIG[normalized_env]


# Example usage:
try:
    config = EndpointManager.get_environment_config('DEVELOPMENT')
    print(config)
    # Output: {'endpoint': 'http://localhost:5000/api', 'client_id': 'dev-client-id-123'}
except (TypeError, ValueError) as e:
    print(f"Error: {e}")
```

## Access endpoints

Once you have the environment configuration dictionary from `get_environment_config()`, you can simply index into it to access the endpoint value. For example:

```python
config = EndpointManager.get_environment_config('DEVELOPMENT')
endpoint = config['endpoint']
print(endpoint)  
# Output: http://localhost:5000/api
```

In this snippet, `config` is a dictionary returned by `get_environment_config()`, which looks something like:

```python
{
    'endpoint': 'http://localhost:5000/api',
    'client_id': 'dev-client-id-123'
}
```

You can directly use `config['endpoint']` to get just the endpoint.

## Test methods

Below is an example of how you might write unit tests for the `get_environment_config()` method using Python’s built-in `unittest` framework. These tests cover various scenarios:

- **Valid environment**: Ensure it returns the expected dictionary.
- **Non-string environment**: Ensure it raises a `TypeError`.
- **Empty environment**: Ensure it raises a `ValueError`.
- **Unknown environment**: Ensure it raises a `ValueError`.
  
```python
import unittest

class TestEndpointManager(unittest.TestCase):
    def test_valid_environment(self):
        config = EndpointManager.get_environment_config('development')
        self.assertIsInstance(config, dict)
        self.assertIn('endpoint', config)
        self.assertIn('client_id', config)
        self.assertEqual(config['endpoint'], 'http://localhost:5000/api')
        self.assertEqual(config['client_id'], 'dev-client-id-123')
        
        # Test a different environment (case-insensitive)
        config = EndpointManager.get_environment_config('StAgInG')
        self.assertEqual(config['endpoint'], 'https://staging.example.com/api')
        self.assertEqual(config['client_id'], 'staging-client-id-456')
        
    def test_non_string_environment(self):
        with self.assertRaises(TypeError):
            EndpointManager.get_environment_config(None)
        with self.assertRaises(TypeError):
            EndpointManager.get_environment_config(123)

    def test_empty_environment(self):
        with self.assertRaises(ValueError):
            EndpointManager.get_environment_config('')
        with self.assertRaises(ValueError):
            EndpointManager.get_environment_config('   ')

    def test_unknown_environment(self):
        with self.assertRaises(ValueError):
            EndpointManager.get_environment_config('unknown')
        with self.assertRaises(ValueError):
            EndpointManager.get_environment_config('devprod')

if __name__ == '__main__':
    unittest.main()
```

**What’s Happening in Each Test:**

- **`test_valid_environment`**:  
  Checks that a known environment (e.g., `'development'`) returns a dictionary with the expected keys and values. Also tests case-insensitive input (`'StAgInG'`).

- **`test_non_string_environment`**:  
  Ensures that passing a non-string value raises `TypeError`.

- **`test_empty_environment`**:  
  Ensures that passing an empty or whitespace-only string raises `ValueError`.

- **`test_unknown_environment`**:  
  Ensures that passing an environment that isn’t in `ENV_CONFIG` raises `ValueError`.

These tests should be run in an environment where the `EndpointManager` class is defined and can be imported.