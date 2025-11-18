from des_generator import DesGenerator


class DESPermutation:
    def __init__(self):  # TODO
        # DES Initial Permutation table 0-index tables
        self.generator = DesGenerator()

        # initial_permutation_table: 64
        self.initial_permutation_table = self.generator.random_permutation_unique(64)

        # inverse_initial_permutation_table: 64
        self.inverse_initial_permutation_table = self.generator.inverse_permutation(
            self.initial_permutation_table
        )

        # expansion_table: 32 -> 48
        self.expansion_table = self.generator.random_permutation(32, 48)

        # permuted_choice_2_table: 56
        self.permuted_choice_2_table = self.generator.random_permutation_unique(56)

        # p_box_table: 32
        self.p_box_table = self.generator.random_permutation_unique(32)

        # self.initial_permutation_table = [
        #     58,
        #     50,
        #     42,
        #     34,
        #     26,
        #     18,
        #     10,
        #     2,
        #     60,
        #     52,
        #     44,
        #     36,
        #     28,
        #     20,
        #     12,
        #     4,
        #     62,
        #     54,
        #     46,
        #     38,
        #     30,
        #     22,
        #     14,
        #     6,
        #     64,
        #     56,
        #     48,
        #     40,
        #     32,
        #     24,
        #     16,
        #     8,
        #     57,
        #     49,
        #     41,
        #     33,
        #     25,
        #     17,
        #     9,
        #     1,
        #     59,
        #     51,
        #     43,
        #     35,
        #     27,
        #     19,
        #     11,
        #     3,
        #     61,
        #     53,
        #     45,
        #     37,
        #     29,
        #     21,
        #     13,
        #     5,
        #     63,
        #     55,
        #     47,
        #     39,
        #     31,
        #     23,
        #     15,
        #     7,
        # ]

        # # DES Expansion table
        # self.expansion_table = [
        #     32,
        #     1,
        #     2,
        #     3,
        #     4,
        #     5,
        #     4,
        #     5,
        #     6,
        #     7,
        #     8,
        #     9,
        #     8,
        #     9,
        #     10,
        #     11,
        #     12,
        #     13,
        #     12,
        #     13,
        #     14,
        #     15,
        #     16,
        #     17,
        #     16,
        #     17,
        #     18,
        #     19,
        #     20,
        #     21,
        #     20,
        #     21,
        #     22,
        #     23,
        #     24,
        #     25,
        #     24,
        #     25,
        #     26,
        #     27,
        #     28,
        #     29,
        #     28,
        #     29,
        #     30,
        #     31,
        #     32,
        #     1,
        # ]

        # # DES Inverse Initial Permutation table
        # self.inverse_initial_permutation_table = [
        #     40,
        #     8,
        #     48,
        #     16,
        #     56,
        #     24,
        #     64,
        #     32,
        #     39,
        #     7,
        #     47,
        #     15,
        #     55,
        #     23,
        #     63,
        #     31,
        #     38,
        #     6,
        #     46,
        #     14,
        #     54,
        #     22,
        #     62,
        #     30,
        #     37,
        #     5,
        #     45,
        #     13,
        #     53,
        #     21,
        #     61,
        #     29,
        #     36,
        #     4,
        #     44,
        #     12,
        #     52,
        #     20,
        #     60,
        #     28,
        #     35,
        #     3,
        #     43,
        #     11,
        #     51,
        #     19,
        #     59,
        #     27,
        #     34,
        #     2,
        #     42,
        #     10,
        #     50,
        #     18,
        #     58,
        #     26,
        #     33,
        #     1,
        #     41,
        #     9,
        #     49,
        #     17,
        #     57,
        #     25,
        # ]

        # self.permuted_choice_2_table = [
        #     6,
        #     25,
        #     39,
        #     38,
        #     55,
        #     28,
        #     16,
        #     2,
        #     53,
        #     46,
        #     30,
        #     9,
        #     19,
        #     27,
        #     21,
        #     7,
        #     32,
        #     13,
        #     20,
        #     52,
        #     23,
        #     34,
        #     18,
        #     35,
        #     17,
        #     10,
        #     43,
        #     31,
        #     11,
        #     5,
        #     47,
        #     42,
        #     45,
        #     26,
        #     51,
        #     44,
        #     15,
        #     3,
        #     36,
        #     50,
        #     37,
        #     56,
        #     12,
        #     14,
        #     49,
        #     29,
        #     22,
        #     8,
        #     4,
        #     33,
        #     54,
        #     40,
        #     24,
        #     48,
        #     41,
        #     1,
        # ]

        # self.p_box_table = [
        #     16,
        #     7,
        #     20,
        #     21,
        #     29,
        #     12,
        #     28,
        #     17,
        #     1,
        #     15,
        #     23,
        #     26,
        #     5,
        #     18,
        #     31,
        #     10,
        #     2,
        #     8,
        #     24,
        #     14,
        #     32,
        #     27,
        #     3,
        #     9,
        #     19,
        #     13,
        #     30,
        #     6,
        #     22,
        #     11,
        #     4,
        #     25,
        # ]

    def permutate(self, block_bits: str, table: list[int]) -> str:
        """
        Permutes the given block of bits according to the given table.

        Args:
            block_bits (str): The block of bits to be permuted.
            table (list[int]): The permutation table.

        Returns:
            str: The block of bits after permutation.
        """
        # Perform permutation
        permuted = ""
        for position in table:
            permuted += block_bits[position]

        # Returns bits after permutation
        return permuted

    def initial_permutation(self, block_64bits: str):
        """Permutes the 64-bit block according to the DES initial permutation table.

        Args:
            block_64bits (str): The 64-bit block to be permuted.

        Returns:
            str: The 64-bit block after permutation.
        """
        if len(block_64bits) != 64:
            raise ValueError(
                f"Block size mismatch: expected 64 bits, got {len(block_64bits)} bits."
            )
        return self.permutate(block_64bits, self.initial_permutation_table)

    def permuted_choice_1(self, key_64bits: str):
        """Permutation of 64-bit key to remove parity bits and return 56-bit key.

        Args:
            key_64bits (str): The 64-bit key to be permuted.

        Returns:
            str: The 56-bit key after removing parity bits.
        """
        if len(key_64bits) != 64:
            raise ValueError(
                f"Key size mismatch: expected 64 bits, got {len(key_64bits)} bits."
            )
        blocks_7bits = []
        for i in range(8):
            block_8bits = key_64bits[i * 8 : (i + 1) * 8]
            # Assuming parity bit convention is the first bit of each block
            block_7bits = block_8bits[1:]  # Remove parity bit
            blocks_7bits.append(block_7bits)

        block_56bits = "".join(blocks_7bits)
        return block_56bits

    def permuted_choice_2(self, key_56bits: str):
        """Permutes the 56-bit key and concatenates both parts and applies permutation again.
        Removes parity bits and returns 48-bit subkey for round i.

        Args:
            key_56bits (str): The 56-bit key to be permuted.

        Returns:
            str: The 48-bit subkey for round i.
        """

        if len(key_56bits) != 56:
            raise ValueError(
                f"Key size mismatch: expected 56 bits, got {len(key_56bits)} bits."
            )

        # 1. Permutation of 56-bit key
        permuted_block_56bits = ""
        for position in self.permuted_choice_2_table:
            permuted_block_56bits += key_56bits[position]

        # 2. Removes parity bits again
        blocks_6bits = []
        for i in range(8):
            # Divide into 8 groups of 7 bits
            block_7bits = permuted_block_56bits[i * 7 : (i + 1) * 7]
            # 3. Assuming parity bit convention: Remove parity bit (first bit of each block)
            block_6bits = block_7bits[1:]
            blocks_6bits.append(block_6bits)

        subkey = "".join(blocks_6bits)
        return subkey

    def expansion(self, block_32bits: str):
        """Expansion of 32-bit block to 48-bit block according to the DES expansion table.

        Args:
            block_32bits (str): 32-bit block to be expanded.

        Returns:
            str: 48-bit expanded block.
        """
        if len(block_32bits) != 32:
            raise ValueError(
                f"Block size mismatch: expected 32 bits, got {len(block_32bits)} bits."
            )
        return self.permutate(block_32bits, self.expansion_table)

    def p_box(self, block_32bits: str):
        """Permutation of 32-bit block according to the DES P-box table.

        Args:
            block_32bits (str): 32-bit block to be permuted.

        Returns:
            str: 32-bit permuted block.
        """
        if len(block_32bits) != 32:
            raise ValueError(
                f"Block size mismatch: expected 32 bits, got {len(block_32bits)} bits."
            )
        return self.permutate(block_32bits, self.p_box_table)

    def inverse_initial_permutation(self, block_64bits: str):
        """Permutes the 64-bit block according to the DES inverse initial permutation table.

        Args:
            block_64bits (str): The 64-bit block to be permuted.

        Returns:
            str: The 64-bit block after permutation.
        """
        if len(block_64bits) != 64:
            raise ValueError(
                f"Block size mismatch: expected 64 bits, got {len(block_64bits)} bits."
            )
        return self.permutate(block_64bits, self.inverse_initial_permutation_table)


if __name__ == "__main__":
    des_perm = DESPermutation()

    # Test con datos de ejemplo
    test_64bit = "0" * 64  # Bloque de 64 ceros
    test_32bit = "1" * 32  # Bloque de 32 unos
    test_56bit = "01" * 28  # Bloque de 56 bits alternados

    print("Testing DES Permutations...")

    # Test initial permutation
    permuted = des_perm.initial_permutation(test_64bit)
    print(f"Initial permutation: {len(permuted)} bits")

    # Test inverse permutation
    original = des_perm.inverse_initial_permutation(permuted)
    print(f"Inverse works: {test_64bit == original}")

    # Test expansion
    expanded = des_perm.expansion(test_32bit)
    print(f"Expansion: {len(expanded)} bits")

    # Test P-box
    pbox_result = des_perm.p_box(test_32bit)
    print(f"P-box: {len(pbox_result)} bits")

    print("All tests completed!")
