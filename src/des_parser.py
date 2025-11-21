class DESParser:
    def __init__(self, block_size=64):
        self.block_size = block_size

    def split_into_blocks(self, binary_string: str) -> list[str]:
        """
        Splits a binary string into blocks of size self.block_size, without padding.
        The last block may be shorter than the block_size.

        Args:
            binary_string (str): The binary string to split.

        Returns:
            list[str]: A list of binary string blocks.
        """
        return [
            binary_string[i : i + self.block_size]
            for i in range(0, len(binary_string), self.block_size)
        ]

    def parse(self, binary_string: str):
        """Parse a binary string into blocks of size self.block_size.

        Args:
            binary_string (str): The binary string to parse

        Returns:
            list[str]: A list of blocks of size self.block_size

        Notes:
            f the last block is missing 3 bytes, the padding will be b'\x03\x03\x03'.
        """
        # 1. Split into blocks
        blocks_bits = self.split_into_blocks(binary_string)

        # 2. Apply padding to last block if needed
        last_block = blocks_bits[-1]

        # Calculate missing bits
        missing_bits = self.block_size - len(last_block)

        if missing_bits > 0:
            # Calculate how many padding bytes we need
            padding_bytes = missing_bits // 8

            # Create padding (numeric byte repetition)
            padding_byte_value = padding_bytes
            padding_byte = format(padding_byte_value, "08b")
            padding = padding_byte * padding_bytes

            blocks_bits[-1] = last_block + padding

        return blocks_bits

    def deparse(self, blocks_bits: list[str]) -> str:
        """
        Combines the decrypted binary blocks and removes padding from the end.

        Padding is checked by looking at the last byte (8 bits) of the combined
        binary string to determine the padding value (N). If the last N bytes
        match the expected padding pattern, they are removed.

        Args:
            blocks_bits (list[str]): A list of 64-bit decrypted binary blocks.

        Raises:
            ValueError: If any block in the list is not the expected block_size.

        Returns:
            str: The combined binary string with the padding removed, or the original
                 combined string if padding is invalid or not present.
        """
        for i, block_bits in enumerate(blocks_bits):
            if len(block_bits) != self.block_size:
                raise ValueError(
                    f"Block {i} size mismatch: expected {self.block_size} bits, got {len(block_bits)} bits."
                )
        # 1. Combine blocks
        combined = "".join(blocks_bits)
        if len(combined) < 8:
            return combined

        # 2. Check last byte for padding value
        last_byte = combined[-8:]
        padding_value = int(last_byte, 2)

        # 3. Check if padding is correct
        padding_section = combined[-padding_value * 8 :]
        expected_padding = format(padding_value, "08b") * padding_value

        # 4. Remove padding
        if padding_section == expected_padding:
            return combined[: -padding_value * 8]
        else:
            # If padding is not correct, return the original string
            return combined
