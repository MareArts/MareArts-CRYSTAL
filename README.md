# MareArts Crystal 🔐

[![PyPI](https://img.shields.io/pypi/v/marearts-crystal.svg)](https://pypi.org/project/marearts-crystal/)
[![Python versions](https://img.shields.io/pypi/pyversions/marearts-crystal.svg)](https://pypi.org/project/marearts-crystal/)
[![Downloads](https://pepy.tech/badge/marearts-crystal)](https://pepy.tech/project/marearts-crystal)
[![License](https://img.shields.io/pypi/l/marearts-crystal.svg)](https://github.com/MareArts/marearts-crystal/blob/main/LICENSE)
[![Status](https://img.shields.io/pypi/status/marearts-crystal.svg)](https://pypi.org/project/marearts-crystal/)

High-performance encryption library for Python - Simple, Secure, Compatible.

**Part of the [MareArts AI Package Family](https://marearts.com) 🚀**

## 🚀 Installation

```bash
pip install marearts-crystal
```

**System Requirements:**
- Python 3.9, 3.10, 3.11, 3.12
- Works on Windows, macOS, and Linux
- Dependencies: cryptography (automatically installed)

## Quick Start

```python
from marearts_crystal import ma_crystal

# Initialize
mask = ma_crystal("your-secret-key")

# Encrypt data
data = b"Sensitive information"
encrypted = mask.encrypt_data(data)
decrypted = mask.decrypt_data(encrypted)

# Generate serial key
serial_key = mask.generate_serial_key("user@email.com", "2025-09-10", "2025-12-31")
valid = mask.validate_serial_key("user@email.com", serial_key)
```

## Core Features

### 🔑 License Key Management

```python
from marearts_crystal import ma_crystal

mask = ma_crystal("your-company-secret")

# Generate license key
today = mask.get_today_date()
expire = mask.generate_end_date(years=1)  # 1 year license
license_key = mask.generate_serial_key("customer@email.com", today, expire)

print(f"License Key: {license_key}")

# Validate license
result = mask.validate_serial_key("customer@email.com", license_key)
if result:
    start_date, end_date = result
    if mask.validate_date(start_date, end_date):
        print("✅ License is active")
    else:
        print("❌ License expired")
```

### 🔐 File Encryption

```python
# Encrypt a file
with open("screen.png", "rb") as f:
    file_data = f.read()

encrypted = mask.encrypt_data(file_data)

with open("screen.png.enc", "wb") as f:
    f.write(encrypted)

# Decrypt a file
with open("screen.png.enc", "rb") as f:
    encrypted_data = f.read()

decrypted = mask.decrypt_data(encrypted_data)

with open("screen_decrypted.png", "wb") as f:
    f.write(decrypted)
```

### 📝 Config Encryption

```python
import json
from marearts_crystal import ma_crystal

mask = ma_crystal("app-secret-key")

# Save encrypted config
config = {
    "api_key": "secret-api-key",
    "database": "postgresql://localhost/mydb",
    "debug": False
}

encrypted_config = mask.encrypt_string(json.dumps(config))
with open("config.enc", "w") as f:
    f.write(encrypted_config)

# Load encrypted config
with open("config.enc", "r") as f:
    encrypted = f.read()

decrypted = mask.decrypt_string(encrypted)
config = json.loads(decrypted)
print(config)
```

## Practical Examples

### Software Licensing System

```python
from marearts_crystal import ma_crystal
from datetime import datetime

class LicenseManager:
    def __init__(self, secret_key):
        self.mask = ma_crystal(secret_key)
    
    def create_license(self, email, license_type="standard"):
        today = self.mask.get_today_date()
        
        if license_type == "trial":
            end_date = self.mask.generate_end_date(days=30)
        elif license_type == "standard":
            end_date = self.mask.generate_end_date(years=1)
        elif license_type == "premium":
            end_date = self.mask.generate_end_date(years=3)
        else:  # lifetime
            end_date = "2099-12-31"
        
        return self.mask.generate_serial_key(email, today, end_date)
    
    def verify_license(self, email, license_key):
        result = self.mask.validate_serial_key(email, license_key)
        if not result:
            return False, "Invalid license key"
        
        start_date, end_date = result
        if self.mask.validate_date(start_date, end_date):
            days_left = (datetime.strptime(end_date, "%Y-%m-%d") - datetime.now()).days
            return True, f"Valid until {end_date} ({days_left} days remaining)"
        else:
            return False, f"License expired on {end_date}"

# Usage
lm = LicenseManager("company-secret-2024")

# Create licenses
trial_key = lm.create_license("trial@user.com", "trial")
premium_key = lm.create_license("premium@user.com", "premium")

# Verify licenses
valid, message = lm.verify_license("premium@user.com", premium_key)
print(message)
```

### Secure Password Storage

```python
from marearts_crystal import ma_crystal

class PasswordVault:
    def __init__(self, master_password):
        self.mask = ma_crystal(master_password)
    
    def store_password(self, service, username, password):
        data = f"{service}|{username}|{password}"
        return self.mask.encrypt_string(data)
    
    def get_password(self, encrypted_data):
        decrypted = self.mask.decrypt_string(encrypted_data)
        if decrypted:
            service, username, password = decrypted.split("|")
            return {"service": service, "username": username, "password": password}
        return None

# Usage
vault = PasswordVault("master-password-123")

# Store credentials
encrypted = vault.store_password("GitHub", "john_doe", "ghp_secrettoken123")
print(f"Encrypted: {encrypted[:50]}...")

# Retrieve credentials
credentials = vault.get_password(encrypted)
print(f"Service: {credentials['service']}")
print(f"Username: {credentials['username']}")
```

### Batch File Encryption

```python
import os
from marearts_crystal import ma_crystal

def encrypt_folder(folder_path, secret_key):
    mask = ma_crystal(secret_key)
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.enc'):
            continue  # Skip already encrypted files
            
        filepath = os.path.join(folder_path, filename)
        
        # Read file
        with open(filepath, 'rb') as f:
            data = f.read()
        
        # Encrypt
        encrypted = mask.encrypt_data(data)
        
        # Save encrypted file
        with open(f"{filepath}.enc", 'wb') as f:
            f.write(encrypted)
        
        # Remove original (optional)
        os.remove(filepath)
        print(f"✅ Encrypted: {filename}")

# Usage
encrypt_folder("/path/to/sensitive/documents", "folder-secret-key")
```

## API Reference

### Basic Methods

| Method | Description | Example |
|--------|-------------|---------|
| `generate_serial_key(username, start_date, end_date)` | Generate a license key | `key = mask.generate_serial_key("user", "2025-09-10", "2025-12-31")` |
| `validate_serial_key(username, serial_key)` | Validate a license key | `result = mask.validate_serial_key("user", key)` |
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

## Security Features

- ✅ **Automatic V2 Encryption** - New operations use enhanced security
- ✅ **100% Backward Compatible** - Old encrypted data still works
- ✅ **Rate Limiting** - Built-in brute force protection
- ✅ **Binary Compilation** - Cython compilation hides implementation
- ✅ **Input Validation** - Comprehensive input checking

## 🔗 MareArts AI Package Family

MareArts Crystal is part of our comprehensive AI and utility package ecosystem:

| Package | Description | Use Case |
|---------|-------------|----------|
| **[marearts-anpr](https://github.com/MareArts/MareArts-ANPR)** 🚗 | License Plate Recognition | Vehicle identification, parking systems, traffic monitoring |
| **[marearts-road-objects](https://github.com/MareArts/MareArts-Road-Objects)** 🛣️ | Road Object Detection | Traffic analysis, smart city applications, safety systems |
| **[marearts-crystal](https://github.com/MareArts/marearts-crystal)** 🔐 | Encryption & Licensing | Software licensing, data security, key management |

### Why Choose MareArts Packages?

- **🏆 Professional Grade**: Production-ready solutions
- **⚡ High Performance**: Optimized for speed and efficiency  
- **🔧 Easy Integration**: Simple APIs, comprehensive documentation
- **🌍 Cross-Platform**: Windows, macOS, Linux support
- **📦 Complete Ecosystem**: Packages work seamlessly together

**Explore More**: Visit [marearts.com](https://marearts.com) for complete solutions and enterprise licensing.

---

## 📞 Support & Contact

- **Documentation**: [marearts.com/docs](https://marearts.com/docs)
- **Issues**: [GitHub Issues](https://github.com/MareArts/marearts-crystal/issues)
- **Business Inquiries**: [contact@marearts.com](mailto:contact@marearts.com)
- **Website**: [marearts.com](https://marearts.com)

## 📄 License

MIT License - Free for commercial and personal use.

---

<div align="center">

**Made with ❤️ by [MareArts](https://marearts.com)**

*Empowering developers with AI-powered solutions*

[![Visit MareArts.com](https://img.shields.io/badge/Visit-MareArts.com-blue?style=for-the-badge&logo=google-chrome)](https://marearts.com)

</div>
# MareArts-CRYSTAL
