class DESPermutation:
    def __init__(self):  # TODO
        # DES Initial Permutation table
        self.init_permutation_table = [
            58,
            50,
            42,
            34,
            26,
            18,
            10,
            2,
            60,
            52,
            44,
            36,
            28,
            20,
            12,
            4,
            62,
            54,
            46,
            38,
            30,
            22,
            14,
            6,
            64,
            56,
            48,
            40,
            32,
            24,
            16,
            8,
            57,
            49,
            41,
            33,
            25,
            17,
            9,
            1,
            59,
            51,
            43,
            35,
            27,
            19,
            11,
            3,
            61,
            53,
            45,
            37,
            29,
            21,
            13,
            5,
            63,
            55,
            47,
            39,
            31,
            23,
            15,
            7,
        ]

        # DES Expansion table
        self.expansion_table = [
            32,
            1,
            2,
            3,
            4,
            5,
            4,
            5,
            6,
            7,
            8,
            9,
            8,
            9,
            10,
            11,
            12,
            13,
            12,
            13,
            14,
            15,
            16,
            17,
            16,
            17,
            18,
            19,
            20,
            21,
            20,
            21,
            22,
            23,
            24,
            25,
            24,
            25,
            26,
            27,
            28,
            29,
            28,
            29,
            30,
            31,
            32,
            1,
        ]

        # DES Inverse Initial Permutation table
        self.inverse_init_permutation_table = [
            40,
            8,
            48,
            16,
            56,
            24,
            64,
            32,
            39,
            7,
            47,
            15,
            55,
            23,
            63,
            31,
            38,
            6,
            46,
            14,
            54,
            22,
            62,
            30,
            37,
            5,
            45,
            13,
            53,
            21,
            61,
            29,
            36,
            4,
            44,
            12,
            52,
            20,
            60,
            28,
            35,
            3,
            43,
            11,
            51,
            19,
            59,
            27,
            34,
            2,
            42,
            10,
            50,
            18,
            58,
            26,
            33,
            1,
            41,
            9,
            49,
            17,
            57,
            25,
        ]

        self.pc2_permutation_table = [
            6,
            25,
            39,
            38,
            55,
            28,
            16,
            2,
            53,
            46,
            30,
            9,
            19,
            27,
            21,
            7,
            32,
            13,
            20,
            52,
            23,
            34,
            18,
            35,
            17,
            10,
            43,
            31,
            11,
            5,
            47,
            42,
            45,
            26,
            51,
            44,
            15,
            3,
            36,
            50,
            37,
            56,
            12,
            14,
            49,
            29,
            22,
            8,
            4,
            33,
            54,
            40,
            24,
            48,
            41,
            1,
        ]

        self.pbox_table = [
            16,
            7,
            20,
            21,
            29,
            12,
            28,
            17,
            1,
            15,
            23,
            26,
            5,
            18,
            31,
            10,
            2,
            8,
            24,
            14,
            32,
            27,
            3,
            9,
            19,
            13,
            30,
            6,
            22,
            11,
            4,
            25,
        ]

        # Inverse tables for decryption processes:

        self.inverse_pc2_permutation_table = [
            56,
            8,
            38,
            49,
            30,
            1,
            16,
            48,
            12,
            26,
            29,
            43,
            18,
            44,
            37,
            7,
            25,
            23,
            13,
            19,
            15,
            47,
            21,
            53,
            2,
            34,
            14,
            6,
            46,
            11,
            28,
            17,
            50,
            22,
            24,
            39,
            41,
            4,
            3,
            52,
            55,
            32,
            27,
            36,
            33,
            10,
            31,
            54,
            45,
            40,
            35,
            20,
            9,
            51,
            5,
            42,
        ]

        self.inverse_pbox_table = [
            9,
            17,
            23,
            31,
            13,
            28,
            2,
            18,
            24,
            16,
            30,
            6,
            26,
            20,
            10,
            1,
            8,
            14,
            25,
            3,
            4,
            29,
            11,
            19,
            32,
            12,
            22,
            7,
            5,
            27,
            15,
            21,
        ]

    def initial_permutation(self, block_64bits: str):
        # Permutation of 64-bit block
        # returns 64-bit

        block = block_64bits

        # Perform permutation
        permuted = ""
        for pos in self.init_permutation_table:
            # The permutation table uses 1-based indexing (to match presentation), so subtract 1
            permuted += block[pos - 1]

        # Returns 64 bits after initial permutation
        return permuted

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
            block = key_64bits[i * 8 : (i + 1) * 8]  # Bloque de 8 bits
            block_without_parity = block[:i] + block[i + 1 :]  # Remove parity bit
            blocks_7bits.append(block_without_parity)

        block_56bits = "".join(blocks_7bits)
        return block_56bits

    def pc2_permutation(self, key_56bits: str):
        # Permutation of the combined 56-bit key from permuted choice 2
        block = key_56bits

        # Perform permutation
        permuted = ""
        for pos in self.pc2_permutation_table:
            # The permutation table uses 1-based indexing (to match presentation), so subtract 1
            permuted += block[pos - 1]

        # Returns 56 bits after initial permutation
        return permuted

    def permuted_choice_2(self, key_56bits: str):
        """Permutes the 56-bit key and concatenates both parts and applies permutation again.
        Removes parity bits and returns 48-bit subkey for round i.

        Args:
            key_56bits (str): The 56-bit key to be permuted.

        Returns:
            str: The 48-bit subkey for round i.
        """
        # TODO #6 Implement Permuted Choice 2

        # TODO Permutation of 56-bit key
        # TODO Concatenate both parts and apply pemutation
        # TODO Removes parity bits again
        # returns 48-bit (subkey for round i)

        # Apply PC-2 permutation
        permuted_key = self.pc2_permutation(key_56bits)

        blocks_6bits = []
        for i in range(8):
            # Divide into 8 groups of 7 bits
            start_index = i * 7
            end_index = (i + 1) * 7
            block = permuted_key[start_index:end_index]
            block_without_parity = block[1:]  # Remove parity bit (firt of each block)
            blocks_6bits.append(block_without_parity)

        subkey = "".join(blocks_6bits)
        return subkey

    def e_table(self, block_32bits: str):
        """Expansion of 32-bit block to 48-bit block according to the DES expansion table.

        Args:
            block_32bits (str): 32-bit block to be expanded.

        Returns:
            str: 48-bit expanded block.
        """
        expanded_block = ""
        for pos in self.expansion_table:
            expanded_block += block_32bits[pos - 1]

        return expanded_block

    def p_box(self, block_32bits: str):
        """Permutation of 32-bit block according to the DES P-box table.

        Args:
            block_32bits (str): 32-bit block to be permuted.

        Returns:
            str: 32-bit permuted block.
        """
        # TODO #7 Implement P-box
        # TODO permutation of 32-bit
        # returns pbox_32bits

        # Perform permutation
        permuted = ""
        for pos in self.pbox_table:
            # The permutation table uses 1-based indexing (to match presentation), so subtract 1
            permuted += block_32bits[pos - 1]

        # Returns 32 bits after initial permutation
        return permuted

    def inverse_initial_permutation(self, block_64bits: str):
        # Inverse initial permutation of 64-bit ciphertext using the positions where the original bits where before permutation.
        # returns 64-bit (ciphertext block)

        block = block_64bits

        # Perform inverse permutation
        plaintext = ""
        for pos in self.inverse_init_permutation_table:
            plaintext += block[pos - 1]

        # Return plaintext
        return plaintext


if __name__ == "__main__":
    permutation = DESPermutation()
    binary_data64 = "0100100001100101011011000110110001101111001000010010000100100001"
    binary_data56 = "01001000011001010110110001101100011011110010000100100001"
    test_left = permutation.left_circular_shift("10001")
    print(test_left)
    print("Binary data:", binary_data56)
    subkey1 = permutation.permuted_choice_2(binary_data56)
    print(subkey1)
