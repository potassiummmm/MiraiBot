from random import randint


def getJoke() -> str:
    """
    return a random soviet joke
    """
    with open("/usr/mirai/src/text/sovietJokes.txt") as jokes:
        lines = jokes.readlines()
        random_joke = lines[randint(0, len(lines) - 1)].rstrip()
        return random_joke
