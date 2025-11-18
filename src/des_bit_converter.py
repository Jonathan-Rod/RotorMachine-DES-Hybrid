class DESBitConverter:

    def str_to_binary(self, string):  
        """Convert a ascii string to binary string

        Args:
            string (str): The ascii string to convert

        Returns:
            str: The converted binary string
        """
        return "".join([format(ord(char), "08b") for char in string])

    def binary_to_str(self, binary_string):  
        """Convert a binary string to ascii string

        Args:
            binary_string (str): The binary string to convert

        Returns:
            str: The converted ascii string
        """

        return "".join(
            [
                chr(int(binary_string[i * 8 : i * 8 + 8], 2))
                for i in range(len(binary_string) // 8)
            ]
        )


if __name__ == "__main__":
    converter = DESBitConverter()
    test_string = "Hello"
    binary = converter.str_to_binary(test_string)
    print(f"String to binary: {binary}")
    converted_back = converter.binary_to_str(binary)
    print(f"Binary to string: {converted_back}")
