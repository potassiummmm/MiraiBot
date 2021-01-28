import asyncio
from graia.application import GraiaMiraiApplication, Session
from graia.broadcast import Broadcast
from graia.broadcast.interrupt import InterruptControl
import graia.scheduler
def init(config_session: Session) -> None:
    global bcc, sche, app, inc
    loop = asyncio.get_event_loop()
    bcc = Broadcast(loop=loop, debug_flag=True)
    sche = graia.scheduler.GraiaScheduler(loop=loop, broadcast=bcc)
    inc = InterruptControl(bcc)
    app = GraiaMiraiApplication(
        broadcast=bcc,
        connect_info=config_session
    )

class Instance:
    @staticmethod
    def app() -> GraiaMiraiApplication:
        return app
    @staticmethod
    def bcc() -> Broadcast:
        return bcc
    @staticmethod
    def sche() -> graia.scheduler.GraiaScheduler:
        return sche
    @staticmethod
    def inc() -> InterruptControl:
        return inc

