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
                # if (filename == "0a8b21af1cfcc26774df1f513a72cd362a14f5a598ec39d915323078efb5a240.json"):
                data = file.read()
                txData = Transaction(data)
                #     print(serializedTransaction(Transaction(data)))
                # data = file.read()
                # rawTx = serializedTransaction(Transaction(data))
                # try:
                #     bytes.fromhex(rawTx)
                # except Exception as e:
                #     continue
                # txId = calculate_sha256(calculate_sha256(rawTx))
                # sfilename = calculate_sha256(reverse_tx_id(txId)) + ".json"
                # if (filename == sfilename):
                d[txData.vin[0].prevout.scriptpubkey_type] += 1
                # if (txData.vin[0].prevout.scriptpubkey_type == "p2pkh"):
                #     print(cnt)
                #     cnt += 1

    for key, value in d.items():
        print("Key:", key, "Value:", value)

validateMempoolTransactions()