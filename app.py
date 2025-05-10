from flask import Flask, render_template, request, jsonify
import socket
import threading
from concurrent.futures import ThreadPoolExecutor
import time
import dns.resolver

app = Flask(__name__)

# Common ports to scan
COMMON_PORTS = {
    'TCP': [20, 21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 993, 995, 3306, 3389, 5432, 8080],
    'UDP': [53, 67, 68, 69, 123, 161, 162, 500]
}

BLACKLISTS = [
    'zen.spamhaus.org',
    'bl.spamcop.net',
    'b.barracudacentral.org',
    'dnsbl.sorbs.net',
    'psbl.surriel.com',
    'dnsbl-1.uceprotect.net',
    'spam.dnsbl.sorbs.net',
    'cbl.abuseat.org',
]

def scan_port(protocol, host, port, timeout=1):
    try:
        if protocol == 'TCP':
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            return {
                'port': port,
                'status': 'open',
                'protocol': protocol
            }
    except:
        pass
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()
    target = data.get('target')
    protocol = data.get('protocol', 'TCP')
    
    if not target:
        return jsonify({'error': 'Target is required'}), 400
    
    try:
        # Resolve domain to IP if needed
        ip = socket.gethostbyname(target)
    except socket.gaierror:
        return jsonify({'error': 'Invalid domain or IP address'}), 400
    
    results = []
    ports_to_scan = COMMON_PORTS.get(protocol, [])
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [
            executor.submit(scan_port, protocol, ip, port)
            for port in ports_to_scan
        ]
        
        for future in futures:
            result = future.result()
            if result:
                results.append(result)
    
    return jsonify({
        'target': target,
        'ip': ip,
        'protocol': protocol,
        'results': results
    })

@app.route('/dns-lookup', methods=['POST'])
def dns_lookup():
    data = request.get_json()
    domain = data.get('domain')
    if not domain:
        return jsonify({'error': 'Domain is required'}), 400
    try:
        answers = dns.resolver.resolve(domain, 'A')
        records = [r.to_text() for r in answers]
        return jsonify({'domain': domain, 'records': records})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/mx-lookup', methods=['POST'])
def mx_lookup():
    data = request.get_json()
    domain = data.get('domain')
    if not domain:
        return jsonify({'error': 'Domain is required'}), 400
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        records = [r.to_text() for r in answers]
        return jsonify({'domain': domain, 'records': records})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def reverse_ip(ip):
    return '.'.join(reversed(ip.split('.')))

@app.route('/blacklist-check', methods=['POST'])
def blacklist_check():
    data = request.get_json()
    target = data.get('target')
    if not target:
        return jsonify({'error': 'Domain or IP is required'}), 400
    try:
        # If domain, resolve to IP
        try:
            ip = socket.gethostbyname(target)
        except Exception:
            ip = target
        reversed_ip = reverse_ip(ip)
        results = []
        for bl in BLACKLISTS:
            query = f"{reversed_ip}.{bl}"
            try:
                dns.resolver.resolve(query, 'A')
                listed = True
            except dns.resolver.NXDOMAIN:
                listed = False
            except Exception:
                listed = 'error'
            results.append({'blacklist': bl, 'listed': listed})
        return jsonify({'target': target, 'ip': ip, 'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True) 