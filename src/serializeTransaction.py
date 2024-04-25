from transaction import Transaction
import hashlib

def serializedTransaction(transaction: Transaction):
    rawTxData = ""
    rawTxData += "0" + str(transaction.version) + "000000"
    rawTxData += "0" + str(len(transaction.vin))
    for vin_data in transaction.vin:
        rawTxData += reverse_tx_id(vin_data.txid)
        rawTxData += add_padding_front(str(remove_first_two_letters(hex(vin_data.vout))), 2) + "000000" 
        rawTxData += add_padding_front(remove_first_two_letters(hex(int(len(vin_data.scriptsig) / 2))), 2)
        rawTxData += vin_data.scriptsig
        rawTxData += "ffffffff"
    rawTxData += "0" + str(len(transaction.vout))
    for vout_data in transaction.vout:
        rawTxData += add_padding(reverse_tx_id(remove_first_two_letters(hex(vout_data.value))))
        rawTxData += remove_first_two_letters(hex(int(len(vout_data.scriptpubkey) / 2)))
        rawTxData += vout_data.scriptpubkey
    rawTxData += reverse_tx_id(add_padding_front(remove_first_two_letters(hex(transaction.locktime))))

    return rawTxData

def reverse_tx_id(input_string):
    if len(input_string) % 2 == 1:
        input_string = "0" + input_string
    input_list = list(input_string)
    i = 0
    j = len(input_list) - 2
    while i < j:
        input_list[i], input_list[j] = input_list[j], input_list[i]
        input_list[i + 1], input_list[j + 1] = input_list[j + 1], input_list[i + 1]
        i += 2
        j -= 2
        
    return ''.join(input_list)

def add_padding(input_string, fixed_len = 16):
    num_zeros = fixed_len - len(input_string)
    padded_string = input_string + '0' * num_zeros 
    return padded_string

def add_padding_front(input_string, fixed_len = 8):
    num_zeros = fixed_len - len(input_string)
    padded_string = '0' * num_zeros + input_string
    return padded_string

def reverse_string(input_string):
    return input_string[::-1]

def remove_first_two_letters(input_string):
    return input_string[2:]

def calculate_sha256(hex_input):
    input_bytes = bytes.fromhex(hex_input)
    
    sha256_hash = hashlib.sha256(input_bytes).hexdigest()
    
    return sha256_hash