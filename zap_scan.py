from robot.api.deco import keyword
from zapv2 import ZAPv2
import time

import subprocess
import time

@keyword("Start ZAP Server")
def start_zap_daemon(zap_path, api_key, port=8080):
    print("[+] Starting ZAP in daemon mode...")
    cmd = [
        zap_path,
        '-daemon',
        f'-config', f'api.key={api_key}',
        f'-port', str(port)
    ]
    zap_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("[+] Waiting for ZAP to become responsive...")
    time.sleep(10)  # Give ZAP some time to start (or improve with a health check)  
    print(f"[+] ZAP started on port {port}")
    return zap_process


@keyword("Run ZAP Scan")
def run_zap_scan(target_url, api_key):
    print("[*] Connecting to ZAP...")
    zap = ZAPv2(
        apikey=api_key,
        proxies={
            'http': 'http://127.0.0.1:8080',
            'https': 'http://127.0.0.1:8080'
        }
    )

    while not zap.core.version:
        print("[*] Waiting for ZAP to be ready...")
        time.sleep(1)

    print(f"[*] Accessing target URL: {target_url}")
    zap.urlopen(target_url)
    time.sleep(2)

    print("[*] Spidering target...")
    spider_id = zap.spider.scan(target_url)
    while int(zap.spider.status(spider_id)) < 100:
        print(f"  Spider progress: {zap.spider.status(spider_id)}%")
        time.sleep(2)

    print("[*] Starting active scan...")
    scan_id = zap.ascan.scan(target_url)
    while int(zap.ascan.status(scan_id)) < 100:
        print(f"  Active scan progress: {zap.ascan.status(scan_id)}%")
        time.sleep(5)

    print("[*] Scan completed. Saving report...")
    with open("zap_juice_report.html", "w", encoding="utf-8") as report_file:
        report_file.write(zap.core.htmlreport())

    print("[+] Report saved as zap_juice_report.html")