#!/usr/bin/env python3
"""
MareArts Crystal - README Examples
All examples from the README documentation
"""
import json
import tempfile
import os
from datetime import datetime

def example_quick_start():
    """Quick Start example from README"""
    print("=== Quick Start Example ===")
    
    from marearts_crystal import ma_crystal

    # Initialize
    mask = ma_crystal("your-secret-key")

    # Encrypt data
    data = b"Sensitive information"
    encrypted = mask.encrypt_data(data)
    decrypted = mask.decrypt_data(encrypted)
    
    print(f"Original: {data}")
    print(f"Encrypted: {encrypted[:50]}...")
    print(f"Decrypted: {decrypted}")
    print(f"Success: {decrypted == data}")

    # Generate serial key
    serial_key = mask.generate_serial_key("user@email.com", "2025-09-10", "2025-12-31")
    valid = mask.validate_serial_key("user@email.com", serial_key)
    
    print(f"\nSerial Key: {serial_key[:50]}...")
    print(f"Validation: {valid}")
    print("Quick Start completed successfully!\n")

def example_license_management():
    """License Key Management example from README"""
    print("=== License Key Management Example ===")
    
    from marearts_crystal import ma_crystal

    mask = ma_crystal("your-company-secret")

    # Generate license key
    today = mask.get_today_date()
    expire = mask.generate_end_date(years=1)  # 1 year license
    license_key = mask.generate_serial_key("customer@email.com", today, expire)

    print(f"Today: {today}")
    print(f"Expires: {expire}")
    print(f"License Key: {license_key[:50]}...")

    # Validate license
    result = mask.validate_serial_key("customer@email.com", license_key)
    if result:
        start_date, end_date = result
        if mask.validate_date(start_date, end_date):
            print("✅ License is active")
        else:
            print("❌ License expired")
    
    print("License Management completed successfully!\n")

def example_file_encryption():
    """File Encryption example from README"""
    print("=== File Encryption Example ===")
    
    from marearts_crystal import ma_crystal
    
    mask = ma_crystal("test-secret-key")
    
    # Create test files in temp directory
    with tempfile.TemporaryDirectory() as temp_dir:
        original_file = os.path.join(temp_dir, "document.pdf")
        encrypted_file = os.path.join(temp_dir, "document.pdf.enc")
        decrypted_file = os.path.join(temp_dir, "document_decrypted.pdf")
        
        # Create test data
        test_data = b"This is test PDF content for encryption demo"
        
        # Write original file
        with open(original_file, "wb") as f:
            f.write(test_data)
        
        # Encrypt a file
        with open(original_file, "rb") as f:
            file_data = f.read()

        encrypted = mask.encrypt_data(file_data)

        with open(encrypted_file, "wb") as f:
            f.write(encrypted)

        print(f"Original file size: {len(test_data)} bytes")
        print(f"Encrypted file size: {len(encrypted)} bytes")

        # Decrypt a file
        with open(encrypted_file, "rb") as f:
            encrypted_data = f.read()

        decrypted = mask.decrypt_data(encrypted_data)

        with open(decrypted_file, "wb") as f:
            f.write(decrypted)
        
        # Verify the decrypted file matches original
        with open(decrypted_file, "rb") as f:
            decrypted_data = f.read()
        
        print(f"Decryption success: {decrypted_data == test_data}")
    
    print("File Encryption completed successfully!\n")

def example_config_encryption():
    """Config Encryption example from README"""
    print("=== Config Encryption Example ===")
    
    from marearts_crystal import ma_crystal

    mask = ma_crystal("app-secret-key")

    # Save encrypted config
    config = {
        "api_key": "secret-api-key",
        "database": "postgresql://localhost/mydb",
        "debug": False
    }

    encrypted_config = mask.encrypt_string(json.dumps(config))
    
    with tempfile.TemporaryDirectory() as temp_dir:
        config_file = os.path.join(temp_dir, "config.enc")
        
        with open(config_file, "w") as f:
            f.write(encrypted_config)

        print(f"Original config: {config}")
        print(f"Encrypted config: {encrypted_config[:50]}...")

        # Load encrypted config
        with open(config_file, "r") as f:
            encrypted = f.read()

        decrypted = mask.decrypt_string(encrypted)
        loaded_config = json.loads(decrypted)
        
        print(f"Loaded config: {loaded_config}")
        print(f"Config matches: {loaded_config == config}")
    
    print("Config Encryption completed successfully!\n")

def example_license_manager_class():
    """LicenseManager class example from README"""
    print("=== LicenseManager Class Example ===")
    
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

    print(f"Trial key: {trial_key[:50]}...")
    print(f"Premium key: {premium_key[:50]}...")

    # Verify licenses
    valid, message = lm.verify_license("premium@user.com", premium_key)
    print(f"Premium license verification: {message}")
    
    print("LicenseManager Class completed successfully!\n")

def example_password_vault():
    """PasswordVault class example from README"""
    print("=== PasswordVault Example ===")
    
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
    print(f"Password: {credentials['password']}")
    
    print("PasswordVault completed successfully!\n")

def example_api_methods():
    """API methods example"""
    print("=== API Methods Example ===")
    
    from marearts_crystal import ma_crystal
    
    mask = ma_crystal("test-api-key")
    
    print("Testing all API methods:")
    
    # Test basic methods
    key = mask.generate_serial_key("user", "2025-09-10", "2025-12-31")
    result = mask.validate_serial_key("user", key)
    print(f"Serial key validation: {result is not None}")
    
    encrypted_str = mask.encrypt_string("secret")
    text = mask.decrypt_string(encrypted_str)
    print(f"String encryption: {text == 'secret'}")
    
    encrypted_data = mask.encrypt_data(b"data")
    data = mask.decrypt_data(encrypted_data)
    print(f"Data encryption: {data == b'data'}")
    
    # Test utility methods
    today = mask.get_today_date()
    print(f"Today's date: {today}")
    
    expire = mask.generate_end_date(years=1)
    print(f"Future date: {expire}")
    
    valid = mask.validate_date("2025-09-10", "2025-12-31")
    print(f"Date validation: {valid}")
    
    is_v2_key = mask.is_v2_serial_key(key)
    print(f"V2 serial key detection: {is_v2_key}")
    
    is_v2_data = mask.is_v2_data(encrypted_data)
    print(f"V2 data detection: {is_v2_data}")
    
    # Test additional methods
    derived_key = mask.string_to_secret_key("password")
    print(f"Key derivation: {isinstance(derived_key, str)}")
    
    print("All API methods completed successfully!\n")

def main():
    print("="*70)
    print("MAREARTS CRYSTAL - README EXAMPLES")
    print("="*70)
    
    examples = [
        example_quick_start,
        example_license_management,
        example_file_encryption,
        example_config_encryption,
        example_license_manager_class,
        example_password_vault,
        example_api_methods,
    ]
    
    print("Running all examples from README...\n")
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"❌ {example.__name__} failed: {e}\n")
    
    print("="*70)
    print("🎉 All examples completed! Check output above for results.")
    print("="*70)

if __name__ == "__main__":
    main()