import os
import base64
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class CryptoEngine:
    @staticmethod
    def generate_x25519_keypair() -> tuple[bytes, bytes]:
        """Generates an X25519 keypair and returns raw bytes (private, public)."""
        private_key = x25519.X25519PrivateKey.generate()
        public_key = private_key.public_key()
        return (private_key.private_bytes_raw(), public_key.public_bytes_raw())

    @staticmethod
    def derive_shared_key(private_bytes: bytes, peer_public_bytes: bytes) -> bytes:
        """Derives a shared key using the local private key and peer's public key."""
        private_key = x25519.X25519PrivateKey.from_private_bytes(private_bytes)
        peer_public_key = x25519.X25519PublicKey.from_public_bytes(peer_public_bytes)
        return private_key.exchange(peer_public_key)

    @staticmethod
    def compute_hkdf(shared_key: bytes, length: int = 32) -> bytes:
        """Derives a symmetric key using HKDF-SHA256 from the shared key."""
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=length,
            salt=None,
            info=b'devdrop_handshake'
        )
        return hkdf.derive(shared_key)

    @staticmethod
    def encrypt_aes_gcm(key: bytes, plaintext: bytes) -> tuple[bytes, bytes]:
        """Encrypts plaintext with AES-GCM and returns ciphertext and nonce."""
        aesgcm = AESGCM(key)
        nonce = os.urandom(12)
        ciphertext = aesgcm.encrypt(nonce, plaintext, None)
        return ciphertext, nonce

    @staticmethod
    def decrypt_aes_gcm(key: bytes, nonce: bytes, ciphertext: bytes) -> bytes:
        """Decrypts AES-GCM given key, nonce, and ciphertext."""
        aesgcm = AESGCM(key)
        return aesgcm.decrypt(nonce, ciphertext, None)

    @staticmethod
    def bytes_to_b64(data: bytes) -> str:
        return base64.b64encode(data).decode('utf-8')
        
    @staticmethod
    def b64_to_bytes(data: str) -> bytes:
        return base64.b64decode(data.encode('utf-8'))
