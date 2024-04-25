import os
from collections import defaultdict
from transaction import Transaction
from serializeTransaction import serializedTransaction, calculate_sha256, reverse_tx_id
folder_path = "../mempool"

def validateMempoolTransactions():
    f = True
    d = defaultdict(int)
    cnt = 0
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
    
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                data = file.read()
                txData = serializedTransaction(Transaction(data))
                txId = calculate_sha256(calculate_sha256(txData))
                sfilename = calculate_sha256(reverse_tx_id(txId)) + ".json"
                if (sfilename == filename):
                    print(cnt)
                    cnt += 1

validateMempoolTransactions()