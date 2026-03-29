from typing import TypedDict

class OfferDict(TypedDict):
    type: str  # "offer"
    pub_key: str  # base64
    nonce: str  # random base64
    version: int

class AnswerDict(TypedDict):
    type: str  # "answer"
    pub_key: str  # base64
    nonce: str  # random base64
    version: int

class EncryptedMessageDict(TypedDict):
    ciphertext: str  # base64
    nonce: str  # base64

class PlainTextMessageDict(TypedDict):
    type: str  # "message"
    payload: str
    timestamp: float
