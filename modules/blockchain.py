import os
import json

class BlockchainHashSubmitter:
    """Optional transaction helper for a local Ethereum-compatible dev chain."""
    @classmethod
    def from_environment(cls):
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            pass
        return cls()

    def submit_hash(self, digest: str):
        rpc_url = os.getenv("BLOCKCHAIN_URL", "")
        private_key = os.getenv("BLOCKCHAIN_PRIVATE_KEY", "")
        if not rpc_url or not private_key:
            print("Blockchain not configured; set local development values in .env.")
            return None
        try:
            from web3 import Web3
            from eth_account import Account
            w3 = Web3(Web3.HTTPProvider(rpc_url, request_kwargs={"timeout": 5}))
            if not w3.is_connected():
                return None
            account = Account.from_key(private_key)
            # Only the digest is included; no file contents are sent.
            payload = json.dumps({"sha256": digest}, separators=(",", ":")).encode().hex()
            tx = {
                "nonce": w3.eth.get_transaction_count(account.address),
                "to": account.address,
                "value": 0,
                "gas": 100000,
                "gasPrice": w3.eth.gas_price,
                "data": "0x" + payload,
                "chainId": w3.eth.chain_id,
            }
            signed = w3.eth.account.sign_transaction(tx, private_key)
            tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=60)
            return receipt["transactionHash"].hex()
        except ImportError:
            print("Install optional blockchain dependencies from requirements.txt.")
            return None
        except Exception as exc:
            print(f"Blockchain submission failed: {exc}")
            return None
