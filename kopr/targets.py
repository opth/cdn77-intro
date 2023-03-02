import re
import requests
from paramiko import SSHClient
from ping3 import ping

from logger import Logger


class MonitoringTarget:
    ip: str
    logger: Logger

    def __init__(self, ip: str, logger: Logger) -> None:
        self.logger = logger
        self.ip = ip
        
    async def ping(self) -> None:
        response = ping(self.ip, unit="ms", timeout=3)
        
        if not response:
            self.logger.log(f"ping: Ping failed, host {self.ip} is unreachable")
        else:
            self.logger.log(f"ping: Pinged {self.ip}, took {'%.3f' % response} ms")
        return response
    
class NginxTarget(MonitoringTarget):
    stub_port: int = 8080
    
    def __init__(self, ip: str, logger: Logger) -> None:
        super().__init__(ip, logger)
    
    async def log_stub(self):
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
        
class LoadTarget(MonitoringTarget):
    client: SSHClient
    username: str = "root"
    key_filename: str = "./ansible"
    
    def __init__(self, ip: str, logger: Logger) -> None:
        super().__init__(ip, logger)
        
        self.client = SSHClient()
        self.client.load_system_host_keys()
        
    async def log_load(self):
        self.client.connect(self.ip, username=self.username, key_filename=self.key_filename)
        stdin, stdout, stderr = self.client.exec_command('uptime')
        
        load_str = str(stdout.readlines(1024))
        load_1, load_5, load_15 = re.search(r'(\d+.\d+), (\d+.\d+), (\d+.\d+)', load_str).groups()
        
        self.client.close()
        
        self.logger.log(f"load: Loads at {self.ip} are: [ 1m: {load_1}, 5m: {load_5}, 15m: {load_15}]")
        