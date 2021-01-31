import core
from pathlib import Path
from graia.application import Session
from config import BOT_ACCOUNT, BOT_HOST, AUTHKEY

if __name__ == "__main__":
    core.init(Session(
        host=BOT_HOST,
        authKey=AUTHKEY,
        account=BOT_ACCOUNT,
        websocket=True
    )
    )
    core.load_plugins(Path("plugins"))
    app = core.Instance.app()
    while True:
        try:
            app.launch_blocking()
        except KeyboardInterrupt:
            break
