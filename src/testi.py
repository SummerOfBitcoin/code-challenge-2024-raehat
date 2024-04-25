import os
from collections import defaultdict
from transaction import Transaction
from serializeTransaction import serializedTransaction, calculate_sha256, reverse_tx_id, getLegacyMessage, verifyP2PKHTx, verifyTx, getP2WPKHMessage
folder_path = "../mempool"

def validateMempoolTransactions():
    f = True
    d = defaultdict(int)
    cnt = 0
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
    
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                if (filename == "fd5b2900e4a5177609fe449540814d02efe7eed61dc06113a993dd25446d04d3.json"):
                    data = file.read()
                    print(getP2WPKHMessage(Transaction(data), 0))

validateMempoolTransactions()