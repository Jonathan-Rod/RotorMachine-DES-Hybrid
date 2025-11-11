class DESParser:
    def __init__(self, block_size=64):
        self.block_size = block_size

    def parse(self, binary_string):  # TODO
        """Returns a list of binary string blocks of fixed size.

        Applies padding using a numeric scheme where the number of missing bytes
        is repeated as 8-bit binary values to fill the block.

        Args:
            binary_string (str): The binary string to split into blocks.

        Returns:
            List[str]: List of binary string blocks.
        """
        remainder = len(binary_string) % self.block_size
        padding_bytes = (self.block_size - remainder) // 8 if remainder != 0 else 8

        padding_byte = format(padding_bytes, "08b")
        padding = padding_byte * padding_bytes

        padded_binary = binary_string + padding

        return [
            padded_binary[i : i + self.block_size]
            for i in range(0, len(padded_binary), self.block_size)
        ]

    def deparse(self, binary_string):  # TODO
        """Removes padding from a binary string that was padded using numeric byte repetition.

        Args:
            binary_string (str): The binary string to remove padding from.

        Returns:
            str : The unpadded binary string
        """
        if len(binary_string) < 8:
            return binary_string  # No padding posible

        last_byte = binary_string[-8:]
        padding_value = int(last_byte, 2)

        padding_section = binary_string[-padding_value * 8 :]
        expected_padding = format(padding_value, "08b") * padding_value

        if padding_section == expected_padding:
            return binary_string[: -padding_value * 8]
        else:
            return binary_string  # No se reconoce padding válido, se devuelve todo

    def deparse_blocks(self, blocks):  # TODO
        """Deparses a list of binary string blocks into a single binary string,
        removing padding.

        Verifica que todos los bloques tengan el tamaño correcto antes de unirlos.

        Args:
            blocks (List[str]): List of binary string blocks.

        Returns:
            str: The unpadded binary string.
        """
        for block in blocks:
            if len(block) != self.block_size:
                raise ValueError(
                    f"Block size mismatch: expected {self.block_size} bits, got {len(block)} bits."
                )

        combined = "".join(blocks)
        return self.deparse(combined)


from des_bit_converter import DESBitConverter

if __name__ == "__main__":

    converter = DESBitConverter()

    string = "This is a test string for DESParser. It should handle padding correctly. It should also be able to deparse blocks correctly."

    print(f"Test string: {string}")

    test_binary = converter.str_to_binary(string)
    print(f"Test binary: {test_binary}")

    parser = DESParser()

    blocks = parser.parse(test_binary)
    print(f"Parsed blocks: {blocks}")

    deparsed = parser.deparse_blocks(blocks)
    print(f"Deparsed binary: {deparsed}")

    original_string = converter.binary_to_str(deparsed)
    print(f"Original string: {original_string}")
