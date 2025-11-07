class DESPermutation:
    def __init__(self):
        pass

    def initial_permutation(self, block_64bits):
        # Permutation of 64-bit block
        # returns 64-bit

        # DES Initial Permutation table
        initial_permut_table = [
            58, 50, 42, 34, 26, 18, 10, 2,
            60, 52, 44, 36, 28, 20, 12, 4,
            62, 54, 46, 38, 30, 22, 14, 6,
            64, 56, 48, 40, 32, 24, 16, 8,
            57, 49, 41, 33, 25, 17, 9,  1,
            59, 51, 43, 35, 27, 19, 11, 3,
            61, 53, 45, 37, 29, 21, 13, 5,
            63, 55, 47, 39, 31, 23, 15, 7
        ]
        block = block_64bits
    
        # Perform permutation
        permuted = ''
        for pos in initial_permut_table:
            # The permutation table uses 1-based indexing (to match presentation), so subtract 1
            permuted += block[pos-1]

        # Returns 64 bits after initial permutation
        return permuted  


    def permuted_choice_1(self):
        # TODO Permutation of 64-bit key
        # returns 56-bit
        pass

    def permuted_choice_2(self):
        # TODO Permutation of 56-bit key
        # returns 48-bit (subkey for round i)
        pass

    def e_table(self, block_32bits):
        # Expansion of 32-bit
        # returns 48-bit

        E_TABLE = [
            32,  1,  2,  3,  4,  5,
            4,  5,  6,  7,  8,  9,
            8,  9, 10, 11, 12, 13,
            12, 13, 14, 15, 16, 17,
            16, 17, 18, 19, 20, 21,
            20, 21, 22, 23, 24, 25,
            24, 25, 26, 27, 28, 29,
            28, 29, 30, 31, 32,  1
        ]

        expanded_block = ''
        for pos in E_TABLE:
            expanded_block += block_32bits[pos - 1]

        return expanded_block

    def p_box(self, block_32bits):
        # TODO P-box permutation of 32-bit
        # returns pbox_32bits

        pass

    def inverse_initial_permutation(self, block_64bits):
        # Inverse initial permutation of 64-bit ciphertext using the positions where the original bits where before permutation.
        # returns 64-bit (ciphertext block)

        inverse_initial_permut_table = [
        40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9,  49, 17, 57, 25
        ]
    
        block = block_64bits
    
        # Perform inverse permutation
        plaintext = ''
        for pos in inverse_initial_permut_table:
            plaintext += block[pos-1]

        # Return plaintext
        return plaintext
