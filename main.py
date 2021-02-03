import core
from pathlib import Path
from graia.application import Session
from config import BOT_ACCOUNT, BOT_HOST, AUTHKEY
import time

if __name__ == "__main__":
    start = time.time()
    core.init(
        Session(host=BOT_HOST,
                authKey=AUTHKEY,
                account=BOT_ACCOUNT,
                websocket=True))
    print("init time", time.time() - start)
    core.load_plugins(Path("plugins"))
    print("load time", time.time() - start)
    app = core.Instance.app()
    while True:
        try:
            app.launch_blocking()
        except KeyboardInterrupt:
            break
