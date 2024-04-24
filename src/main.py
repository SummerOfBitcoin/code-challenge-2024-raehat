import os
from transaction import Transaction
from serializeTransaction import serializedTransaction
folder_path = "../mempool"

def validateMempoolTransactions():
    f = True
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
    
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                data = file.read()
                if (filename == "0a8b21af1cfcc26774df1f513a72cd362a14f5a598ec39d915323078efb5a240.json"):
                    print(filename)
                    print(serializedTransaction(Transaction(data)))
                    f = False
                

validateMempoolTransactions()