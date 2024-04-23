import json

class Transaction:
    def __init__(self, data):
        data = json.loads(data)
        self.version = data["version"]
        self.locktime = data["locktime"]
        self.vin = [self.Input(vin_data) for vin_data in data["vin"]]
        self.vout = [self.Output(vout_data) for vout_data in data["vout"]]

    class Input:
        def __init__(self, vin_data):
            self.txid = vin_data["txid"]
            self.vout = vin_data["vout"]
            self.prevout = self.PrevOut(vin_data["prevout"])
            self.scriptsig = vin_data["scriptsig"]
            self.witness = vin_data["witness"]
            self.is_coinbase = vin_data["is_coinbase"]
            self.sequence = vin_data["sequence"]

        class PrevOut:
            def __init__(self, prevout_data):
                self.scriptpubkey = prevout_data["scriptpubkey"]
                self.scriptpubkey_asm = prevout_data["scriptpubkey_asm"]
                self.scriptpubkey_type = prevout_data["scriptpubkey_type"]
                self.scriptpubkey_address = prevout_data["scriptpubkey_address"]
                self.value = prevout_data["value"]

    class Output:
        def __init__(self, vout_data):
            self.scriptpubkey = vout_data["scriptpubkey"]
            self.scriptpubkey_asm = vout_data["scriptpubkey_asm"]
            self.scriptpubkey_type = vout_data["scriptpubkey_type"]
            self.scriptpubkey_address = vout_data["scriptpubkey_address"]
            self.value = vout_data["value"]