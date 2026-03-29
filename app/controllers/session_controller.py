import os
import time
from core.crypto_engine import CryptoEngine
from core.session import Session, SessionState
from core.message import OfferDict, AnswerDict, EncryptedMessageDict, PlainTextMessageDict
from core.encoder import encode_payload
from core.decoder import decode_payload

class SessionController:
    def __init__(self):
        self.session = Session()

    def generate_offer(self) -> str:
        self.session.initialize()
        self.session.state = SessionState.OFFER_CREATED
        
        offer: OfferDict = {
            "type": "offer",
            "pub_key": CryptoEngine.bytes_to_b64(self.session.local_public_key),
            "nonce": CryptoEngine.bytes_to_b64(os.urandom(12)),
            "version": 1
        }
        return encode_payload(offer)

    def process_offer_generate_answer(self, b64_offer: str) -> str:
        payload = decode_payload(b64_offer)
        if payload.get("type") != "offer":
            raise ValueError("Payload is not an offer")
        
        self.session.initialize()
        self.session.peer_public_key = CryptoEngine.b64_to_bytes(payload["pub_key"])
        self.session.calculate_keys()
        self.session.state = SessionState.CONNECTED
        
        answer: AnswerDict = {
            "type": "answer",
            "pub_key": CryptoEngine.bytes_to_b64(self.session.local_public_key),
            "nonce": CryptoEngine.bytes_to_b64(os.urandom(12)),
            "version": 1
        }
        return encode_payload(answer)

    def process_answer(self, b64_answer: str):
        payload = decode_payload(b64_answer)
        if payload.get("type") != "answer":
            raise ValueError("Payload is not an answer")
        
        self.session.peer_public_key = CryptoEngine.b64_to_bytes(payload["pub_key"])
        self.session.calculate_keys()
        self.session.state = SessionState.CONNECTED
        
    def encrypt_message(self, text: str) -> str:
        if self.session.state != SessionState.CONNECTED or not self.session.derived_key:
            raise ValueError("Session is not connected")
        
        msg_dict: PlainTextMessageDict = {
            "type": "message",
            "payload": text,
            "timestamp": time.time()
        }
        encoded_json = encode_payload(msg_dict)
        
        ciphertext, nonce = CryptoEngine.encrypt_aes_gcm(self.session.derived_key, encoded_json.encode('utf-8'))
        
        enc_dict: EncryptedMessageDict = {
            "ciphertext": CryptoEngine.bytes_to_b64(ciphertext),
            "nonce": CryptoEngine.bytes_to_b64(nonce)
        }
        return encode_payload(enc_dict)

    def decrypt_message(self, b64_encrypted: str) -> dict:
        if self.session.state != SessionState.CONNECTED or not self.session.derived_key:
            raise ValueError("Session is not connected")
            
        enc_dict = decode_payload(b64_encrypted)
        if "ciphertext" not in enc_dict or "nonce" not in enc_dict:
            raise ValueError("Invalid encrypted message format")
            
        ciphertext = CryptoEngine.b64_to_bytes(enc_dict["ciphertext"])
        nonce = CryptoEngine.b64_to_bytes(enc_dict["nonce"])

        decrypted_bytes = CryptoEngine.decrypt_aes_gcm(self.session.derived_key, nonce, ciphertext)
        
        msg_payload_b64 = decrypted_bytes.decode('utf-8')
        return decode_payload(msg_payload_b64)
        
    def reset_session(self):
        self.session = Session()
