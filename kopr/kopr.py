# KOPR - KOntrolní PRogram virtuálních služeb
from targets import MonitoringTarget, NginxTarget, LoadTarget
from logger import Logger
import asyncio
from concurrent.futures import ProcessPoolExecutor

tasks = set()

logger = Logger("test.log")

nginx = NginxTarget("172.77.0.2", logger)

loads = (
    nginx,
    LoadTarget("172.77.0.3", logger),
    LoadTarget("172.77.0.10", logger),
    LoadTarget("172.77.0.11", logger),
    LoadTarget("172.77.0.12", logger)
)

for load in loads:
    load.ping()
    load.log_load()

loads[0].log_stub()
