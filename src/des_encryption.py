from des_permutation import DESPermutation
from des_bit_converter import DESBitConverter
from des_parser import DESParser


class DESEncryption:
    def __init__(self, key, rounds=16):
        self.key = key
        self.rounds = rounds
        self.permutation = DESPermutation()  # TODO
        self.bit_converter = DESBitConverter()  # TODO
        self.parser = DESParser()
        self.subkeys = self._generate_subkeys()  # TODO

    def left_circular_shift(self, block_56bits):
        # TODO Apply left circular shift to block_56bits
        # returns shifted_56bits
        pass

    def _generate_subkeys(self):
        # TODO Generate all rounds subkeys
        # TODO permutation.permuted_choice_1
        # TODO left_circular_shift
        # TODO permutation.permuted_choice_2
        # returns subkeys list

        pass

    def _xor(self, x_bits, y_bits):
        # TODO Apply XOR to x_bits and y_bits (same length)
        # returns xor_bits
        pass

    def _sbox(self, block_48bits):
        # TODO Apply S-box to block_48bits
        # returns sbox_32bits (32 bits)
        pass

    def round(self, left_32bits, right_32bits, subkey_48bits):
        # 1. Expansion/permutation(E table) right_32bits to right_48bits
        right_48bits = self.permutation.e_table(right_32bits)  # TODO right_32bits

        # 2. XOR with expanded right_48bits and subkey_48bits
        XOR_48bits = self._xor(
            right_48bits, subkey_48bits
        )  # TODO right_48bits and subkey_48bits

        # 3. S-box substitution (Uses the XOR_48bits result returns sbox_32bits)
        sbox_32bits = self._sbox(XOR_48bits)  # TODO XOR_48bits

        # 4. P-box permutation (uses sbox_32bits returns pbox_32bits)
        pbox_32bits = self.permutation.p_box(sbox_32bits)  # TODO sbox_32bits

        # 5. XOR with plaintext (uses pbox_32bits and left_32bits returns new_right_32bits)
        new_right_32bits = self._xor(
            pbox_32bits, left_32bits
        )  # TODO pbox_32bits and left_32bits

        # 6. Return the right_32bits as new_left_32bits and new_right_32bits
        new_left_32bits = right_32bits

        return new_left_32bits, new_right_32bits

    def encrypt_block(self, block_64bits):
        # 1. Apply initial permutation
        initial_permutation = self.permutation.initial_permutation(
            block_64bits
        )  # TODO block_64bits

        # 2. split initial_permutation into left_32bits and right_32bits
        left_32bits = ...  # TODO
        right_32bits = ...  # TODO

        # 4. Apply rounds
        for i in range(self.rounds):
            left_32bits, right_32bits = self.round(
                left_32bits, right_32bits, self.subkeys[i]
            )  # TODO left_32bits, right_32bits and subkeys[i]

        # 5. 32-bit swap
        left_32bits, right_32bits = right_32bits, left_32bits

        # 6. Apply inverse initial permutation (block_64bits after 32-bit swap)
        inverse_initial_permutation = ...  # TODO block_64bits

        return inverse_initial_permutation

    def encrypt(self, plaintext):
        # TODO Encryption logic
        # TODO divides plaintext into blocks (bit_converter)
        # TODO apply padding if needed (parser)
        # TODO encrypts each block of 64bits (encrypt_block)
        # TODO joins encrypted blocks into ciphertext (bit_converter again and then concatenate to string)
        # TODO returns ciphertext
        pass

    def decrypt_block(self, block_64bits):
        # TODO Decryption logic 64 bits
        # Same process as encryption but in reverse ordder of subkeys
        pass

    def decrypt(self, ciphertext):
        # TODO Decryption logic
        # TODO divides ciphertext into blocks
        # TODO decrypts each block
        # TODO removes padding
        # TODO joins decrypted blocks
        # TODO returns plaintext
        pass
