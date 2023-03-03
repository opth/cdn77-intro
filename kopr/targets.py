import re
import requests
import io
from paramiko import SSHClient, Ed25519Key, AutoAddPolicy
from ping3 import ping
from time import sleep
from logger import Logger

MY_KEY = """\
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACAwGDqsEnJbLOVmtc9jahEAWVfwpwIVidmBQFyfNK3OJAAAAJiuCs93rgrP
dwAAAAtzc2gtZWQyNTUxOQAAACAwGDqsEnJbLOVmtc9jahEAWVfwpwIVidmBQFyfNK3OJA
AAAEA5IEL5SDhbdHW+LY4t0fly0I33Ma+JSlS5NjCNzmX7TTAYOqwSclss5Wa1z2NqEQBZ
V/CnAhWJ2YFAXJ80rc4kAAAAEHJlYWN0aXZlQGtvbG9icmsBAgMEBQ==
-----END OPENSSH PRIVATE KEY-----"""

class MonitoringTarget:
    ip: str
    logger: Logger

    def __init__(self, ip: str, logger: Logger) -> None:
        self.logger = logger
        self.ip = ip
        
    def ping(self) -> None:
        # print(f"Pingin {self.ip}")
        response = ping(self.ip, unit="ms", timeout=3)
        
        if not response:
            self.logger.log(f"ping: Ping failed, host {self.ip} is unreachable")
        else:
            self.logger.log(f"ping: Pinged {self.ip}, took {'%.3f' % response} ms")
        return response
    

class LoadTarget(MonitoringTarget):
    client: SSHClient
    username: str = "root"
    pkey: Ed25519Key

    def __init__(self, ip: str, logger: Logger) -> None:
        super().__init__(ip, logger)
        
        self.client = SSHClient()
        self.client.load_system_host_keys()
        self.pkey = Ed25519Key.from_private_key(io.StringIO(MY_KEY))
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        
    def log_load(self):
        self.client.connect(self.ip, username=self.username, pkey=self.pkey)
        stdin, stdout, stderr = self.client.exec_command('uptime')
        
        load_str = str(stdout.readlines(1024))
        load_1, load_5, load_15 = re.search(r'(\d+.\d+), (\d+.\d+), (\d+.\d+)', load_str).groups()
        
        self.client.close()
        
        self.logger.log(f"load: Loads at {self.ip} are: [ 1m: {load_1}, 5m: {load_5}, 15m: {load_15}]")


class NginxTarget(LoadTarget):
    stub_port: int = 8080
    
    def __init__(self, ip: str, logger: Logger) -> None:
        super().__init__(ip, logger)
    
    def log_stub(self):
        try:
            r = requests.get(f"http://{self.ip}:{self.stub_port}/stub_status")
        except Exception:
            self.logger.log("Could not fetch nginx stub status", err=True)
            return
        
        active_connections = int(
            re.search(r'(Active connections: )(\d+)', r.text)[2]
        )
        
        server_search = re.search(r' (\d+) (\d+) (\d+) \n', r.text)
        accepts = server_search[1]
        handled = server_search[2]
        reqs = server_search[3]
        
        self.logger.log(f"nginx: Nginx is up. status:[ active_conections: {active_connections}, "
                        + f"accepts: {accepts}, handled: {handled}, requests: {reqs}]")
        
        