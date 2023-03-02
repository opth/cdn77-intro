import io
from datetime import datetime


class Logger:
    log_file: io.StringIO

    def __init__(self, filename: str) -> None:
        self.log_file = open(filename, mode='at', encoding='utf-8')

    def __del__(self):
        self.log_file.close()

    def log(self, line_str: str, err: bool = False):
        now_str = datetime.now().strftime("%a %Y-%m-%d %H:%M:%S")
        err_str = ""
        
        if err:
            err_str = " Error"
            
        self.log_file.write(f"{now_str}{err_str}: {line_str}\n")