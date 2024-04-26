import os
from collections import defaultdict
from transaction import Transaction
from serializeTransaction import serializedTransaction, calculate_sha256, reverse_tx_id, getLegacyMessage, verifyP2PKHTx, verifyTx, getP2WPKHMessage, calculateWTXID
folder_path = "mempool"

def validateMempoolTransactions():
    f = True
    d = defaultdict(int)
    cnt = 0
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
    
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                if (filename == "036b0ec9d18d0b23f77eaeafe5b7c48117ce48f8f73b26fd747e0a3e77912eb9.json"):
                    data = file.read()
                    print(calculateWTXID(Transaction(data)))
                # data = file.read()
                # if (len(Transaction(data).vin) > 1 and Transaction(data).vin[0].prevout.scriptpubkey_type == "v0_p2wpkh"):
                #     print(filename)
                #     break


validateMempoolTransactions()