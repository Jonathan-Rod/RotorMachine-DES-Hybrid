from des_generator import DesGenerator


class RotorMachine:
    # Note I am assuming rotors are length 128 for all ASCII characters
    def __init__(
        self,
        rotor1: list[str] = None,
        rotor2: list[str] = None,
        rotor3: list[str] = None,
    ):

        self.generator = DesGenerator()

        if rotor1 is None:
            self.rotor1_original = self.generator.random_all_ascii()
        else:
            self.rotor1_original = rotor1

        if rotor2 is None:
            self.rotor2_original = self.generator.random_all_ascii()
        else:
            self.rotor2_original = rotor2

        if rotor3 is None:
            self.rotor3_original = self.generator.random_all_ascii()
        else:
            self.rotor3_original = rotor3

        self.rotor_length = len(self.rotor1_original)  # 128 ascii length
        sorted_alphabet = sorted(self.generator.random_all_ascii())

        for i, rotor in enumerate(
            [self.rotor1_original, self.rotor2_original, self.rotor3_original], start=1
        ):
            if sorted(rotor) != sorted_alphabet:
                raise ValueError(
                    f"Rotor {i} must contain 26 unique uppercase and 26 unique lowercase letters."
                )
        self.reset_rotors()

    def reset_rotors(self):
        """
        Resets the current state of the machine.

        This sets the active rotors back to their original wirings and resets all
        rotor position counters (rotor1_pos, rotor2_pos, rotor3_pos) to 0.
        """
        self.rotor1 = self.rotor1_original.copy()
        self.rotor2 = self.rotor2_original.copy()
        self.rotor3 = self.rotor3_original.copy()
        self.rotor1_pos = 0
        self.rotor2_pos = 0
        self.rotor3_pos = 0

    def rotate_rotors(self):
        """
        Rotates the rotors according to the internal stepping mechanism.

        Rotor 1 (fastest) rotates every character input.
        Rotor 2 (medium) rotates when Rotor 1 completes half a revolution.
        Rotor 3 (lowest) rotates when Rotor 2 completes a full revolution.
        """
        # Fast rotor
        self.rotor1 = self.rotor1[1:] + [self.rotor1[0]]
        self.rotor1_pos = (self.rotor1_pos + 1) % self.rotor_length

        # Medium rotor
        if self.rotor1_pos % (self.rotor_length // 2) == 0:
            self.rotor2 = self.rotor2[1:] + [self.rotor2[0]]
            self.rotor2_pos = (self.rotor2_pos + 1) % self.rotor_length

        # Slow rotor
        if self.rotor2_pos % self.rotor_length == 0:
            self.rotor3 = self.rotor3[1:] + [self.rotor3[0]]
            self.rotor3_pos = (self.rotor3_pos + 1) % self.rotor_length

    def encrypt_char(self, char1):  # O(N)
        """
        Encrypts a single character using the current rotor configuration.

        The character goes through the permutation sequence: Rotor 1 -> Rotor 2 -> Rotor 3.
        The rotors rotate after the character is encrypted.

        Args:
            char1 (str): The single plaintext character to encrypt.

        Returns:
            str: The resulting ciphertext character, or the original character if it's
                 not part of the rotor alphabet (e.g., punctuation or space).
        """
        if char1 not in self.rotor1:
            output_char = char1
        else:
            output_char = char1
            char2 = self.rotor2[self.rotor1.index(char1)]
            char3 = self.rotor3[self.rotor2.index(char2)]
            output_char = char3

        self.rotate_rotors()

        return output_char

    def decrypt_char(self, char3):
        """
        Decrypts a single character using the current rotor configuration.

        The character goes through the inverse permutation sequence: Rotor 3 <- Rotor 2 <- Rotor 1.
        The rotors rotate after the character is decrypted.

        Args:
            char3 (str): The single ciphertext character to decrypt.

        Returns:
            str: The resulting plaintext character, or the original character if it's
                 not part of the rotor alphabet.
        """
        if char3 not in self.rotor3:
            output_char = char3

        else:
            char2 = self.rotor2[self.rotor3.index(char3)]
            char1 = self.rotor1[self.rotor2.index(char2)]
            output_char = char1

        self.rotate_rotors()

        return output_char

    def encrypt(self, text):
        """
        Encrypts an entire string by processing each character sequentially.

        The rotors are reset before encryption begins. All input is converted to uppercase.

        Args:
            text (str): The plaintext string to be encrypted.

        Returns:
            str: The resulting ciphertext string.
        """
        self.reset_rotors()
        encrypted_text = ""
        for char in text:
            encrypted_text += self.encrypt_char(char)
        return encrypted_text

    def decrypt(self, text):
        """
        Decrypts an entire string by processing each character sequentially.

        The rotors are reset before decryption begins. All input is converted to uppercase.

        Args:
            text (str): The ciphertext string to be decrypted.

        Returns:
            str: The resulting plaintext string.
        """
        self.reset_rotors()
        decrypted_text = ""
        for char in text:
            decrypted_text += self.decrypt_char(char)
        return decrypted_text

    def get_rotor_state_dict(self) -> dict:
        """Returns the current state of the rotor machine

        Returns:
            dict: Dictionary containing the current state of the rotor machine
        """
        return {
            "rotor1": self.rotor1,
            "rotor2": self.rotor2,
            "rotor3": self.rotor3,
            "rotor1_pos": self.rotor1_pos,
            "rotor2_pos": self.rotor2_pos,
            "rotor3_pos": self.rotor3_pos,
            "rotor1_current": self.rotor1[0],
            "rotor2_current": self.rotor2[0],
            "rotor3_current": self.rotor3[0],
        }
