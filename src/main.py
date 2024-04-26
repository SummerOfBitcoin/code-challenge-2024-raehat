import os
from collections import defaultdict
from transaction import Transaction
from serializeTransaction import serializedTransaction, calculate_sha256, reverse_tx_id, verifyTx, calculateWTXID
from blockheader import generateBlockHeader, calculateMerkleRoot
from coinbase import generateCoinbaseTx
folder_path = "mempool"

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
                # if filename == "fd5b2900e4a5177609fe449540814d02efe7eed61dc06113a993dd25446d04d3.json" or filename == "0a8b21af1cfcc26774df1f513a72cd362a14f5a598ec39d915323078efb5a240.json" or filename == "f05466166d2de825fbf32c93f6e4ecb76305dc3dcdef9b8e00c3c2d707c4a6f6.json" or filename == "2681b9decad3256f37c6bc9f3ea5d900839945d4eafc27a7bc4f99db5fadf68d.json":
                # if True:
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
                        verifiedTxList.append(reverse_tx_id(txId))
                        if (Transaction(data).vin[0].prevout.scriptpubkey_type == "p2pkh"):
                            wtxids.append(reverse_tx_id(txId))
                            if (cnt > 20):
                                print(filename)
                        elif (Transaction(data).vin[0].prevout.scriptpubkey_type == "v0_p2wpkh"):
                            wtxids.append(calculateWTXID(Transaction(data)))
                            if (cnt > 20):
                                print(filename)
                        cnt += 1
                    else:
                        pnt += 1
            if (cnt > 29):
                break
            
                    
    # print(cnt)
    # print(pnt)
    return (verifiedTxList, wtxids)

def mineBlock():
    list = []
    vmt = validateMempoolTransactions()
    print('lol: ', calculateMerkleRoot(vmt[1]))
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
    print(vmt[1])
    # print(cb)

print(mineBlock())