from des_encryption import DESEncryption
from rotor_machine import RotorMachine


class HybridCryptosystem:

    def __init__(self):
        self.rotor_machine = RotorMachine()
        self.des = DESEncryption()
        self.E1 = None
        self.E2 = None
        self.D1 = None
        self.D2 = None

    def encrypt(self, M: str):
        """Encrypts the given plaintext using a hybrid cryptosystem consisting of a rotor machine and DES encryption.

        Args:
            M (str): The plaintext to encrypt.

        Returns:
            str: The encrypted ciphertext.

        Time complexity: O(n) where n is the length of the plaintext
        The rotor machine encryption and decryption operations have a time complexity of O(n)
        The DES encryption and decryption operations have a time complexity of O(1) since they operate on 64-bit blocks
        Therefore, the overall time complexity of the encryption and decryption processes is O(n) + O(k) where k is the number of rounds to each block
        """
        
        self._reset_variables()
        # 1. Encrypt using the rotor machine
        self.E1 = self.rotor_machine.encrypt(M)
        # 2. Encrypt the result using DES
        self.E2 = self.des.encrypt(self.E1)
        return self.E2  # Encrypted text

    def decrypt(self, M: str):
        """Decrypts the given ciphertext using a hybrid cryptosystem consisting of a rotor machine and DES encryption.

        Args:
            M (str): The ciphertext to decrypt.

        Returns:
            str: The decrypted plaintext.

        Time complexity: O(n) where n is the length of the ciphertext
        The DES decryption operation has a time complexity of O(1)
        The rotor machine decryption operation has a time complexity of O(n)
        Therefore, the overall time complexity of the decryption process is O(n) + O(k) where k is the number of rounds to each block
        """
        # 1. Decrypt using DES
        self.D1 = self.des.decrypt(M)
        # 2. Decrypt the result using the rotor machine
        self.D2 = self.rotor_machine.decrypt(self.D1)
        return self.D2  # Decrypted text

    def get_E1(self):
        if self.E1 is None:
            raise ValueError("E1 is not set.")
        return self.E1

    def get_E2(self):
        if self.E2 is None:
            raise ValueError("E2 is not set.")
        return self.E2

    def get_D1(self):
        if self.D1 is None:
            raise ValueError("D1 is not set.")
        return self.D1

    def get_D2(self):
        if self.D2 is None:
            raise ValueError("D2 is not set.")
        return self.D2

    def _reset_variables(self):
        self.E1 = None
        self.E2 = None
        self.D1 = None
        self.D2 = None


if __name__ == "__main__":
    hybrid_crypto = HybridCryptosystem()
    plaintext = "This is the hybrid cryptosystem test."
    encrypted_text = hybrid_crypto.encrypt(plaintext)
    decrypted_text = hybrid_crypto.decrypt(encrypted_text)

    print(f"Plaintext: {plaintext}")
    print(f"Encrypted Text: {encrypted_text}")
    print(f"Decrypted Text: {decrypted_text}")
