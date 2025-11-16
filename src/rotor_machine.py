class RotorMachine:

    def __init__(
        self,
        rotor1: list[str] = list("UCOASJNZTHPGVDKEQILWRBYFXM"),
        rotor2: list[str] = list("ZABCDEFGHIJKLMNOPQRSTUVWXY"),
        rotor3: list[str] = list("TAFDOCNLWEPBVSKRYXMGJHUIZQ"),
    ):
        self.rotor1_original = rotor1
        self.rotor2_original = rotor2
        self.rotor3_original = rotor3
        self.rotor_length = 26
        for i, rotor in enumerate([rotor1, rotor2, rotor3], start=1):
            if len(set(rotor)) != self.rotor_length:
                raise ValueError(
                    f"Rotor {i} must contain {self.rotor_length} unique characters."
                )
        self.reset_rotors()

    def reset_rotors(self):
        self.rotor1 = self.rotor1_original.copy()
        self.rotor2 = self.rotor2_original.copy()
        self.rotor3 = self.rotor3_original.copy()
        self.rotor1_pos = 0
        self.rotor2_pos = 0
        self.rotor3_pos = 0

    def rotate_rotors(self):
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

    def encrypt_char(self, char1): # O(N)
        if char1 not in self.rotor1:
            return char1

        # Here is the ecryption logic
        char2 = self.rotor2[self.rotor1.index(char1)] # O(1)
        char3 = self.rotor3[self.rotor2.index(char2)] # O(1)

        # Apply rotation after each character
        self.rotate_rotors() # O(N)

        return char3

    def decrypt_char(self, char3):
        if char3 not in self.rotor3:
            return char3

        # Here is the decryption logic
        char2 = self.rotor2[self.rotor3.index(char3)]
        char1 = self.rotor1[self.rotor2.index(char2)]

        # Apply rotation after each character
        self.rotate_rotors()

        return char1

    def encrypt(self, text):
        self.reset_rotors()
        encrypted_text = ""
        for char in text.upper():
            encrypted_text += self.encrypt_char(char)
        return encrypted_text

    def decrypt(self, text):
        self.reset_rotors()
        decrypted_text = ""
        for char in text.upper():
            decrypted_text += self.decrypt_char(char)
        return decrypted_text

