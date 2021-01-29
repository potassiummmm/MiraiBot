import core
from pathlib import Path
from graia.application import Session


if __name__ == "__main__":
    core.init(Session(
        host = "http://localhost:8081",
        authKey = "testauthkey",
        account = 1521138307,
        websocket = True,
        debug_flag = True
        )
    )
    core.load_plugins(Path("plugins"),active_groups=[])
    app = core.Instance.app()
    while True:
        try:
            app.launch_blocking()
        except KeyboardInterrupt:
            break
