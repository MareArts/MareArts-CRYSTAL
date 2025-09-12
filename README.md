# MareArts Crystal

[![PyPI](https://img.shields.io/pypi/v/marearts-crystal.svg)](https://pypi.org/project/marearts-crystal/)
[![Python versions](https://img.shields.io/pypi/pyversions/marearts-crystal.svg)](https://pypi.org/project/marearts-crystal/)
[![Downloads](https://pepy.tech/badge/marearts-crystal)](https://pepy.tech/project/marearts-crystal)
[![License](https://img.shields.io/pypi/l/marearts-crystal.svg)](https://github.com/MareArts/marearts-crystal/blob/main/LICENSE)

Professional encryption library for Python applications. Secure your software licenses, encrypt sensitive files, and protect user data with military-grade encryption.

**What is this?** A tool that lets you encrypt (lock) and decrypt (unlock) data using secret keys, like a digital safe that only you can open.

**Use Cases:**
- 🔐 **Software Licensing** - Generate and validate license keys for your applications
- 📁 **File Protection** - Encrypt sensitive documents, images, or any files
- 🔑 **Password Management** - Securely store passwords and credentials
- ⚙️ **Config Security** - Protect API keys and database credentials in config files
- 📊 **Data Privacy** - Encrypt user data for GDPR/HIPAA compliance

**Why MareArts Crystal?**
- **Zero Setup** - Pre-compiled for all platforms, just `pip install` and use
- **Production Ready** - Used by companies for real-world applications
- **Fast** - C++ performance with Python simplicity

## Installation

```bash
pip install marearts-crystal
```

Requirements: Python 3.9-3.12, Windows/macOS/Linux

## Quick Start

### License Key Generation

```python
from marearts_crystal import ma_crystal

mask = ma_crystal("your-company-secret")

# Generate license key with signature
today = mask.get_today_date()  # "2025-09-12"
expire = mask.generate_end_date(years=1)  # "2026-09-12"
license_key, signature = mask.generate_serial_key("customer@email.com", today, expire)

print(f"License Key: {license_key}")
# Output: License Key: MAEV2:gAAAAABow91CXuG7dJR3eAWpEXj67RP-qboPAHiDGpVfd2dGN5yBXp...

print(f"Signature: {signature}")
# Output: Signature: a21521da5beb6d7c

# Validate license
result = mask.validate_serial_key("customer@email.com", license_key)
if result:
    start_date, end_date, signature = result
    # start_date = "2025-09-12", end_date = "2026-09-12", signature = "a21521da5beb6d7c"
    if mask.validate_date(start_date, end_date):
        print(f"✅ License active until {end_date}")
        # Output: ✅ License active until 2026-09-12
```

```python
# Using signature for tracking
license_db = {}  # Your database

# Store license with signature
license_key, signature = mask.generate_serial_key("user@email.com", today, expire)
license_db[signature] = {
    "email": "user@email.com",
    "key": license_key,
    "created": today
}

# Later, verify and track
result = mask.validate_serial_key("user@email.com", license_key)
if result:
    start, end, sig = result
    print(f"License {sig} is valid")  # Use signature as ID
```

### File Encryption

```python
# Encrypt file
with open("document.pdf", "rb") as f:
    file_data = f.read()  # Read original file (e.g., 241979 bytes)

encrypted = mask.encrypt_data(file_data)
print(f"Encrypted size: {len(encrypted)} bytes")
# Output: Encrypted size: 322724 bytes

with open("document.pdf.enc", "wb") as f:
    f.write(encrypted)

# Decrypt file
with open("document.pdf.enc", "rb") as f:
    encrypted_data = f.read()

decrypted = mask.decrypt_data(encrypted_data)
print(f"Decrypted size: {len(decrypted)} bytes")
# Output: Decrypted size: 241979 bytes (matches original)

with open("document_decrypted.pdf", "wb") as f:
    f.write(decrypted)
print("✅ File successfully decrypted")
# Output: ✅ File successfully decrypted
```

## More Examples

### Python Examples ([View on GitHub](https://github.com/MareArts/marearts-crystal/tree/main/examples))
- License key generation and validation
- File encryption/decryption  
- Config file encryption
- License manager class implementation
- Password vault implementation
- All API methods demonstration

### Jupyter Notebook ([Interactive Tutorial](https://github.com/MareArts/marearts-crystal/blob/main/examples/examples.ipynb))
- Interactive step-by-step tutorial
- Visual output of each operation
- Real-time testing environment

## API Reference

### Basic Methods

| Method | Description | Example |
|--------|-------------|---------|
| `generate_serial_key(username, start_date, end_date)` | Generate a license key with signature | `key, signature = mask.generate_serial_key("user", "2025-09-10", "2025-12-31")` |
| `validate_serial_key(username, serial_key)` | Validate a license key | `result = mask.validate_serial_key("user", key)` # Returns (start_date, end_date, signature) |
| `encrypt_string(text)` | Encrypt text | `encrypted = mask.encrypt_string("secret")` |
| `decrypt_string(encrypted)` | Decrypt text | `text = mask.decrypt_string(encrypted)` |
| `encrypt_data(bytes)` | Encrypt binary data | `encrypted = mask.encrypt_data(b"data")` |
| `decrypt_data(encrypted)` | Decrypt binary data | `data = mask.decrypt_data(encrypted)` |

### Utility Methods

| Method | Description | Example |
|--------|-------------|---------|
| `get_today_date()` | Get today's date (YYYY-MM-DD) | `today = mask.get_today_date()` |
| `generate_end_date(years, months, days)` | Calculate future date | `expire = mask.generate_end_date(years=1)` |
| `validate_date(start, end)` | Check if current date is in range | `valid = mask.validate_date("2025-09-10", "2025-12-31")` |
| `is_v2_serial_key(key)` | Check if key uses V2 format | `is_v2 = mask.is_v2_serial_key(key)` |
| `is_v2_data(data)` | Check if data uses V2 encryption | `is_v2 = mask.is_v2_data(data)` |
| `string_to_secret_key(input_string)` | Derive key from string | `key = mask.string_to_secret_key("password")` |
| `secret_key_to_string(secret_key, encrypted)` | Decrypt with provided key | `text = mask.secret_key_to_string(key, encrypted)` |


## Support

- **Email**: hello@marearts.com
- **Website**: [marearts.com](https://marearts.com)

## License

MIT License
