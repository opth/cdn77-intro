# KOPR - KOntrolní PRogram virtuálních služeb
from ping3 import ping

class MonitoringTarget:
    ip: str
    
    def __init__(self, ip: str) -> None:
        self.ip = ip
        
    def ping(self) -> None:
        response = ping(self.ip, unit="ms", timeout=3)
        return response
        
x = MonitoringTarget("10.0.0.1")
x.ping()