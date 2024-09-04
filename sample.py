import numpy as np

def unpack_nbit_to_16bit(packed_array, n, endian='big'):
    # Convert the bytearray to a NumPy array for easier manipulation
    packed_array = np.frombuffer(packed_array, dtype=np.uint8)

    # Handle endianness by flipping the array if needed
    if endian == 'little':
        packed_array = packed_array[::-1]

    # Calculate the number of n-bit values in the packed array
    total_bits = len(packed_array) * 8
    num_values = total_bits // n
    
    # Initialize an empty array to hold the unpacked 16-bit values
    unpacked_array = np.zeros(num_values, dtype=np.uint16)
    
    # Bit position in the packed data
    bit_pos = 0
    unpacked_idx = 0
    max_value = (1 << n) - 1  # Mask for n-bit values
    
    for i in range(num_values):
        # Find which byte the n-bit value starts in
        start_byte = bit_pos // 8
        end_byte = (bit_pos + n - 1) // 8  # The byte in which the n-bit value ends
        
        # Calculate the offset within the start_byte
        start_offset = bit_pos % 8
        
        if start_byte == end_byte:
            # The n-bit value is contained within a single byte
            unpacked_value = (packed_array[start_byte] >> start_offset) & max_value
        else:
            # The n-bit value spans two bytes
            low_part = int(packed_array[start_byte]) >> start_offset
            high_part = int(packed_array[end_byte]) << (8 - start_offset)
            unpacked_value = (low_part | high_part) & max_value
        
        unpacked_array[unpacked_idx] = unpacked_value
        unpacked_idx += 1
        bit_pos += n
    
    # Handle little-endian conversion by reversing the array again if needed
    if endian == 'little':
        unpacked_array = unpacked_array[::-1]
    
    return unpacked_array

# Example usage:
packed_data = bytearray([0b00001111, 0b10001111, 0b11000011])
n = 10
unpacked_data_big_endian = unpack_nbit_to_16bit(packed_data, n, endian='big')
unpacked_data_little_endian = unpack_nbit_to_16bit(packed_data, n, endian='little')

print("Big Endian:", unpacked_data_big_endian)
print("Little Endian:", unpacked_data_little_endian)
