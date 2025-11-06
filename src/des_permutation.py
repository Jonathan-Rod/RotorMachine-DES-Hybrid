class DESPermutation:
    def __init__(self):
        pass

    def initial_permutation(self, block_64bits):
        # TODO Initial permutation of block_64bits
        # returns 64-bit
        pass

    def permuted_choice_1(self):
        # TODO Permutation of 64-bit key
        # returns 56-bit
        pass

    def permuted_choice_2(self):
        # TODO Permutation of 56-bit key
        # returns 48-bit (subkey for round i)
        pass

    def e_table(self, block_32bits):
        # TODO Expansion of 32-bit
        # returns 48-bit
        pass

    def p_box(self, block_32bits):
        # TODO P-box permutation of 32-bit
        # returns pbox_32bits
        pass

    def inverse_initial_permutation(self, block_64bits):
        # TODO Inverse initial permutation of 64-bit ciphertext
        # returns 64-bit (ciphertext block)
        pass
