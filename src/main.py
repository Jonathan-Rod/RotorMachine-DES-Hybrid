from rotor_machine import RotorMachine
from hybrid_cryptosystem import HybridCryptosystem
from des_encryption import DESEncryption
from des_parser import DESParser
from des_generator import DesGenerator
from des_bit_converter import DESBitConverter
from des_permutation import DESPermutation


def run_split_into_blocks_test():
    """Runs a test to check if the DESParser can correctly split a binary string into blocks of size block_size.

    Returns:
        bool: True if the DESParser correctly split the binary string, False otherwise.
    """
    des_parser = DESParser(block_size=3)  # Using custom block size
    test_binary_string = "0100100001100101011011000110110001101111"  # "Hello" in binary
    blocks = des_parser.split_into_blocks(test_binary_string)
    expected_blocks = [
        "010",
        "010",
        "000",
        "110",
        "010",
        "101",
        "101",
        "100",
        "011",
        "011",
        "000",
        "110",
        "111",
        "1",
    ]
    return blocks == expected_blocks


def run_parse_test():
    """Runs a test to check if the DESParser can correctly parse a binary string into blocks of size block_size.

    Returns:
        bool: True if the DESParser correctly parsed the binary string, False otherwise.

    """
    des_parser = DESParser()  # Default block size is 64
    test_binary_string = "0100100001100101011011000110110001101111"  # "Hello" in binary
    blocks = des_parser.parse(test_binary_string)
    expected_blocks = ["0100100001100101011011000110110001101111" + "00000011" * 3]
    return blocks == expected_blocks


def run_deparse_test():
    """Runs a test to check if the DESParser can correctly deparsed blocks back into a binary string.

    Returns:
        bool: True if the deparsed binary string matches the expected binary string, False otherwise.
    """
    des_parser = DESParser()  # Default block size is 64
    # Hello with padding of 3 bytes (00000011)
    blocks = ["0100100001100101011011000110110001101111" + "00000011" * 3]
    deparsed = des_parser.deparse(blocks)
    expected_deparsed = "0100100001100101011011000110110001101111"  # "Hello" in binary
    return deparsed == expected_deparsed


def des_parser_test():
    """Runs three tests to check if the DESParser can correctly split a binary string into blocks, parse a binary string into blocks, and deparsed blocks back into a binary string. Prints the result of each test.

    Returns:
        bool: True if all three tests pass, False otherwise.
    """
    if not run_split_into_blocks_test():
        print("Split into blocks test failed.")
        return False
    print("Split into blocks test passed.")
    if not run_parse_test():
        print("Parse test failed.")
        return False
    print("Parse test passed.")
    if not run_deparse_test():
        print("Deparse test failed.")
        return False
    print("Deparse test passed.")
    return True


def run_string_to_binary_test():
    """Runs a test to check if the DESBitConverter can correctly convert a string to a binary string.

    Returns:
        bool: True if the converted binary string matches the expected binary string, False otherwise.
    """
    des_bit_converter = DESBitConverter()
    test_string = "Hello"
    binary = des_bit_converter.str_to_binary(test_string)
    expected_binary = "0100100001100101011011000110110001101111"
    return binary == expected_binary


def run_binary_to_string_test():
    """Runs a test to check if the DESBitConverter can correctly convert a binary string back into the original string.

    Returns:
        bool: True if the converted string matches the expected string, False otherwise.
    """
    des_bit_converter_test = DESBitConverter()
    test_binary = "0100100001100101011011000110110001101111"
    string = des_bit_converter_test.binary_to_str(test_binary)
    expected_string = "Hello"
    return string == expected_string


def des_bit_converter_test():
    """Runs two tests to check if the DESBitConverter can correctly convert a string to a binary string and back into the original string. Prints the result of each test.

    Returns:
        bool: True if both tests pass, False otherwise."""
    if not run_string_to_binary_test():
        print("String to binary test failed.")
        return False
    print("String to binary test passed.")

    if not run_binary_to_string_test():
        print("Binary to string test failed.")
        return False
    print("Binary to string test passed.")

    return True


def run_initial_permutation_test(des_perm: DESPermutation, test_block_64bits: str):
    """
    Runs a test to check if the DESPermutation class can correctly permute a 64-bit block according to the DES initial permutation table.

    Args:
        des_perm (DESPermutation): The DESPermutation object to be tested.
        test_block_64bits (str): The 64-bit block to be tested.

    Returns:
        bool: True if the permuted block matches the expected permuted block, False otherwise.
    """
    permuted = des_perm.initial_permutation(test_block_64bits)
    expected_permuted = (
        "0001111100000000000111101111001000000000000111100001110111110000"
    )
    return permuted == expected_permuted


def run_des_permutated_choice_1_test(des_perm: DESPermutation, test_block_64bits: str):
    """Runs a test to check if the DESPermutation class can correctly permute a 64-bit block according to the DES permutation choice 1 table.

    Args:
        des_perm (DESPermutation): The DESPermutation object to be tested.
        test_block_64bits (str): The 64-bit block to be tested.

    Returns:
        bool: True if the DESPermutation class can correctly permute the 64-bit block, False otherwise.
    """
    permuted, parity = des_perm.permuted_choice_1(test_block_64bits)
    expected_permuted = "00000000000111110001111000001111000000011110000111010000"
    expected_parity = "01001111"
    return permuted == expected_permuted and parity == expected_parity


def run_des_permutated_choice_2_test(des_perm: DESPermutation, test_block_56bits: str):
    """Runs a test to check if the DESPermutation class can correctly permute a 56-bit key according to the DES permutation choice 2 table.

    Args:
        des_perm (DESPermutation): The DESPermutation object to be tested.
        test_block_56bits (str): The 56-bit block to be tested.

    Returns:
        bool: True if the DESPermutation class can correctly permute the 56-bit block, False otherwise.
    """
    permuted = des_perm.permuted_choice_2(test_block_56bits)
    expected_permuted = "01110100101100000011010011001000001110110"
    return permuted == expected_permuted


def run_expansion_test(des_perm: DESPermutation, test_block_32bits: str):
    """Runs a test to check if the DESPermutation class can correctly expand a 32-bit block according to the DES expansion table.

    Args:
        des_perm (DESPermutation): The DESPermutation object to be tested.
        test_block_32bits (str): The 32-bit block to be tested.

    Returns:
        bool: True if the DESPermutation class can correctly expand the 32-bit block, False otherwise.
    """
    expanded = des_perm.expansion(test_block_32bits)
    expected_expanded = "001001010000001100001010101101011000001101011000"
    return expanded == expected_expanded


def run_p_box_test(des_perm: DESPermutation, test_block_32bits: str):
    """Runs a test to check if the DESPermutation class can correctly perform DES P-box permutation.

    Args:
        des_perm (DESPermutation): The DESPermutation object to be tested.
        test_block_32bits (str): The 32-bit block to be tested.

    Returns:
        bool: True if the DESPermutation class can correctly perform DES P-box permutation, False otherwise.
    """
    p_boxed = des_perm.p_box(test_block_32bits)
    expected_p_boxed = "10011000000111011001010010101100"
    return p_boxed == expected_p_boxed


def run_inverse_initial_permutation_test(
    des_perm: DESPermutation, test_block_64bits: str
):
    """Runs a test to check if the DESPermutation class can correctly perform DES inverse initial permutation.

    Args:
        des_perm (DESPermutation): The DESPermutation object to be tested.
        test_block_64bits (str): The 64-bit block to be tested.

    Returns:
        bool: True if the DESPermutation class can correctly perform DES inverse initial permutation, False otherwise.
    """
    initial_permuted = des_perm.initial_permutation(test_block_64bits)
    inv_permuted = des_perm.inverse_initial_permutation(initial_permuted)
    expected_inv_permuted = test_block_64bits
    return inv_permuted == expected_inv_permuted


def des_permutation_test():
    """Runs multiple tests to check if the DESPermutation class can correctly perform DES initial permutation, DES permutation choice 1, DES permutation choice 2, DES expansion, DES P-box, and DES inverse initial permutation. Prints the result of each test.

    Returns:
        bool: True if all tests pass, False otherwise.
    """
    test_block_64bits = "0100100001100101011011000110110001101111" + "00000011" * 3

    # "01001000011001010110110001101100011011110000001100000011"
    test_block_56bits = test_block_64bits[:56]

    # "01001000011001010110110001101100"
    test_block_32bits = test_block_64bits[:32]

    initial_permutation_table = [
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
        56,
        48,
        40,
        32,
        24,
        16,
        8,
        0,
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
    ]

    expansion_table = [
        31,
        0,
        1,
        2,
        3,
        4,
        3,
        4,
        5,
        6,
        7,
        8,
        7,
        8,
        9,
        10,
        11,
        12,
        11,
        12,
        13,
        14,
        15,
        16,
        15,
        16,
        17,
        18,
        19,
        20,
        19,
        20,
        21,
        22,
        23,
        24,
        23,
        24,
        25,
        26,
        27,
        28,
        27,
        28,
        29,
        30,
        31,
        0,
    ]

    inverse_initial_permutation_table = [
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
        32,
        0,
        40,
        8,
        48,
        16,
        56,
        24,
    ]

    permuted_choice_1_table = [
        # 56 bits de clave
        56,
        48,
        40,
        32,
        24,
        16,
        8,
        0,
        57,
        49,
        41,
        33,
        25,
        17,
        9,
        1,
        58,
        50,
        42,
        34,
        26,
        18,
        10,
        2,
        59,
        51,
        43,
        35,
        62,
        54,
        46,
        38,
        30,
        22,
        14,
        6,
        61,
        53,
        45,
        37,
        29,
        21,
        13,
        5,
        60,
        52,
        44,
        36,
        28,
        20,
        12,
        4,
        27,
        19,
        11,
        3,
        # 8 bits de paridad
        7,
        15,
        23,
        31,
        39,
        47,
        55,
        63,
    ]

    permuted_choice_2_table = [
        5,
        24,
        38,
        37,
        54,
        27,
        15,
        1,
        52,
        45,
        29,
        8,
        18,
        26,
        20,
        6,
        31,
        12,
        19,
        51,
        22,
        33,
        17,
        34,
        16,
        9,
        42,
        30,
        10,
        4,
        46,
        41,
        44,
        25,
        50,
        43,
        14,
        2,
        35,
        49,
        36,
        55,
        11,
        13,
        48,
        28,
        21,
        7,
    ]

    p_box_table = [
        15,
        6,
        19,
        20,
        28,
        11,
        27,
        16,
        0,
        14,
        22,
        25,
        4,
        17,
        30,
        9,
        1,
        7,
        23,
        13,
        31,
        26,
        2,
        8,
        18,
        12,
        29,
        5,
        21,
        10,
        3,
        24,
    ]

    des_permutation = DESPermutation(
        initial_permutation_table,
        inverse_initial_permutation_table,
        expansion_table,
        permuted_choice_1_table,  # NOTE includes parity bits
        permuted_choice_2_table,
        p_box_table,
    )

    if not run_initial_permutation_test(des_permutation, test_block_64bits):
        print("Initial permutation test failed.")
        return False
    print("Initial permutation test passed.")

    if not run_des_permutated_choice_1_test(des_permutation, test_block_64bits):
        print("DES permutated choice 1 test failed.")
        return False
    print("DES permutated choice 1 test passed.")

    if not run_des_permutated_choice_2_test(des_permutation, test_block_56bits):
        print("DES permutated choice 2 test failed.")
        return False
    print("DES permutated choice 2 test passed.")

    if not run_expansion_test(des_permutation, test_block_32bits):
        print("Expansion test failed.")
        return False
    print("Expansion test passed.")

    if not run_p_box_test(des_permutation, test_block_32bits):
        print("P-box test failed.")
        return False
    print("P-box test passed.")

    if not run_inverse_initial_permutation_test(des_permutation, test_block_64bits):
        print("Inverse initial permutation test failed.")
        return False
    print("Inverse initial permutation test passed.")
    return True


def run_des_encryption_test():
    """Runs a test to check if the DES encryption class can correctly encrypt and decrypt a string.

    Encrypts a test string using the DES encryption class, decrypts the result, and checks if the decrypted string matches the original string.

    Returns:
        bool: True if the test passes, False otherwise."""
    des_encryption = DESEncryption()
    test_string = "Run DES test."
    encrypted = des_encryption.encrypt(test_string)
    decrypted = des_encryption.decrypt(encrypted)
    return test_string == decrypted


def des_test():
    """Runs a test to check if the DES encryption class can correctly encrypt and decrypt a string.

    Returns:
        bool: True if the test passes, False otherwise."""
    if not run_des_encryption_test():
        print("DES encryption test failed.")
        return False
    print("DES encryption test passed.")

    return True


def run_default_rotor_machine_test():
    """Runs a test to check if the default rotor machine can correctly encrypt and decrypt a string.

    Returns:
        bool: True if the test passes, False otherwise."""
    rotor_machine = RotorMachine()
    test_string = "Run default rotor machine test."
    encrypted = rotor_machine.encrypt(test_string)
    decrypted = rotor_machine.decrypt(encrypted)
    return test_string == decrypted


def run_custom_rotor_machine_test():
    """Runs a test to check if a custom rotor machine can correctly encrypt and decrypt a string.

    Returns:
        bool: True if the test passes, False otherwise."""
    des_generator = DesGenerator()
    custom_rotor1 = des_generator.random_all_ascii()
    custom_rotor2 = des_generator.random_all_ascii()
    custom_rotor3 = des_generator.random_all_ascii()
    rotor_machine = RotorMachine(
        rotor1=custom_rotor1, rotor2=custom_rotor2, rotor3=custom_rotor3
    )
    test_string = "Run custom rotor machine test."
    encrypted = rotor_machine.encrypt(test_string)
    decrypted = rotor_machine.decrypt(encrypted)
    print(encrypted)
    print(decrypted)
    return test_string == decrypted


def rotor_machine_test():
    """Runs two tests to check if the rotor machine can correctly encrypt and decrypt a string using both default and custom rotor settings. Prints the result of each test.

    Returns:
        bool: True if the test passes, False otherwise."""
    if not run_default_rotor_machine_test():
        print("Default rotor machine test failed.")
        return False
    print("Default rotor machine test passed.")

    if not run_custom_rotor_machine_test():
        print("Custom rotor machine test failed.")
        return False
    print("Custom rotor machine test passed.")

    return True


def run_hybrid_cryptosystem_test():
    hybrid_cryptosystem = HybridCryptosystem()
    test_string = "Run hybrid cryptosystem test."
    encrypted = hybrid_cryptosystem.encrypt(test_string)
    decrypted = hybrid_cryptosystem.decrypt(encrypted)
    return test_string == decrypted


def hybrid_cryptosystem_test():
    """Runs a test to check if the hybrid cryptosystem can correctly encrypt and decrypt a string. Prints the result of the test.

    Returns:
        bool: True if the test passes, False otherwise."""
    if not run_hybrid_cryptosystem_test():
        print("Hybrid cryptosystem test failed.")
        return False
    print("Hybrid cryptosystem test passed.")

    return True


def main():
    """Main entry point for the program. Runs all tests and prints the results of each test."""

    results = []
    print("Running tests...")

    print("\nStarting DES parser test...")
    results.append(des_parser_test())
    print("\nDES parser test completed.")
    print("Passed DES parser test." if results[-1] else "Failed DES parser test.")

    print("\nStarting DES bit converter test...")
    results.append(des_bit_converter_test())
    print("\nDES bit converter test completed.")
    print(
        "Passed DES bit converter test."
        if results[-1]
        else "Failed DES bit converter test."
    )

    print("\nStarting DES permutation test...")
    results.append(des_permutation_test())
    print("\nDES permutation test completed.")
    print(
        "Passed DES permutation test."
        if results[-1]
        else "Failed DES permutation test."
    )

    print("\nStarting DES test...")
    results.append(des_test())
    print("\nDES test completed.")
    print("Passed DES test." if results[-1] else "Failed DES test.")

    print("\nStarting rotor machine test...")
    results.append(rotor_machine_test())
    print("\nRotor machine test completed.")
    print("Passed rotor machine test." if results[-1] else "Failed rotor machine test.")

    print("\nStarting hybrid cryptosystem test...")
    results.append(hybrid_cryptosystem_test())
    print("\nHybrid cryptosystem test completed.")
    print(
        "Passed hybrid cryptosystem test."
        if results[-1]
        else "Failed hybrid cryptosystem test."
    )

    print("\nAll tests completed.")
    passed = sum(1 for result in results if result)
    failed = len(results) - passed
    print(f"\nTest Results: Passed: {passed}, Failed: {failed}")


if __name__ == "__main__":
    main()
