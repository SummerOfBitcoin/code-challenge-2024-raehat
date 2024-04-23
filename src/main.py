import os
from transaction import Transaction
folder_path = "../mempool"

def validateMempoolTransactions():
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
    
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                data = file.read()
                Transaction(data)
                

validateMempoolTransactions()