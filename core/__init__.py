import asyncio
from graia.application import GraiaMiraiApplication, Session
from graia.broadcast import Broadcast
from graia.broadcast.interrupt import InterruptControl
from graia.scheduler import GraiaScheduler
from .plugin import *


def init(config_session: Session) -> None:
    global bcc, app, inc, sche
    loop = asyncio.get_event_loop()
    bcc = Broadcast(loop=loop, debug_flag=True)
    inc = InterruptControl(bcc)
    app = GraiaMiraiApplication(broadcast=bcc, connect_info=config_session)
    sche = GraiaScheduler(loop=loop, broadcast=bcc)


class Instance:
    @staticmethod
    def app() -> GraiaMiraiApplication:
        return app

    @staticmethod
    def bcc() -> Broadcast:
        return bcc

    @staticmethod
    def inc() -> InterruptControl:
        return inc

    @staticmethod
    def sche() -> GraiaScheduler:
        return sche
