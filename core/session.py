import hashlib
from typing import Optional
from core.crypto_engine import CryptoEngine

class SessionState:
    INIT = "INIT"
    OFFER_CREATED = "OFFER_CREATED"
    ANSWER_CREATED = "ANSWER_CREATED"
    CONNECTED = "CONNECTED"
    CLOSED = "CLOSED"

class Session:
    def __init__(self):
        self.state = SessionState.INIT
        self.local_private_key: Optional[bytes] = None
        self.local_public_key: Optional[bytes] = None
        self.peer_public_key: Optional[bytes] = None
        self.shared_key: Optional[bytes] = None
        self.derived_key: Optional[bytes] = None
        self.session_id: Optional[str] = None
        self.fingerprint: Optional[str] = None

    def initialize(self):
        self.local_private_key, self.local_public_key = CryptoEngine.generate_x25519_keypair()
    
    def calculate_keys(self):
        if self.local_private_key and self.peer_public_key:
            self.shared_key = CryptoEngine.derive_shared_key(self.local_private_key, self.peer_public_key)
            self.derived_key = CryptoEngine.compute_hkdf(self.shared_key)
            self.generate_fingerprint()

    def generate_fingerprint(self):
        if self.local_public_key and self.peer_public_key:
            # Sort keys to ensure both peers generate the exact same string
            keys = sorted([self.local_public_key, self.peer_public_key])
            combined = keys[0] + keys[1]
            digest = hashlib.sha256(combined).hexdigest().upper()
            self.fingerprint = ':'.join(digest[i:i+2] for i in range(0, 32, 2))
