# KOPR - KOntrolní PRogram virtuálních služeb
from targets import MonitoringTarget, NginxTarget, LoadTarget
from logger import Logger
import asyncio

tasks = set()

logger = Logger("test.log")
hosts = ["1.1.1.1", "10.0.0.1", "172.77.0.2", "172.77.0.3"]
        
lt = LoadTarget(hosts[2], logger)

for host in hosts:
    x = MonitoringTarget(host, logger)
    tasks.add(
        asyncio.create_task(
            x.ping()
        )
    )

async def main():
    await asyncio.gather(
        tasks
    )
    
asyncio.run(main())
        
# asyncio.gather(tasks)
        

# for host in hosts:
#     target = MonitoringTarget(host, logger)
#     target.ping()

# ng = NginxTarget(hosts[2], logger)
# ng.log_stub()
