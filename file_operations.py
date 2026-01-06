"""
File operations for VaultBurn: secure deletion, encryption, and decryption.
"""
import os
import logging
from cryptography.fernet import Fernet
from utils import human_size


def secure_delete(file_path, passes=3):
    """Securely delete a file with multiple overwrite passes and logging."""
    try:
        if not os.path.exists(file_path):
            logging.warning(f"File not found: {file_path}")
            return False
            
        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)
        
        logging.info(f"Starting secure deletion of '{file_name}' ({human_size(file_size)}) with {passes} passes")
        
        # Perform secure deletion
        for pass_num in range(1, passes + 1):
            random_data = os.urandom(file_size)
            with open(file_path, "wb") as f:
                f.write(random_data)
                f.flush()
                os.fsync(f.fileno())
            logging.debug(f"Completed overwrite pass {pass_num}/{passes} for '{file_name}'")
        
        os.remove(file_path)
        logging.info(f"Successfully deleted '{file_name}' - {human_size(file_size)} permanently destroyed")
        return True
        
    except PermissionError as e:
        logging.error(f"Permission denied deleting '{file_path}': {e}")
        return False
    except OSError as e:
        logging.error(f"OS error deleting '{file_path}': {e}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error deleting '{file_path}': {e}")
        return False


def generate_key():
    """Generate a secure encryption key."""
    return Fernet.generate_key()


def encrypt_file(file_path, key):
    """Encrypt a file using the provided key."""
    try:
        # Read the file
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
        # Create cipher
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(file_data)
        
        # Write encrypted file
        encrypted_path = file_path + '.encrypted'
        with open(encrypted_path, 'wb') as f:
            f.write(encrypted_data)
        
        logging.info(f"Successfully encrypted '{os.path.basename(file_path)}' -> '{os.path.basename(encrypted_path)}'")
        return encrypted_path
        
    except Exception as e:
        logging.error(f"Error encrypting '{file_path}': {e}")
        return None


def decrypt_file(encrypted_path, key, output_path=None):
    """Decrypt a file using the provided key."""
    try:
        # Read encrypted file
        with open(encrypted_path, 'rb') as f:
            encrypted_data = f.read()
        
        # Create cipher and decrypt
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data)
        
        # Determine output path
        if output_path is None:
            if encrypted_path.endswith('.encrypted'):
                output_path = encrypted_path[:-10]  # Remove .encrypted
            else:
                output_path = encrypted_path + '.decrypted'
        
        # Write decrypted file
        with open(output_path, 'wb') as f:
            f.write(decrypted_data)
        
        logging.info(f"Successfully decrypted '{os.path.basename(encrypted_path)}' -> '{os.path.basename(output_path)}'")
        return output_path
        
    except Exception as e:
        logging.error(f"Error decrypting '{encrypted_path}': {e}")
        return None
