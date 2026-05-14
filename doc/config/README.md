# Config Integration Examples

This folder contains integrated Python config modules and runnable examples.

## What is integrated

- `doc/config/framework_config.py`: singleton config source
- `doc/config/config_reader.py`: required/optional key access
- `doc/config/property_file_reader.py`: token resolver (`config:`, `faker:`, `user:`)
- `doc/config/faker_utils.py`: random test data
- `doc/config/integration.py`: one bundle that wires all of the above

## Quick run

```powershell
python run_config_integration_example.py
```

## Behave example (no browser required)

```powershell
behave features/config-integration/config_integration.feature
```

The feature uses the `@config_only` tag so `features/environment.py` skips WebDriver startup.

## Login example (integrated config tokens)

Run a tiny local login-credentials demo:

```powershell
python run_login_config_example.py
```

Run a real Behave login scenario that resolves `user:` tokens before calling the login page object:

```powershell
behave features/config-integration/config_login_with_tokens.feature
```
