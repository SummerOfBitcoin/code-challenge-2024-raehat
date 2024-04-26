from transaction import Transaction
from ecdsa_verify import ecdsa_verify
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
    rawTxData += add_padding_front(remove_first_two_letters(str(hex(len(transaction.vout)))), 2)
    for vout_data in transaction.vout:
        rawTxData += add_padding(reverse_tx_id(remove_first_two_letters(hex(vout_data.value))))
        rawTxData += remove_first_two_letters(hex(int(len(vout_data.scriptpubkey) / 2)))
        rawTxData += vout_data.scriptpubkey
    rawTxData += reverse_tx_id(add_padding_front(remove_first_two_letters(hex(transaction.locktime))))

    return rawTxData

def calculateWTXID(transaction: Transaction):
    rawTxData = ""
    rawTxData += "0" + str(transaction.version) +"000000" + "0001"
    rawTxData += add_padding_front(remove_first_two_letters(str(hex(len(transaction.vin)))), 2)
    for vin_data_idx in range(len(transaction.vin)):
        rawTxData += reverse_tx_id(transaction.vin[vin_data_idx].txid)
        rawTxData += add_padding_front(str(remove_first_two_letters(hex(transaction.vin[vin_data_idx].vout))), 2) + "000000"
        rawTxData += "00"
        rawTxData += "ffffffff"
    rawTxData += add_padding_front(remove_first_two_letters(str(hex(len(transaction.vout)))), 2)
    for vout_data in transaction.vout:
        rawTxData += add_padding(reverse_tx_id(remove_first_two_letters(hex(vout_data.value))))
        rawTxData += remove_first_two_letters(hex(int(len(vout_data.scriptpubkey) / 2)))
        rawTxData += vout_data.scriptpubkey
    for vin_data in transaction.vin:
        rawTxData += "0" + str(len(vin_data.witness))
        for witness_data in vin_data.witness:
            rawTxData += remove_first_two_letters(hex(int(len(witness_data) / 2)))
            rawTxData += witness_data
    rawTxData += reverse_tx_id(add_padding_front(remove_first_two_letters(hex(transaction.locktime))))

    return reverse_tx_id(calculate_sha256(calculate_sha256(rawTxData)))

def verifyTx(transaction: Transaction):
    ans = True
    for i in range(len(transaction.vin)):
        if (transaction.vin[i].prevout.scriptpubkey_type == "p2pkh"):
            ans = ans and not verifyP2PKHTx(transaction, i)
        elif (transaction.vin[i].prevout.scriptpubkey_type == "v0_p2wpkh"):
            ans = ans and not verifyP2WPKHTx(transaction, i)

    return not ans

def verifyP2WPKHTx(transaction: Transaction, i):
    msg = getP2WPKHMessage(transaction, i)
    sign = transaction.vin[i].witness[0][:-2]
    publickey = transaction.vin[i].witness[1]
    return ecdsa_verify(sign, msg, publickey)
    

def verifyP2PKHTx(transaction: Transaction, i):
    msg = getLegacyMessage(transaction, i)
    scriptsig_asm_list = transaction.vin[i].scriptsig_asm.split()
    sign = scriptsig_asm_list[1][:-2]
    publickey = scriptsig_asm_list[3]
    return ecdsa_verify(sign, msg, publickey)

def getP2WPKHMessage(transaction: Transaction, inputtxno):
    version = "0" + str(transaction.version) + "000000"
    inputs = ""
    sequences = ""
    for vin_data_idx in range(len(transaction.vin)):
        inputs += reverse_tx_id(transaction.vin[vin_data_idx].txid)
        inputs += add_padding_front(str(remove_first_two_letters(hex(transaction.vin[vin_data_idx].vout))), 2) + "000000" 
        sequences += "ffffffff"
    hashinputs = calculate_sha256(calculate_sha256(inputs))
    hashsequences = calculate_sha256(calculate_sha256(sequences))
    input = reverse_tx_id(transaction.vin[inputtxno].txid) + add_padding_front(str(remove_first_two_letters(hex(transaction.vin[inputtxno].vout))), 2) + "000000"
    hashinput = calculate_sha256(input)
    scriptcode = "1976a914" + transaction.vin[inputtxno].prevout.scriptpubkey_asm.split()[2] + "88ac"
    amount = add_padding(reverse_tx_id(format(transaction.vin[inputtxno].prevout.value, 'x')))
    sequence = "ffffffff"
    outputs = ""
    for vout_data in transaction.vout:
        outputs += add_padding(reverse_tx_id(remove_first_two_letters(hex(vout_data.value))))
        outputs += remove_first_two_letters(hex(int(len(vout_data.scriptpubkey) / 2)))
        outputs += vout_data.scriptpubkey
    hashoutputs = calculate_sha256(calculate_sha256(outputs))
    locktime = reverse_tx_id(add_padding_front(remove_first_two_letters(hex(transaction.locktime))))
    preimage = version + hashinputs + hashsequences + input + scriptcode + amount + sequence + hashoutputs + locktime + "01000000"
    return calculate_sha256(preimage)
    
def getLegacyMessage(transaction: Transaction, inputtxno):
    rawTxData = ""
    rawTxData += "0" + str(transaction.version) + "000000"
    rawTxData += "0" + str(len(transaction.vin))
    for vin_data_idx in range(len(transaction.vin)):
        rawTxData += reverse_tx_id(transaction.vin[vin_data_idx].txid)
        rawTxData += add_padding_front(str(remove_first_two_letters(hex(transaction.vin[vin_data_idx].vout))), 2) + "000000" 
        if vin_data_idx == inputtxno:
            rawTxData += add_padding_front(remove_first_two_letters(hex(int(len(transaction.vin[vin_data_idx].prevout.scriptpubkey) / 2))), 2)
        else:
            rawTxData += "00"
        if vin_data_idx == inputtxno:
            rawTxData += transaction.vin[vin_data_idx].prevout.scriptpubkey
        else:
            rawTxData += ""
        rawTxData += "ffffffff"
    rawTxData += add_padding_front(remove_first_two_letters(str(hex(len(transaction.vout)))), 2)
    for vout_data in transaction.vout:
        rawTxData += add_padding(reverse_tx_id(remove_first_two_letters(hex(vout_data.value))))
        rawTxData += remove_first_two_letters(hex(int(len(vout_data.scriptpubkey) / 2)))
        rawTxData += vout_data.scriptpubkey
    rawTxData += reverse_tx_id(add_padding_front(remove_first_two_letters(hex(transaction.locktime))))
    rawTxData += "01000000"

    return calculate_sha256(rawTxData)

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

