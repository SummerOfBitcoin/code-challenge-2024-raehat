import os
from collections import defaultdict
from transaction import Transaction
from serializeTransaction import serializedTransaction, calculate_sha256, reverse_tx_id, verifyTx
folder_path = "../mempool"

def validateMempoolTransactions():
    f = True
    d = defaultdict(int)
    cnt = 0
    pnt = 0
    ns = set()
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
                        cnt += 1
                    else:
                        pnt += 1

    print(cnt)
    print(pnt)

validateMempoolTransactions()
