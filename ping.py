from sys import platform
linux = platform == "linux"

import os, subprocess

PHONE_AWAY_IP = "192.168.0.3"
PHONE_HOTSPOT_IP = "192.168.43.1"

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-c' if linux else '-n'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    FNULL = open(os.devnull, 'w')
    return subprocess.call(command, stdout=FNULL, stderr=subprocess.STDOUT) == 0

def is_phone_available():
    return ping(PHONE_AWAY_IP) or ping(PHONE_HOTSPOT_IP)

def is_phone_available_fake():
    return os.path.exists("ping/phone")
