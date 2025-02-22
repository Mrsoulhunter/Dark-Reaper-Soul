# Dark Reaper Soul - Advanced DoS Attack Tool

![Dark Reaper Soul](https://img.shields.io/badge/Status-Legendary-brightgreen)  
*Unleash the Power of Cybersecurity Testing*

Welcome to **Dark Reaper Soul**, a cutting-edge Denial-of-Service (DoS) tool crafted by Ajay Devaliya (@Mrsoulhunter) for ethical red teaming and penetration testing. This tool combines raw TCP SYN floods, HTTP/HTTPS floods, and Slowloris attacks with advanced evasion techniques—obfuscated payloads, randomized headers, and massive concurrency—to push systems to their limits. Built with precision, it’s designed to test network resilience in controlled environments.

> **⚠️ Legal Notice**: This tool is for **authorized testing only**. Unauthorized use is illegal and unethical. Use responsibly.

## Features
- **Multi-Mode Attacks**: Choose from Basic DoS, Firewall Bypass, Full Security Bypass, and Slowloris.
- **Raw SYN Floods**: Powered by `scapy` for layer-4 devastation (admin/root required).
- **HTTPS Mastery**: Socket-level HTTPS floods for modern web targets.
- **Evasion Tactics**: XOR/base64 payload obfuscation, random User-Agents, and spoofed IPs.
- **High Concurrency**: Up to 20,000 threads—overwhelm with style.
- **Proxy Support**: Extendable via `proxies.txt` for stealth.

## Installation
1. **Clone the Repo**:
   ```bash
   git clone https://github.com/Mrsoulhunter/dark-reaper-soul.git
   cd dark-reaper-soul
