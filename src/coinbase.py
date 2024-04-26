# def generateCoinbaseTx(mrcoinbase):
#     rawTx = "010000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff2503233708184d696e656420627920416e74506f6f6c373946205b8160a4256c0000946e0100ffffffff02f595814a000000001976a914edf10a7fac6b32e24daa5305c723f3de58db1bc888ac0000000000000000266a24aa21a9ed"  + mrcoinbase + "0120000000000000000000000000000000000000000000000000000000000000000000000000"
#     rawTxWithoutmf = "01000000010000000000000000000000000000000000000000000000000000000000000000ffffffff2503233708184d696e656420627920416e74506f6f6c373946205b8160a4256c0000946e0100ffffffff02f595814a000000001976a914edf10a7fac6b32e24daa5305c723f3de58db1bc888ac0000000000000000266a24aa21a9ed"  + mrcoinbase + "00000000"
#     return (rawTx, rawTxWithoutmf)

def generateCoinbaseTx(mrcoinbase):
    rawTx = "010000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff2503233708184d696e656420627920416e74506f6f6c373946205b8160a4256c0000946e0100ffffffff02f595814a000000001976a914edf10a7fac6b32e24daa5305c723f3de58db1bc888ac000000000000000020"  + mrcoinbase + "0120000000000000000000000000000000000000000000000000000000000000000000000000"
    rawTxWithoutmf = "01000000010000000000000000000000000000000000000000000000000000000000000000ffffffff2503233708184d696e656420627920416e74506f6f6c373946205b8160a4256c0000946e0100ffffffff02f595814a000000001976a914edf10a7fac6b32e24daa5305c723f3de58db1bc888ac000000000000000020"  + mrcoinbase + "00000000"
    return (rawTx, rawTxWithoutmf)