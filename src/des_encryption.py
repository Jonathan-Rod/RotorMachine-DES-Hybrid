from des_generator import DesGenerator
from des_permutation import DESPermutation
from des_bit_converter import DESBitConverter
from des_parser import DESParser

class DESEncryption:
    """Implements the Data Encryption Standard (DES) algorithm in Electronic Codebook (ECB) mode.

    The class handles key generation, subkey creation, S-box substitution,
    P-box permutation, and the full Feistel network for 64-bit block encryption and decryption.

    Attributes:
        rounds (int): The number of Feistel rounds (default is 16 for standard DES).
        permutation (DESPermutation): Helper object for various permutations (IP, EP, PC-1, PC-2, P-box).
        bit_converter (DESBitConverter): Helper object for string-to-binary and binary-to-string conversions.
        parser (DESParser): Helper object for 64-bit block parsing and padding/deparsing.
        generator (DesGenerator): Helper object for generating random alphabets and permutations.
        key_64bits (str): The 64-bit encryption key in binary format.
        subkeys (list[str]): A list containing the 16 48-bit subkeys used for the rounds.
        sbox_tables (list[list[int]]): A list of 8 S-box tables (each containing 64 4-bit integers).

    Args:
        key_64bits (str, optional): A user-provided 64-bit key string in binary format.
                                    If None, a random 64-bit key is generated. Defaults to None.
        rounds (int, optional): The number of DES rounds to perform. Defaults to 16.

    Raises:
        ValueError: If a provided key_64bits is not exactly 64 bits long.
    """

    def __init__(self, key_64bits: str = None, rounds: int = 16):
        self.rounds = rounds
        self.permutation = DESPermutation()
        self.bit_converter = DESBitConverter()
        self.parser = DESParser()
        self.generator = DesGenerator()
        if key_64bits:
            if len(key_64bits) != 64:
                raise ValueError(
                    f"Key size mismatch: expected 64 bits, got {len(key_64bits)} bits."
                )
            self.key_64bits = key_64bits
        else:
            self.key_64bits = self._generate_key()

        self.subkeys = self._generate_subkeys()
        self.sbox_tables = self._generate_sbox_tables()

    def _generate_sbox_tables(self) -> list[list[int]]:
        """Returns a list of 8 S-box tables, each containing 64 4-bit integers.

        Returns:
            list[list[int]]: A list of 8 S-box tables.
        """
        sbox_tables = []
        num_tables = 8
        for _ in range(num_tables):
            sbox = []
            num_rows = 4
            for _ in range(num_rows):
                num_columns = 16
                row = self.generator.random_permutation_unique(num_columns)
                sbox.extend(row)
            sbox_tables.append(sbox)
        return sbox_tables

    def _generate_key(self) -> str:
        """Generates a 64-bit random key for DES encryption.

        Returns:
            str: A 64-bit key in binary format.
        """
        block_size = 64
        generated_key_64bits = self.generator.random_bits(block_size)
        return generated_key_64bits

    def left_circular_shift(self, block_bits: str) -> str:
        """Performs a single-bit left circular shift on a string of bits.

        This is used during the subkey generation process (PC-1 output) to cyclically
        shift the C and D halves. The bit from the left end is moved to the right end.

        Args:
            block_bits (str): The bit string (e.g., 28 bits of C or D) to shift.

        Returns:
            str: The resulting bit string after the left circular shift.
        """

        length = len(block_bits)
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
        block_pc1_size = 64
        if len(key_64bits) != block_pc1_size:
            raise ValueError(
                f"Key size mismatch: expected {block_pc1_size} bits, got {len(key_64bits)} bits."
            )

        # 1. Apply Permuted_choice_1
        key_56bits = self.permutation.permuted_choice_1(key_64bits)
        block_pc1_size = 56
        if len(key_56bits) != block_pc1_size:
            raise ValueError(
                f"Key size mismatch after PC-1: expected {block_pc1_size} bits, got {len(key_56bits)} bits."
            )
        # 2. Split into left and right 28 bits
        half_block_pc1_size = block_pc1_size // 2
        C = key_56bits[:half_block_pc1_size]
        D = key_56bits[half_block_pc1_size:]

        # 3. Generate 16 subkeys of 48 bits each
        subkeys_48bits = []
        for i in range(self.rounds):
            # 4. Left circular shift both halves
            C = self.left_circular_shift(C)
            D = self.left_circular_shift(D)

            # 5. Combine halves back into 56 bits
            shifted_key_56bits = C + D

            # 6. Apply permuted_choice_2
            subkey_48bits = self.permutation.permuted_choice_2(shifted_key_56bits)
            block_pc2_size = 48
            if len(subkey_48bits) != block_pc2_size:
                raise ValueError(
                    f"Subkey size mismatch after PC-2: expected {block_pc2_size} bits, got {len(subkey_48bits)} bits."
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
        num_boxes = 8
        for sbox_index in range(num_boxes):

            bits_per_block = 6
            block_6bits = block_48bits[
                sbox_index * bits_per_block : (sbox_index + 1) * bits_per_block
            ]

            # 2. Determine row and column for S-box lookup
            row_bits = block_6bits[0] + block_6bits[5]
            col_bits = block_6bits[1:5]

            # Convert binary to decimal
            base = 2
            row = int(row_bits, base)
            col = int(col_bits, base)

            # 3. Apply S-box lookup
            sbox_columns = 16
            sbox_item = self.sbox_tables[sbox_index][row * sbox_columns + col]

            bits_per_sbox = 4
            sbox_output_bits = format(sbox_item, f"0{bits_per_sbox}b")

            # 4. Combine results into 32-bit block
            result_32bits += sbox_output_bits

        return result_32bits

    def round(
        self, left_32bits: str, right_32bits: str, subkey_48bits: str
    ) -> tuple[str, str]:
        """Applies a single round of DES encryption to the given 32-bit blocks.

        Args:
            left_32bits (str): The left 32-bit block.
            right_32bits (str): The right 32-bit block.
            subkey_48bits (str): The 48-bit subkey for the current round.

        Returns:
            tuple[str, str]: A tuple containing the new left and right 32-bit blocks after the round.
        """

        # 1. Expansion/permutation(E table) right_32bits to right_48bits
        right_48bits = self.permutation.expansion(right_32bits)

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
        block_size = 64
        if len(initial_permutation) != block_size:
            raise ValueError(
                f"Block size mismatch: expected {block_size} bits, got {len(initial_permutation)} bits."
            )

        half_bits = block_size // 2
        left_32bits = initial_permutation[:half_bits]
        right_32bits = initial_permutation[half_bits:]

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
        """
        Decrypts a single 64-bit ciphertext block using the DES algorithm.

        The decryption process uses the same Feistel rounds as encryption, but the
        48-bit subkeys are applied in reverse order.

        Args:
            block_64bits (str): The 64-bit block to decrypt.

        Returns:
            str: The decrypted 64-bit plaintext block.
        """

        # 1. Apply initial permutation
        initial_permutation = self.permutation.initial_permutation(block_64bits)

        # 2. split initial_permutation into left_32bits and right_32bits
        block_size = 64
        if len(initial_permutation) != block_size:
            raise ValueError(
                f"Block size mismatch: expected {block_size} bits, got {len(initial_permutation)} bits."
            )
        half_bits = block_size // 2
        left_32bits = initial_permutation[:half_bits]
        right_32bits = initial_permutation[half_bits:]

        # 4. Apply rounds inverse round keys
        for i in range(self.rounds - 1, -1, -1):
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

    def decrypt(self, ciphertext: str) -> str:
        """Decrypts the given ciphertext using the DES algorithm.

        The ciphertext is converted to binary, broken into 64-bit blocks, decrypted,
        padding is removed, and the result is converted back to a string.

        Args:
            ciphertext (str): The ciphertext to decrypt.

        Returns:
            str: The final decrypted plaintext.
        """
        # 1. Convert string to binary
        binary_str = self.bit_converter.str_to_binary(ciphertext)

        # 2. Divide binary into 64-bit blocks
        block_size = 64
        blocks_64bits = [
            binary_str[i : i + block_size]
            for i in range(0, len(binary_str), block_size)
        ]

        # 3. Decrypt each 64-bit block
        encrypted_blocks_64bits = [
            self.decrypt_block(block_64bits) for block_64bits in blocks_64bits
        ]

        # 4. Remove padding here
        deparsed_decrypted_binary = self.parser.deparse(encrypted_blocks_64bits)

        # 5. Join encrypted blocks and convert to string
        plaintext = self.bit_converter.binary_to_str(deparsed_decrypted_binary)
        return plaintext


if __name__ == "__main__":
    des = DESEncryption()
    plaintext = "Hemos terminado la implementación de DES."
    ciphertext = des.encrypt(plaintext)
    print(f"Ciphertext: {ciphertext}")
    decrypted_text = des.decrypt(ciphertext)
    print(f"Decrypted text: {decrypted_text}")
