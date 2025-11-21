from random import Random


class DesGenerator:
    def __init__(self, seed=None):
        self.random_generator = Random(seed)

    def random_alphabet(self) -> list[str]:
        """Returns a shuffled alphabet upper string.

        Returns:
            list[str]: A list of shuffled alphabet upper characters.
        """
        alphabet = list("QWERTYUIOPASDFGHJKLZXCVBNM")
        self.random_generator.shuffle(alphabet)
        return alphabet

    def random_permutation(self, input_size: int, output_size: int) -> list[int]:
        """Returns a list of output_size random integers in the range [0, input_size - 1].

        Args:
            input_size (int): The size of the range from which to select the random integers.
            output_size (int): The number of random integers to generate.

        Returns:
            list[int]: A list of output_size random integers.
        """
        return [
            self.random_generator.randint(0, input_size - 1) for _ in range(output_size)
        ]

    def random_permutation_unique(self, size: int) -> list[int]:
        """Returns a list of unique random integers in the range [0, size - 1] of length size.

        Args:
            size (int): The size of the range from which to select the random integers and the length of the returned list.

        Returns:
            list[int]: A list of unique random integers.
        """
        return self.random_generator.sample(range(size), size)

    def inverse_permutation(self, permutation: list[int]) -> list[int]:
        """Returns the inverse of a given permutation.

        Args:
            permutation (list[int]): The permutation to invert.

        Returns:
            list[int]: The inverse permutation.
        """
        inverse_permutation = [0] * len(permutation)
        for i, j in enumerate(permutation):
            inverse_permutation[j] = i
        return inverse_permutation

    def random_bits(self, num_bits: int) -> str:
        """Returns a string of num_bits random bits.

        Args:
            num_bits (int): The number of bits to generate.

        Returns:
            str: A string of num_bits random bits.
        """
        return format(self.random_generator.getrandbits(num_bits), f"0{num_bits}b")


if __name__ == "__main__":
    des_generator = DesGenerator()

    # Test random permutation (no duplicates)
    unique_permutation = des_generator.random_permutation_unique(6)
    print(f"Unique permutation: {unique_permutation}")
    print(f"All unique: {len(set(unique_permutation)) == len(unique_permutation)}")

    # Test random permutation (with duplicates)
    expansion_table = des_generator.random_permutation(4, 8)  # 4→8 bits
    print(f"Expansion table: {expansion_table}")
    print(f"Has duplicates: {len(set(expansion_table)) < len(expansion_table)}")

    # Test random alphabet
    print(f"Shuffle example: {des_generator.random_alphabet()} ")

    # Test random bits
    print(f"Random bits: {des_generator.random_bits(64)}")
