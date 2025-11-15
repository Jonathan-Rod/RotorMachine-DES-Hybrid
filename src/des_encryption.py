from des_permutation import DESPermutation
from des_bit_converter import DESBitConverter
from des_parser import DESParser


class DESEncryption:
    def __init__(self, rounds=16):
        # self.key = key
        self.rounds = rounds
        self.permutation = DESPermutation()  # TODO
        self.bit_converter = DESBitConverter()  # TODO
        self.parser = DESParser()
        self.subkeys = self._generate_subkeys()  # TODO 48 bits each subkey

    # Changed input to hanlde any bit length
    def left_circular_shift(self, block_bits):
        # Apply left circular shift to block_bits
        length = len(block_bits)
    
        # Use modulo to handle shifts larger than the string length
        shift_amount = 1 % length
    
        shifted_string = block_bits[shift_amount:] + block_bits[:shift_amount]
    
        return shifted_string


    def _generate_subkeys(self):
        # TODO #5 Implement Subkey Generation
        # TODO Generate all rounds subkeys
        # TODO key 64-bits
        key_64bits = ""  # TODO
        # TODO permutation.permuted_choice_1
        key_56bits = self.permutation.permuted_choice_1(key_64bits)
        # TODO inside a for loop self.rounds
        subkeys = []
        for i in range(self.rounds):
            # TODO left_circular_shift
            if i == 0:
                shifted_key_56bits = self.left_circular_shift(key_56bits)
            else:
                shifted_key_56bits = self.left_circular_shift(shifted_key_56bits)

            # TODO permutation.permuted_choice_2
            subkey = self.permutation.permuted_choice_2(shifted_key_56bits)
            subkeys.append(subkey)

        return subkeys

    def _xor(self, x_bits: str, y_bits: str) -> str:
        """Performs a bitwise XOR operation on two bit strings of equal length.

        Args:
            x_bits (str): The first bit string.
            y_bits (str): The second bit string.

        Returns:
            str: The result of the XOR operation.
        """
        if len(x_bits) != len(y_bits):
            raise ValueError("Input bit strings must be of equal length")

        xor_bits = ""

        for a, b in zip(x_bits, y_bits):
            xor_bit = str(int(a) ^ int(b))
            xor_bits += xor_bit

        return xor_bits

    def _sbox(self, block_48bits: str) -> str:  # TODO
        """TODO #4 Applies S-box substitution to the given 48-bit block.

        Args:
            block_48bits (str): The 48-bit block to apply S-box substitution to.

        Returns:
            str: The 32-bit result of the S-box substitution.
        """
        return "0" * 32  # TODO

    def round(self, left_32bits, right_32bits, subkey_48bits):
        """Applies a single round of DES encryption to the given 32-bit blocks.

        Args:
            left_32bits (str): The left 32-bit block.
            right_32bits (str): The right 32-bit block.
            subkey_48bits (str): The 48-bit subkey for the current round.

        Returns:
            tuple: A tuple containing the new left and right 32-bit blocks after the round.
        """

        # 1. Expansion/permutation(E table) right_32bits to right_48bits
        right_48bits = self.permutation.e_table(right_32bits)

        # 2. XOR with expanded right_48bits and subkey_48bits
        XOR_48bits = self._xor(right_48bits, subkey_48bits)

        # 3. TODO S-box substitution (Uses the XOR_48bits result returns sbox_32bits)
        sbox_32bits = self._sbox(XOR_48bits)

        # 4. TODO P-box permutation (uses sbox_32bits returns pbox_32bits)
        pbox_32bits = self.permutation.p_box(sbox_32bits)

        # 5. XOR with plaintext (uses pbox_32bits and left_32bits returns new_right_32bits)
        new_right_32bits = self._xor(pbox_32bits, left_32bits)

        # 6. Return the right_32bits as new_left_32bits and new_right_32bits
        new_left_32bits = right_32bits

        return new_left_32bits, new_right_32bits

    def encrypt_block(self, block_64bits: str) -> str:
        """Encrypts a 64-bit block using the DES algorithm.

        Args:
            block_64bits (str): The 64-bit block to encrypt.

        Returns:
            str: The encrypted 64-bit block.
        """

        # 1. Apply initial permutation
        initial_permutation = self.permutation.initial_permutation(block_64bits)

        # 2. split initial_permutation into left_32bits and right_32bits
        if len(initial_permutation) != 64:
            raise ValueError(
                f"Block size mismatch: expected 64 bits, got {len(initial_permutation)} bits."
            )
        left_32bits = initial_permutation[:32]
        right_32bits = initial_permutation[32:]

        # 4. TODO Apply rounds
        for i in range(self.rounds):
            left_32bits, right_32bits = self.round(
                left_32bits, right_32bits, self.subkeys[i]
            )

        # 5. 32-bit swap
        left_32bits, right_32bits = right_32bits, left_32bits
        swapped_block_64bits = left_32bits + right_32bits

        # 6. Apply inverse initial permutation (block_64bits after 32-bit swap)
        inverse_initial_permutation = self.permutation.inverse_initial_permutation(
            swapped_block_64bits
        )

        return inverse_initial_permutation

    def encrypt(self, plaintext: str) -> str:  # TODO
        """Encrypts the given plaintext using DES encryption.

        Args:
            plaintext (str): The plaintext to encrypt.

        Returns:
            str: The encrypted ciphertext.
        """

        # 1. Convert string to binary
        binary_str = self.bit_converter.str_to_binary(plaintext)

        # 2. Divide binary into 64-bit blocks with padding
        blocks_64bits = self.parser.parse(binary_str)

        # 3. Encrypt each 64-bit block
        encrypted_blocks_64bits = [
            self.encrypt_block(block_64bits) for block_64bits in blocks_64bits
        ]

        # 4. Join encrypted blocks and convert to string
        encrypted_binary = "".join(encrypted_blocks_64bits)
        ciphertext = self.bit_converter.binary_to_str(encrypted_binary)

        return ciphertext

    def decrypt_block(self, block_64bits):
        # TODO #3 Implement Decryption block logic
        # Same process as encryption but in reverse ordder of subkeys
        pass

    def decrypt(self, ciphertext):
        # TODO #2 Implement Decryption logic
        # TODO divides ciphertext into blocks
        # TODO decrypts each block
        # TODO removes padding
        # TODO joins decrypted blocks
        # TODO returns plaintext
        pass
