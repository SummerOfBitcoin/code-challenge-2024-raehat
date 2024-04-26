import time
from serializeTransaction import reverse_tx_id, calculate_sha256, add_padding_front

def generateBlockHeader(list, merkleRoot, nonceInt):
    version = "00000020"
    prevBlock = "0000000000000000000000000000000000000000000000000000000000000000"
    timeStamp = reverse_tx_id(format(int(time.time()), 'x'))
    bits = "1f00ffff"
    nonce = add_padding_front(reverse_tx_id(format(nonceInt, 'x')), 8)
    return version + prevBlock + reverse_tx_id(merkleRoot) + timeStamp + reverse_tx_id(bits) + nonce

def calculateMerkleRoot(list):
    if (len(list) == 1):
        return list[0]
    newList = []
    i = 0
    while i < len(list) - 1:
        item = reverse_tx_id(calculate_sha256(calculate_sha256(reverse_tx_id(list[i]) + reverse_tx_id(list[i + 1]))))
        newList.append(item)
        i += 2
    if (len(list) % 2 == 1):
        item = reverse_tx_id(calculate_sha256(calculate_sha256(reverse_tx_id(list[-1]) + reverse_tx_id(list[-1]))))
        newList.append(item)
    return calculateMerkleRoot(newList)
