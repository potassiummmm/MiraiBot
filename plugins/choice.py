import random
import datetime


def makeChoice(*paras):
    random.seed(datetime.datetime.now())
    return paras[random.randint(0, len(paras) - 1)]
