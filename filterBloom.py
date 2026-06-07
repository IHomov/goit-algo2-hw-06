import hashlib

class BloomFilter:
    def __init__(self, size: int, num_hashes: int):
        self.size = size
        self.num_hashes = num_hashes
        # Use bytearray for memory efficiency — each element occupies only 1 byte
        self.bit_array = bytearray(size)

    def _hashes(self, item: str):
        """
        Generation of stable indices using MD5.
        Built-in hash() cannot be used due to salt randomization between runs.
        """
        for i in range(self.num_hashes):
            # Create a unique string for each hashing iteration
            encoded_item = f"{item}_{i}".encode('utf-8')
            # Get the numeric equivalent of the hash
            hash_digest = int(hashlib.md5(encoded_item).hexdigest(), 16)
            yield hash_digest % self.size

    def add(self, item: str):
        # Protect against incorrect data types or empty strings
        if not isinstance(item, str) or not item.strip():
            return
        
        for hash_index in self._hashes(item):
            self.bit_array[hash_index] = 1

    def check(self, item: str) -> bool:
        # Protect against incorrect data types or empty strings
        if not isinstance(item, str) or not item.strip():
            return False
            
        return all(self.bit_array[hash_index] == 1 for hash_index in self._hashes(item))


def check_password_uniqueness(bloom: BloomFilter, passwords: list) -> dict:
    results = {}
    
    # Protect against incorrect data types
    if not isinstance(passwords, list):
        return {}
   

    for password in passwords:
        # work with incorrect values (numbers, None, empty strings) according to the requirements
        if not isinstance(password, str) or not password.strip():
            results[str(password)] = "некоректне значення"
            continue
            
        if bloom.check(password):
            results[password] = "можливо існує"
        else:
            results[password] = "унікальний"
            
    return results


if __name__ == "__main__":
    # Initialization of the Bloom filter
    bloom = BloomFilter(size=1000, num_hashes=3)

    # Adding existing passwords
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    # Checking new passwords (including incorrect data for testing condition #3)
    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest", "", None, 12345]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    # Displaying results
    for password, status in results.items():
        print(f"Пароль '{password}' - {status}.")