# Port Scanner Web Application

A modern web application for scanning common TCP and UDP ports on any domain or IP address. Built with Python Flask and a beautiful UI using Tailwind CSS.

## Features

- Scan common TCP and UDP ports
- Support for both domain names and IP addresses
- Modern and responsive user interface
- Real-time scanning results
- Concurrent port scanning for faster results

## Installation

1. Clone this repository
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the application:
   ```bash
   python app.py
   ```
2. Open your web browser and navigate to `http://localhost:5000`
3. Enter a domain name or IP address
4. Select the protocol (TCP or UDP)
5. Click "Start Scan" to begin the port scan

## Security Note

This tool is intended for legitimate network administration and security testing purposes only. Always ensure you have proper authorization before scanning any network or system.

## Common Ports Scanned

### TCP Ports
- 20, 21 (FTP)
- 22 (SSH)
- 23 (Telnet)
- 25 (SMTP)
- 53 (DNS)
- 80 (HTTP)
- 110 (POP3)
- 143 (IMAP)
- 443 (HTTPS)
- 445 (SMB)
- 993 (IMAPS)
- 995 (POP3S)
- 3306 (MySQL)
- 3389 (RDP)
- 5432 (PostgreSQL)
- 8080 (HTTP Alt)

### UDP Ports
- 53 (DNS)
- 67, 68 (DHCP)
- 69 (TFTP)
- 123 (NTP)
- 161, 162 (SNMP)
- 500 (ISAKMP) 