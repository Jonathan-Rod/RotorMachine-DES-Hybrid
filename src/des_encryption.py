class DESEncryption:
    def __init__(self, plaintext, key):
        self.plaintext = plaintext
        self.key = key
        self.rounds = 16

    def left_circular_shift(self, key):
        # TODO
        return key[1:] + key[0]

    def permuted_choice_1(self, key):
        # TODO
        pass

    def permuted_choice_2(self, key):
        # TODO
        pass

    def round(self, plaintext, permuted_choice_2):
        # TODO Expansion/permutation with plaintext (E table) (plaintex Right side)
        # TODO XOR with round key (permuted_choice_2)
        # TODO S-box substitution
        # TODO P-box permutation
        # TODO XOR with plaintext (plaintextLeft side)

        return plaintext

    def encrypt(self, text):
        # Encryption logic
        key = self.permuted_choice_1(self.key)
        for i in range(self.rounds):
            key = self.left_circular_shift(key)
            permuted_choice_2 = self.permuted_choice_2(key)
            text = self.round(text, permuted_choice_2)

        return text

    def decrypt(self, text):
        # Decryption logic
        for i in range(self.rounds):
            pass

        return text
