from des_permutation import DESPermutation
from des_bit_converter import DESBitConverter
from des_parser import DESParser
from random import getrandbits


class DESEncryption:
    def __init__(self, key_64bits: str = None, rounds: int = 16):
        self.rounds = rounds
        self.permutation = DESPermutation()
        self.bit_converter = DESBitConverter()
        self.parser = DESParser()

        if key_64bits:
            if len(key_64bits) != 64:
                raise ValueError(
                    f"Key size mismatch: expected 64 bits, got {len(key_64bits)} bits."
                )
            self.key_64bits = key_64bits
        else:
            self.key_64bits = self._generate_key()

        self.subkeys = self._generate_subkeys()

        self.sbox_tables: list[list[list[int]]] = [
            # S1
            [
                [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
                [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
                [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
                [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
            ],
            # S2
            [
                [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
                [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
                [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
                [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
            ],
            # S3
            [
                [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
                [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
                [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
                [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
            ],
            # S4
            [
                [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
                [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
                [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
                [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
            ],
            # S5
            [
                [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
                [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
                [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
                [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
            ],
            # S6
            [
                [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
                [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
                [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
                [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
            ],
            # S7
            [
                [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
                [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
                [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
                [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
            ],
            # S8
            [
                [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
                [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
                [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
                [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
            ],
        ]

    def _generate_key(self) -> str:
        """
        Generates a 64-bit random key for DES encryption.

        Returns:
            str: A 64-bit key in binary format.
        """
        generated_key_64bits = format(getrandbits(64), "064b")
        return generated_key_64bits

    def left_circular_shift(self, block_bits):
        # Apply left circular shift to block_bits
        length = len(block_bits)

        # Use modulo to handle shifts larger than the string length
        shift_amount = 1 % length

        shifted_string = block_bits[shift_amount:] + block_bits[:shift_amount]

        return shifted_string

    def _generate_subkeys(self) -> list[str]:
        """Generate 16 subkeys of 48 bits each from the given key.

        Raises:
            ValueError: If the key size is not 64 bits.

        Returns:
            list[str]: A list of 16 subkeys of 48 bits each.
        """
        key_64bits = self.key_64bits
        if len(key_64bits) != 64:
            raise ValueError(
                f"Key size mismatch: expected 64 bits, got {len(key_64bits)} bits."
            )

        # 1. TODO Apply Permuted_choice_1
        key_56bits = self.permutation.permuted_choice_1(key_64bits)
        if len(key_56bits) != 56:
            raise ValueError(
                f"Key size mismatch after PC-1: expected 56 bits, got {len(key_56bits)} bits."
            )
        # 2. Split into left and right 28 bits
        C = key_56bits[:28]
        D = key_56bits[28:]

        # 3. TODO Generate 16 subkeys of 48 bits each
        subkeys_48bits = []
        for i in range(self.rounds):
            # 4. TODO Left circular shift both halves
            C = self.left_circular_shift(C)
            D = self.left_circular_shift(D)

            # 5. Combine halves back into 56 bits
            shifted_key_56bits = C + D

            # 6. TODO Apply permuted_choice_2
            subkey_48bits = self.permutation.permuted_choice_2(shifted_key_56bits)
            if len(subkey_48bits) != 48:
                raise ValueError(
                    f"Subkey size mismatch after PC-2: expected 48 bits, got {len(subkey_48bits)} bits."
                )
            subkeys_48bits.append(subkey_48bits)

        return subkeys_48bits

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

    def _sbox(self, block_48bits: str) -> str:
        """#4 Applies S-box substitution to the given 48-bit block.

        Args:
            block_48bits (str): The 48-bit block to apply S-box substitution to.

        Returns:
            str: The 32-bit result of the S-box substitution.
        """

        result_32bits = ""
        # 1. Divide block_48bits into 8 blocks of 6 bits each
        for i in range(8):
            block_6bits = block_48bits[i * 6 : (i + 1) * 6]

            # 2. Determine row and column for S-box lookup
            row_bits = block_6bits[0] + block_6bits[5]
            col_bits = block_6bits[1:5]

            row = int(row_bits, 2)  # Convert to decimal
            col = int(col_bits, 2)  # Convert to decimal

            # 3. Apply S-box lookup
            sbox_item = self.sbox_tables[i][row][col]
            sbox_output_bits = format(sbox_item, "04b")  # Convert to 4-bit binary

            # 4. Combine results into 32-bit block
            result_32bits += sbox_output_bits

        return result_32bits

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

        # 3. S-box substitution (Uses the XOR_48bits result returns sbox_32bits)
        sbox_32bits = self._sbox(XOR_48bits)

        # 4. P-box permutation (uses sbox_32bits returns pbox_32bits)
        pbox_32bits = self.permutation.p_box(sbox_32bits)

        # 5. XOR with plaintext (uses pbox_32bits and left_32bits returns new_right_32bits)
        new_right_32bits = self._xor(pbox_32bits, left_32bits)

        # 6. Return the right_32bits as new_left_32bits and new_right_32bits
        new_left_32bits = right_32bits

        # 7. Swap and prepare for next round.
        # We assume that the new_right_32bits is the output calculated in step 6 and new_left_32bits is the previous right_32bits

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

        # 4. Apply rounds
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

    def encrypt(self, plaintext: str) -> str:
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

    def decrypt_block(self, block_64bits: str) -> str:
        # TODO #3 Implement Decryption block logic

        # 1. Apply initial permutation
        initial_permutation = self.permutation.initial_permutation(block_64bits)

        # 2. split initial_permutation into left_32bits and right_32bits
        if len(initial_permutation) != 64:
            raise ValueError(
                f"Block size mismatch: expected 64 bits, got {len(initial_permutation)} bits."
            )
        left_32bits = initial_permutation[:32]
        right_32bits = initial_permutation[32:]

        # 4. Apply rounds inverse round keys
        for i in range(self.rounds):
            left_32bits, right_32bits = self.round(
                left_32bits, right_32bits, self.subkeys[self.rounds - 1 - i]
            )

        # 5. 32-bit swap
        left_32bits, right_32bits = right_32bits, left_32bits
        swapped_block_64bits = left_32bits + right_32bits

        # 6. Apply inverse initial permutation (block_64bits after 32-bit swap)
        inverse_initial_permutation = self.permutation.inverse_initial_permutation(
            swapped_block_64bits
        )

        return inverse_initial_permutation

    def decrypt(self, ciphertext: str) -> str:
        # 1. Convert string to binary
        binary_str = self.bit_converter.str_to_binary(ciphertext)

        # 2. Divide binary into 64-bit blocks
        blocks_64bits = [binary_str[i : i + 64] for i in range(0, len(binary_str), 64)]

        # 3. Decrypt each 64-bit block
        encrypted_blocks_64bits = [
            self.decrypt_block(block_64bits) for block_64bits in blocks_64bits
        ]

        # 4. Remove padding here
        deparsed_decrypted_blocks_64bits = self.parser.deparse_blocks(
            encrypted_blocks_64bits
        )

        # 5. Join encrypted blocks and convert to string
        decrypted_binary = "".join(deparsed_decrypted_blocks_64bits)
        plaintext = self.bit_converter.binary_to_str(decrypted_binary)
        return plaintext


if __name__ == "__main__":
    des = DESEncryption()
    plaintext = "Hemos terminado la implementación de DES."
    ciphertext = des.encrypt(plaintext)
    print(f"Ciphertext: {ciphertext}")
    decrypted_text = des.decrypt(ciphertext)
    print(f"Decrypted text: {decrypted_text}")

