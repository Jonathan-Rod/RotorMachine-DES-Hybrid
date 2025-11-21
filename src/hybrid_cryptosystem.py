from des_encryption import DESEncryption
from rotor_machine import RotorMachine


class HybridCryptosystem:
    """
    Implements a two-layer hybrid cryptographic system.

    It combines the stream cipher characteristics of a RotorMachine (Layer 1)
    with the block cipher strength of DESEncryption (Layer 2) for enhanced security.
    Encryption flow: Plaintext -> RotorMachine -> DESEncryption -> Ciphertext (M -> E1 -> E2).
    Decryption flow (Inverse Key): Ciphertext -> DESEncryption -> RotorMachine -> Plaintext (M -> D1 -> D2).
    """

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

    """
    Retrieves one of the intermediate results (E1, E2, D1, or D2) from the last
    encryption or decryption operation.

    Raises:
        ValueError: If the corresponding intermediate variable has not been set
                (i.e., if encrypt() or decrypt() has not been called).

    Returns:
        str: The stored intermediate result string.
    """

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
        """
        Resets all intermediate encryption (E1, E2) and decryption (D1, D2) state variables to None.
        This ensures that data from a previous operation is cleared before a new operation begins.
        """
        self.E1 = None
        self.E2 = None
        self.D1 = None
        self.D2 = None
