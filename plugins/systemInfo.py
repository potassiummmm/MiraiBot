import subprocess

def getSystemInfo():
    result = subprocess.getoutput("neofetch --stdout")
    return result.strip('\n')


