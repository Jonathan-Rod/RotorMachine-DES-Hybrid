from des_generator import DesGenerator
import string

class RotorMachine:
    """
    Implements a basic three-rotor cipher machine.

    The machine uses three distinct rotor wirings (permutation alphabets) generated
    randomly by a DesGenerator instance upon initialization.
    """

    def __init__(
        self,
        rotor1: list[str] = None,
        rotor2: list[str] = None,
        rotor3: list[str] = None,
    ):
        """
        Initializes the RotorMachine with either custom or randomly generated rotor wirings.

        If custom rotors are provided, they must each contain exactly 26 unique characters.
        If no rotors are provided, three random rotor wirings will be generated using DesGenerator.

        Args:
            rotor1: Optional custom wiring for rotor 1 (default: randomly generated)
            rotor2: Optional custom wiring for rotor 2 (default: randomly generated)
            rotor3: Optional custom wiring for rotor 3 (default: randomly generated)

        Raises:
            ValueError: If a rotor does not contain 26 unique characters.
        """

        self.generator = DesGenerator()

        if rotor1 is None:
            rotor1 = self.generator.random_alphabet()
        if rotor2 is None:
            rotor2 = self.generator.random_alphabet()
        if rotor3 is None:
            rotor3 = self.generator.random_alphabet()

        self.rotor1_original = rotor1
        self.rotor2_original = rotor2
        self.rotor3_original = rotor3
        self.rotor_length = len(string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation + " ")
        for i, rotor in enumerate(
            [self.rotor1_original, self.rotor2_original, self.rotor3_original], start=1
        ):
            if len(set(rotor)) != self.rotor_length:
                raise ValueError(
                    f"Rotor {i} must contain {self.rotor_length} unique characters."
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
        Rotor 2 rotates when Rotor 1 completes half a revolution.
        Rotor 3 rotates when Rotor 2 completes a full revolution.
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


if __name__ == "__main__":

    # Using custom rotors
    rotor1 = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    rotor2 = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    rotor3 = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    #rotor_machine = RotorMachine(rotor1=rotor1, rotor2=rotor2, rotor3=rotor3)
    rotor_machine = RotorMachine()
    plaintext = "Hemos terminado la implementación de rotors."

    ciphertext = rotor_machine.encrypt(plaintext)
    print(rotor_machine.get_rotor_state_dict())
    print(f"Ciphertext: {ciphertext}")

    decrypted_text = rotor_machine.decrypt(ciphertext)
    print(rotor_machine.get_rotor_state_dict())
    print(f"Decrypted text: {decrypted_text}")
