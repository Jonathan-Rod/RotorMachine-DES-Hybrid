from des_generator import DesGenerator


class DESPermutation:
    # NOTE: All tables are 0-indexed
    def __init__(
        self,
        initial_permutation_table: list[int] = None,
        inverse_initial_permutation_table: list[int] = None,
        expansion_table: list[int] = None,
        permuted_choice_1_table: list[
            int
        ] = None,  # NOTE I am assuming that first 56 indexes are the key bits and last 8 indexes are parity bits.
        permuted_choice_2_table: list[int] = None,
        p_box_table: list[int] = None,
    ):
        # DES Initial Permutation table 0-index tables
        self.generator = DesGenerator()

        # initial_permutation_table: 64
        if initial_permutation_table is not None:
            self.initial_permutation_table = initial_permutation_table
        else:
            self.initial_permutation_table = self.generator.random_permutation_unique(
                64
            )

        # inverse_initial_permutation_table: 64
        if inverse_initial_permutation_table is not None:
            self.inverse_initial_permutation_table = inverse_initial_permutation_table
        else:
            self.inverse_initial_permutation_table = self.generator.inverse_permutation(
                self.initial_permutation_table
            )

        # expansion_table: 32 -> 48
        if expansion_table is not None:
            self.expansion_table = expansion_table
        else:
            self.expansion_table = self.generator.random_permutation(32, 48)

        # permuted_choice_1_table: 64 -> 56
        if permuted_choice_1_table is not None:
            self.permuted_choice_1_table = permuted_choice_1_table[:56]
            # TODO unused
            self.permuted_choice_1_parity_bits_table = permuted_choice_1_table[56:]
        else:
            indexes_64 = self.generator.random_permutation_unique(64)
            self.permuted_choice_1_table = indexes_64[:56]
            # TODO unused
            self.permuted_choice_1_parity_bits_table = indexes_64[56:]

        # permuted_choice_2_table: 56
        if permuted_choice_2_table is not None:
            self.permuted_choice_2_table = permuted_choice_2_table
        else:
            self.permuted_choice_2_table = self.generator.random_permutation_unique(56)

        # p_box_table: 32
        if p_box_table is not None:
            self.p_box_table = p_box_table
        else:
            self.p_box_table = self.generator.random_permutation_unique(32)

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
        block_56bits = self.permutate(key_64bits, self.permuted_choice_1_table)
        parity_8bits = self.permutate(
            key_64bits, self.permuted_choice_1_parity_bits_table
        )

        return block_56bits, parity_8bits

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
