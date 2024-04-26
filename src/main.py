import os
from collections import defaultdict
from transaction import Transaction
from serializeTransaction import serializedTransaction, calculate_sha256, reverse_tx_id, verifyTx
from blockheader import generateBlockHeader, calculateMerkleRoot
from coinbase import generateCoinbaseTx
folder_path = "../mempool"

def validateMempoolTransactions():
    f = True
    d = defaultdict(int)
    cnt = 0
    pnt = 0
    ns = set()
    verifiedTxList = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
    
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                data = file.read()
                txData = serializedTransaction(Transaction(data))
                try:
                    bytes.fromhex(txData)
                except Exception as e:
                    continue
                txId = calculate_sha256(calculate_sha256(txData))
                sfilename = calculate_sha256(reverse_tx_id(txId)) + ".json"
                if (sfilename == filename):
                    if verifyTx(Transaction(data)):
                        verifiedTxList.append(txId)
                        cnt += 1
                    else:
                        pnt += 1
    print(cnt)
    print(pnt)
    return verifiedTxList

def mineBlock():
    list = validateMempoolTransactions()
    merkleRoot = calculateMerkleRoot(list)
    nonce = 0
    while (True):
        blockHeaderData = generateBlockHeader(list, merkleRoot, nonce)
        blockHeader = reverse_tx_id(calculate_sha256(calculate_sha256(blockHeaderData)))
        if (int(blockHeader, 16) < int("0000ffff00000000000000000000000000000000000000000000000000000000", 16)):
            break
        nonce += 1

    file_path = "output.txt"
    with open(file_path, 'w') as file:
        file.write(blockHeaderData)
        file.write(generateCoinbaseTx())
        file.write(reverse_tx_id(calculate_sha256(calculate_sha256(generateCoinbaseTx()))))
        for element in list:
            file.write(element)

print(mineBlock())