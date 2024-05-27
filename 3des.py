import itertools

# Tabelas de permutação e S-boxes para o DES
IP = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

FP = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]

E = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]

P = [
    16, 7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2, 8, 24, 14,
    32, 27, 3, 9,
    19, 13, 30, 6,
    22, 11, 4, 25
]

S = [
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
    ],
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
    ],
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
    ],
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
    ],
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
    ],
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 13, 15, 1, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
    ],
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
    ],
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
    ],
]

def permute(block, table):
    """
    Permuta os bits de 'block' de acordo com a tabela 'table'.
    
    Parâmetros:
    - block: Lista de bits a serem permutados.
    - table: Tabela de permutação.
    
    Retorna:
    - Lista de bits permutados.
    """
    return [block[x-1] for x in table]

def substitute_with_sbox(input_bits, sboxes):
    """
    Aplica substituições S-Box a grupos de 6 bits.
    
    Parâmetros:
    - input_bits: Lista de bits de entrada (48 bits).
    - sboxes: Lista de S-Boxes a serem usadas (8 S-Boxes).
    
    Retorna:
    - Lista de 32 bits resultantes das substituições S-Box.
    """
    output_bits = []
    for i in range(8):
        sbox_input = input_bits[i * 6:(i + 1) * 6]
        row = int(f"{sbox_input[0]}{sbox_input[5]}", 2)
        col = int(''.join([str(x) for x in sbox_input[1:5]]), 2)
        sbox_value = sboxes[i][row][col]
        output_bits.extend([int(x) for x in f"{sbox_value:04b}"])
    return output_bits

def feistel(right, key):
    """
    Função Feistel: expansão, XOR, substituição e permutação.
    
    Parâmetros:
    - right: Metade direita do bloco (32 bits).
    - key: Subchave para a rodada atual (48 bits).
    
    Retorna:
    - A saída permutada de 32 bits após as operações Feistel.
    """
    # Expansão: A metade direita (32 bits) é expandida para 48 bits
    expanded = permute(right, E)
    
    # XOR: A metade direita expandida é XORed com a subchave de 48 bits
    xor_result = [expanded[i] ^ key[i] for i in range(48)]
    
    # Substituição (S-Boxes): Aplica as S-Boxes
    sbox_result = substitute_with_sbox(xor_result, S)
    
    # Permutação: Permuta os 32 bits de saída das S-Boxes
    return permute(sbox_result, P)

def des_encrypt_block(block, keys):
    """
    Criptografa um bloco de 64 bits usando DES.
    
    Parâmetros:
    - block: Bloco de 64 bits a ser criptografado.
    - keys: Lista de subchaves (16 subchaves de 48 bits).
    
    Retorna:
    - Bloco de 64 bits criptografado.
    """
    # Permutação inicial
    block = permute(block, IP)
    left, right = block[:32], block[32:]

    # 16 rodadas do DES
    for key in keys:
        new_right = [left[i] ^ x for i, x in enumerate(feistel(right, key))]
        left = right
        right = new_right

    # Permutação final
    return permute(right + left, FP)

def string_to_bit_array(text):
    """
    Converte uma string em um array de bits.
    
    Parâmetros:
    - text: String a ser convertida.
    
    Retorna:
    - Array de bits.
    """
    array = []
    for char in text:
        binval = bin(ord(char))[2:].zfill(8)
        array.extend([int(x) for x in binval])
    return array

def bit_array_to_string(array):
    """
    Converte um array de bits de volta para uma string.
    
    Parâmetros:
    - array: Array de bits a ser convertido.
    
    Retorna:
    - String resultante.
    """
    result = []
    for i in range(0, len(array), 8):
        byte = array[i:i+8]
        result.append(chr(int(''.join([str(x) for x in byte]), 2)))
    return ''.join(result)

def pad(text):
    """
    Adiciona padding ao texto para que seu tamanho seja múltiplo de 8 bytes.
    
    Parâmetros:
    - text: Texto a ser preenchido.
    
    Retorna:
    - Texto com padding.
    """
    while len(text) % 8 != 0:
        text += ' '
    return text

def generate_keys(key):
    """
    Gera 16 subchaves para as 16 rodadas do DES.
    
    Parâmetros:
    - key: Chave principal (64 bits).
    
    Retorna:
    - Lista de 16 subchaves (48 bits cada).
    """
    return [key] * 16  # Simplificação: 16 chaves iguais

def des_encrypt(key, text):
    """
    Encripta um texto usando DES.
    
    Parâmetros:
    - key: Chave de criptografia (8 bytes).
    - text: Texto a ser criptografado.
    
    Retorna:
    - Texto criptografado.
    """
    text = pad(text)
    bit_text = string_to_bit_array(text)
    keys = generate_keys(string_to_bit_array(key))
    encrypted_blocks = []
    for i in range(0, len(bit_text), 64):
        block = bit_text[i:i+64]
        encrypted_block = des_encrypt_block(block, keys)
        encrypted_blocks.extend(encrypted_block)
    return bit_array_to_string(encrypted_blocks)

def des_decrypt(key, text):
    """
    Decripta um texto usando DES.
    
    Parâmetros:
    - key: Chave de decriptografia (8 bytes).
    - text: Texto a ser decriptado.
    
    Retorna:
    - Texto decriptado.
    """
    bit_text = string_to_bit_array(text)
    keys = generate_keys(string_to_bit_array(key))[::-1]
    decrypted_blocks = []
    for i in range(0, len(bit_text), 64):
        block = bit_text[i:i+64]
        decrypted_block = des_encrypt_block(block, keys)
        decrypted_blocks.extend(decrypted_block)
    return bit_array_to_string(decrypted_blocks).strip()

def triple_des_encrypt(key1, key2, key3, text):
    """
    Encripta um texto usando Triple DES (3DES).
    
    Parâmetros:
    - key1: Primeira chave de criptografia (8 bytes).
    - key2: Segunda chave de criptografia (8 bytes).
    - key3: Terceira chave de criptografia (8 bytes).
    - text: Texto a ser criptografado.
    
    Retorna:
    - Texto criptografado com 3DES.
    """
    # Criptografa com a primeira chave
    encrypted = des_encrypt(key1, text)
    # Descriptografa com a segunda chave
    decrypted = des_decrypt(key2, encrypted)
    # Criptografa novamente com a terceira chave
    final_encrypted = des_encrypt(key3, decrypted)
    return final_encrypted

def triple_des_decrypt(key1, key2, key3, text):
    """
    Decripta um texto usando Triple DES (3DES).
    
    Parâmetros:
    - key1: Primeira chave de decriptografia (8 bytes).
    - key2: Segunda chave de decriptografia (8 bytes).
    - key3: Terceira chave de decriptografia (8 bytes).
    - text: Texto a ser decriptado.
    
    Retorna:
    - Texto decriptado com 3DES.
    """
    # Descriptografa com a terceira chave
    decrypted = des_decrypt(key3, text)
    # Criptografa com a segunda chave
    encrypted = des_encrypt(key2, decrypted)
    # Descriptografa novamente com a primeira chave
    final_decrypted = des_decrypt(key1, encrypted)
    return final_decrypted

# Exemplo de uso do 3DES
key1 = 'key12345'  # Primeira chave (8 bytes)
key2 = 'key67890'  # Segunda chave (8 bytes)
key3 = 'keyabcde'  # Terceira chave (8 bytes)
text = 'Hello, World!'

encrypted_3des = triple_des_encrypt(key1, key2, key3, text)
print(f"Encrypted with 3DES: {encrypted_3des}")

decrypted_3des = triple_des_decrypt(key1, key2, key3, encrypted_3des)
print(f"Decrypted with 3DES: {decrypted_3des}")
