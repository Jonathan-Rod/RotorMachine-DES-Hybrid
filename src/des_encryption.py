from des_permutation import DESPermutation
from des_bit_converter import DESBitConverter
from des_parser import DESParser
from random import getrandbits


class DESEncryption:
    def __init__(self, rounds: int = 16):
        self.rounds = rounds
        self.permutation = DESPermutation()
        self.bit_converter = DESBitConverter()
        self.parser = DESParser()
        self.key_64bits = self._generate_key()  # TODO Implement key generation
        self.subkeys = self._generate_subkeys()

        self.sbox_tables: list[list[list[int]]] = (
            ""  # TODO Define 8 S-box tables in DESPermutation class
        )

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
        # TODO #5 Implement Subkey Generation
        """Generate 16 subkeys of 48 bits each from the given key.

        Raises:
            ValueError: If the key size is not 64 bits.

        Returns:
            list[str]: A list of 16 subkeys of 48 bits each.
        """
        key_64bits = self.key_64bits  # TODO Ensure key
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

    def _sbox(self, block_48bits: str) -> str:  # TODO
        """TODO #4 Applies S-box substitution to the given 48-bit block.

        Args:
            block_48bits (str): The 48-bit block to apply S-box substitution to.

        Returns:
            str: The 32-bit result of the S-box substitution.
        """

        result_32bits = ""
        # 1. TODO Divide block_48bits into 8 blocks of 6 bits each
        for i in range(8):
            block_6bits = block_48bits[i * 6 : (i + 1) * 6]

            # 2. TODO Determine row and column for S-box lookup
            row_bits = block_6bits[0] + block_6bits[5]
            col_bits = block_6bits[1:5]

            row = int(row_bits, 2)  # Convert to decimal
            col = int(col_bits, 2)  # Convert to decimal

            # 3. TODO Apply S-box lookup
            sbox_item = self.sbox_tables[i][row][col]  # TODO Get S-box value
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

        # 3. TODO S-box substitution (Uses the XOR_48bits result returns sbox_32bits)
        sbox_32bits = self._sbox(XOR_48bits)

        # 4. TODO P-box permutation (uses sbox_32bits returns pbox_32bits)
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


if __name__ == "__main__":
    des = DESEncryption()
    des.key_64bits = "1011001110010110010110011101010001001111111011011110001101111011"
    des._generate_subkeys()
    print(
        des.subkeys)