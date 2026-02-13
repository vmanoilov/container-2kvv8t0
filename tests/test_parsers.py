from app.parsers.nmap_parser import parse_nmap_output
from app.parsers.gobuster_parser import parse_gobuster_output
from app.parsers.ffuf_parser import parse_ffuf_output
from app.parsers.nikto_parser import parse_nikto_output

def test_nmap_parser():
    sample_output = """
Starting Nmap 7.80 ( https://nmap.org ) at 2023-01-01 00:00 UTC
Nmap scan report for example.com (93.184.216.34)
Host is up (0.020s latency).
Not shown: 995 closed ports
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
443/tcp  open  https
"""
    findings = parse_nmap_output(sample_output)
    assert len(findings) == 3
    assert findings[0].data['port'] == 22
    assert findings[0].data['service'] == 'ssh'

def test_gobuster_parser():
    sample_output = """
/admin (Status: 200)
/login (Status: 302)
/config (Status: 403)
"""
    findings = parse_gobuster_output(sample_output)
    assert len(findings) == 3
    assert findings[0].data['path'] == 'admin'
    assert findings[0].data['status'] == 200

def test_ffuf_parser():
    sample_output = '{"results": [{"url": "http://example.com/admin", "status": 200}]}'
    findings = parse_ffuf_output(sample_output)
    assert len(findings) == 1
    assert findings[0].data['path'] == 'admin'

def test_nikto_parser():
    sample_output = '[{"msg": "Default account found", "url": "http://example.com/admin"}]'
    findings = parse_nikto_output(sample_output)
    assert len(findings) == 1
    assert findings[0].data['message'] == 'Default account found'