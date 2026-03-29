# DevDrop

DevDrop is a secure desktop application for exchanging sensitive information between two parties without exposing data to any server, centralized authority, or cloud provider. It guarantees that secrets never leave your device unencrypted and operates entirely via an offline-capable, copy/paste manual exchange.

## Features

- **No Backend**: Complete peace of mind knowing there are no cloud configurations or databases retaining metadata.
- **End-to-End Encryption**: Every message is protected via AES-GCM (256-bit capabilities inherently provided through HKDF).
- **Strong Key Exchange**: The secure handshake relies on Elliptic-Curve Diffie-Hellman (`X25519`) and `HKDF-SHA256` key derivation.
- **Visual Fingerprinting**: Helps detect and prevent active Man-In-The-Middle (MITM) attacks.
- **Zero-Dependency Core**: Leverages the robust `cryptography` Python package and nothing else for security. 
- **Modern UI**: Provided by `flet`, supporting local state restoration and pinned window behaviors.

## Installation

Run the following command within the application directory to initialize:

```bash
./init.sh
```

This will:
1. Initialize a localized Python Virtual Environment (`.venv`).
2. Install dependencies (`flet`, `cryptography`).
3. Deploy an executable shortcut (`devdrop`) into your `~/.local/bin` folder. 

After initialization, launch the app directly:
```bash
devdrop
```

Or execute `./run.sh`.

## Usage & Offer/Answer Exchange Flow

DevDrop mimics the `Offer/Answer` flow commonly used in WebRTC, but entirely decoupled from networking protocols.

### 1. The Handshake

- **User A**: Opens the Application, clicks `Create Session`. This generates a Base64-encoded `Offer` representing A's public key (X25519) and session metadata. 
- **User A**: Copies the Base64 Offer string and transmits it to User B (e.g. over Slack, SMS, WhatsApp).
- **User B**: Pastes the `Offer` into the connect section and clicks `Process`. This creates an `Answer` payload.
- **User B**: Sends the generated `Answer` back to User A.
- **User A**: Pastes the `Answer` into the connect section and clicks `Process`. 
- **CONNECTED**: The session status indicates Green. A secure shared symmetric key has been derived for future messages.

### 2. Fingerprint Check (Crucial for preventing MITM)

Upon connection, **both** clients will display a green `Fingerprint` (e.g., `AB:23:9F...`). 
It's highly recommended to verify out-of-band (e.g., via a voice call or secondary channel) that the strings match exactly. 

### 3. Exchanging Secrets

Navigate between the `Send` and `Receive` tabs to exchange secret text payloads.
- **Sending**: Enter text, click `Encrypt & Send`. A `CipherText` Base64 string will be generated. Send this string to your peer.
- **Receiving**: Paste any incoming `CipherText` Base64 into the `Paste Encrypted Message` field and select `Decrypt`. 
- Messages are displayed fully encrypted in the inbox and can be actively toggled/revealed via the eye icon.

## Security Overview

DevDrop was explicitly designed to restrict arbitrary network sockets and remote endpoints. It acts as an isolated translation terminal. Since encryption keys are derived dynamically per session, shutting down the application securely eliminates all transient shared keys from the machine.
