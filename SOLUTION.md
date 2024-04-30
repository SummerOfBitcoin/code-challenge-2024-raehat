## Design Approach
A valid block consists of a fixed length block header (80 bytes), serialized coinbase transaction, and transaction id of each transaction recorded in that respective block.

Each transaction within the block should be valid, meaning the private key which signed these transactions should own the UTXOs it intends to spend.

First, I checked for valid transactions from mempool. I implemented OP_CHECKSIG within code, and included only valid transactions within my block.

Then, I generated a coinbase transaction. In coinbase transaction, second output should have witness commitment in it's scriptpubkey. So I calculated witness merkle root from all wtxids, then calculated witness commitment from it, and then included it in the coinbase transaction.

For calculating block header, a value for nonce had to be calculated such that block meets the required difficulty level. I applied brute force to search for possible values of nonce, and stop if a desired value is found.

At last, I compiled the block header, serialized coinbase transaction and transaction ids of all valid transactions into a block.

## Implementation Details
Below is the list of functions I wrote and used within my code.

serializedTransaction(transaction: Transaction): This function takes a Transaction object as input and serializes its data into a raw hexadecimal string format.
calculateWTXID(transaction: Transaction): This function calculates the Witness Transaction ID (WTXID) for a given transaction. It constructs a raw transaction string similar to serializedTransaction, but with additional considerations for witness data.
verifyTx(transaction: Transaction): This function verifies a transaction. It iterates through each input of the transaction and depending on the type of script pubkey (p2pkh or v0_p2wpkh), it calls either verifyP2PKHTx or verifyP2WPKHTx.
verifyP2WPKHTx(transaction: Transaction, i): This function verifies a Pay-to-Witness-Public-Key-Hash (P2WPKH) transaction. It extracts the necessary data from the transaction and then calls ecdsa_verify to verify the ECDSA signature.
verifyP2PKHTx(transaction: Transaction, i): This function verifies a Pay-to-Public-Key-Hash (P2PKH) transaction. It extracts the necessary data from the transaction and then calls ecdsa_verify to verify the ECDSA signature.
getP2WPKHMessage(transaction: Transaction, inputtxno): This function constructs the message for verifying a P2WPKH transaction. It generates a pre-image by hashing various components of the transaction data.
getLegacyMessage(transaction: Transaction, inputtxno): This function constructs the message for verifying a legacy (non-segwit) transaction. It generates a pre-image similar to getP2WPKHMessage.
reverse_tx_id(input_string): This function reverses the endianness of a hexadecimal string.
add_padding(input_string, fixed_len): This function adds padding to a hexadecimal string to make it a fixed length.
add_padding_front(input_string, fixed_len): This function adds padding to the front of a hexadecimal string to make it a fixed length.
reverse_string(input_string): This function reverses a string.
remove_first_two_letters(input_string): This function removes the first two characters from a string.
calculate_sha256(hex_input): This function calculates the SHA-256 hash of a hexadecimal input.
getLegacyMessage(transaction, inputtxno): Constructs a message for verifying a legacy (non-segwit) transaction, similar to getP2WPKHMessage.
reverse_tx_id(input_string): Reverses the endianness of a hexadecimal string, often used in Bitcoin-related operations.
add_padding(input_string, fixed_len): Adds padding to a hexadecimal string to make it a fixed length.
add_padding_front(input_string, fixed_len): Adds padding to the front of a hexadecimal string to make it a fixed length.
reverse_string(input_string): Reverses a string.
remove_first_two_letters(input_string): Removes the first two characters from a string.
calculate_sha256(hex_input): Calculates the SHA-256 hash of a hexadecimal input.
txIsP2WPKH(tx): Checks if a transaction is using the Pay-to-Witness-Public-Key-Hash (P2WPKH) script type.
validateMempoolTransactions(): Validates transactions in the mempool folder and returns a list of verified transaction IDs along with their witness transaction IDs.
mineBlock(): Mines a new block using validated transactions. It retrieves validated transactions from the mempool, generates a coinbase transaction, calculates the Merkle root, and iteratively generates a block header until the desired difficulty target is met. Finally, it writes the block header, coinbase transaction, and transaction list to an output file.
generateBlockHeader: This function generates a block header using the provided list of transactions, Merkle root, and nonce. It constructs the block header by combining version, previous block hash, timestamp, bits, and nonce.
calculateMerkleRoot: This function calculates the Merkle root of a list of transaction IDs. It iteratively hashes pairs of transaction IDs until a single root hash is obtained, which represents the Merkle root of all transactions in the list.

## Results and Performance
My algorithm mines a block within seconds, while some other algorithms may even take minutes to mine a block at this difficulty, 
You can mine a block within 10 seconds running this code.

## Conclusion
There is still room for improvement, I am not able to collect maximum fees I can collect, a helper function can be written which helps choose transactions with high fees. 
I learnt almost everything required to complete this assignment from https://learnmeabitcoin.com/ (amazing resource to get started with bitcoin development), other than that I referred to bitcoin stack exchange.
