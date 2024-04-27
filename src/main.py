import os
from collections import defaultdict
from transaction import Transaction
from serializeTransaction import serializedTransaction, calculate_sha256, reverse_tx_id, verifyTx, calculateWTXID
from blockheader import generateBlockHeader, calculateMerkleRoot
from coinbase import generateCoinbaseTx
folder_path = "mempool"

# def isLegacy(tx: Transaction):
#     for i in range(len(tx.vin)):
#         if (tx.vin[i].prevout.scriptpubkey_type == "p2p")
#     tx.vin[0].prevout.scriptpubkey_type == "p2pkh"

def validateMempoolTransactions():
    f = True
    d = defaultdict(int)
    cnt = 0
    pnt = 0
    ns = set()
    verifiedTxList = []
    wtxids = ["0000000000000000000000000000000000000000000000000000000000000000"]
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
    
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                if True:
                # if filename == "ff907975dc0cfa299e908e5fba6df56c764866d9a9c22828824c28b8e4511320.json":
                    #     cnt += 1
                    #     continue
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
                            if (len(Transaction(data).vin)) == 1 and Transaction(data).vin[0].prevout.scriptpubkey_type == "p2pkh":
                                verifiedTxList.append(reverse_tx_id(txId))
                                wtxids.append(reverse_tx_id(txId))
                                # if (cnt > 20):
                                #     print(filename)
                            if (len(Transaction(data).vin)) == 1 and Transaction(data).vin[0].prevout.scriptpubkey_type == "v0_p2wpkh":
                                verifiedTxList.append(reverse_tx_id(txId))
                                wtxids.append(calculateWTXID(Transaction(data)))
                                # if (cnt > 20):
                                #     print(filename)
                            cnt += 1
                        else:
                            pnt += 1
                    # else:
                    #     print("not equal: ", filename, sfilename)
                    #     print(txData)
            # if (cnt > 50):
            #     break
            
                    
    # print(cnt)
    # print(pnt)
    return (verifiedTxList, wtxids)

def mineBlock():
    list = []
    vmt = validateMempoolTransactions()
    print('merkleroot: ', reverse_tx_id(calculateMerkleRoot(vmt[1])))
    print('merklecomm: ', calculate_sha256(calculate_sha256(reverse_tx_id(calculateMerkleRoot(vmt[1])) + "0000000000000000000000000000000000000000000000000000000000000000")))
    mrcoinbase = calculate_sha256(calculate_sha256(reverse_tx_id(calculateMerkleRoot(vmt[1])) + "0000000000000000000000000000000000000000000000000000000000000000"))
    cb = generateCoinbaseTx(mrcoinbase)
    list.append(reverse_tx_id(calculate_sha256(calculate_sha256(cb[1]))))

    newTxs = vmt[0]
    list += newTxs
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
        file.write(blockHeaderData + '\n')
        file.write(cb[0] + '\n')
        for element in list:
            file.write(element + '\n')
    # print(vmt[1])
    # print(cb[0])

print(mineBlock())