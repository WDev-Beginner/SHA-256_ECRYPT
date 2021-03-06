# for every chunk of 512 bits of our data 

# parse into 16 word array of 32 bits each
# add 48 32-bit words(0) to get a 64 word array 
# perform:
'''
s0 = (w[i-15] rightrotate 7) xor (w[i-15] rightrotate 18) xor (w[i-15] rightshift 3)
s1 = (w[i- 2] rightrotate 17) xor (w[i- 2] rightrotate 19) xor (w[i- 2] rightshift 10)
w[i] = w[i-16] + s0 + w[i-7] + s1
'''
# parse input into 512 chunks
def parse_512_chunks(input):
    chunks, chunk_size = len(input), 512
    return [ input[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]

# parse chunks to 32bit long words, 64 words in total 
def parse_32bit_words(input):
    padded_input = input.ljust(2048, '0')
    chunks, chunk_size = len(padded_input), 32
    return [ padded_input[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]

# preform right rotation of bin
def right_rotate(bin_num, rotation_size):
    int_num = int(bin_num, 2)
    rotated = (int_num >> rotation_size)|(int_num << (32 - rotation_size)) & 0xFFFFFFFF
    return bin(rotated).replace('0b', '').rjust(32, '0')

# perform right shift of bin
def right_shift(bin_num, shift_size):
    int_num = int(bin_num, 2)
    shifted = int_num >> shift_size
    return bin(shifted).replace('0b', '').rjust(32, '0')

# perform xor between two elements
def perform_xor_2(bin_num1, bin_num2):
    y=int(bin_num1,2) ^ int(bin_num2,2) 
    return bin(y).replace('0b', '').rjust(32, '0')

# perform xor between three elements
def perform_xor_3(bin_num1, bin_num2, bin_num3):
    y=int(bin_num1,2) ^ int(bin_num2,2) ^ int(bin_num3,2) 
    return bin(y).replace('0b', '').rjust(32, '0')

# perform modular addition (2^32) of two bins
def perform_modular_addition(bin_nums):
    int_total = 0
    for bin_num in bin_nums:
        int_total += int(bin_num, 2)
    modulated_total = int_total % (2**32)
    return bin(modulated_total).replace('0b', '').rjust(32, '0')

'''
params: 512bit long bin, parsed into 64-32bit long words
return: 512bit long bin, parsed into 64-32bit long words 
        appyling operation described above on them
'''
def convert_chunk_to_message_schedule(chunk):
    s0 = ""
    s1 = ""
    for i in range(16, 64): 
       s0 = perform_xor_3(right_rotate(chunk[i-15], 7), right_rotate(chunk[i-15], 18), right_shift(chunk[i-15], 3))
       s1 = perform_xor_3(right_rotate(chunk[i-2], 17), right_rotate(chunk[i-2], 19), right_shift(chunk[i-2], 10)) 
       to_sum = [chunk[i-16],s0,chunk[i-7],s1]
       chunk[i] = perform_modular_addition(to_sum)
    return chunk

# perform AND on two bins
def perform_and(bin_num1, bin_num2):
    int_num1 = int(bin_num1, 2)
    int_num2 = int(bin_num2, 2)
    and_op = int_num1 & int_num2
    return bin(and_op).replace('0b', '').rjust(32, '0')

# perform NOT on bin
def perform_negation(bin_num):
    int_num1 = int(bin_num, 2)
    neg_op = ~int_num1 + 2**32
    return bin(neg_op).replace('0b', '').rjust(32, '0')
    


