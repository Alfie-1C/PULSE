
PULSE - Personal AI workflow tool Assistaint. Desgin for local-first anbd sercure by system

Pulse is a personal workflow assistant you can run locally or expose securely over VPN if you know what you’re doing. It’s designed for people who want AI superpowers without giving up data ownership.

Local-first: keep your data on your machine.
Hackable: you can swap models, tweak prompts, add tools.
Secure by default: encryption at rest, minimal logs, explicit consent for any network use.


Why?

In a world where AI + data = everything, you shouldn’t have to trade privacy for convenience. Pulse helps you automate, summarize, draft, and organize—while giving you control over where data lives and how it’s protected.

How does it work?

LLM: Runs with ollama 3.2 (lightweight) so it works on most PCs and laptop

Speech:
SST using openAI whipser (local engine to use)
TTS currently use GTTS will be changed later 

Sercuity:
Uses AES-256 at rest via standard laibaries cryptography
Argon2/brcypt passowrd hashing for local auth
Keys loaded from env vars or prompted at runtime

Connectivity
Local only by deafualt 
Optional VPN exposure for remote access
Any external API usage is explicitly opt-in

The modes:
Local-Only (Default): all inference + storage stays on your device.
Privacy-Aware Hybrid: you pick which parts can call out (e.g., gTTS) and see a clear banner when network is used.
Remote via VPN: run on a home server and connect over your own VPN.

Security & Data Handling (basic)

Authentication: local user w/ hashed password (Argon2/bcrypt).

Encryption at Rest: AES-256 (GCM/Fernet) for configs, memory store, logs.
Key Management: keys derived from passphrase at startup or read from PULSE_MASTER_KEY env var; never stored plaintext.
Logging: minimal, sanitized, and encrypted; toggleable from the UI.
Network Policy: outbound calls off by default; any cloud call requires explicit consent and is visibly flagged.
Delete Button: one-click secure wipe for local store (overwritable pass recommended on SSD/HDD where practical).
