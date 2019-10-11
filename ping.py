import platform    # For getting the operating system name
import subprocess  # For executing a shell command

PHONE_AWAY_IP = "192.168.0.3"
PHONE_HOTSPOT_IP = "192.168.43.1"

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0

def isPhoneAvailable():
    return ping(PHONE_AWAY_IP) or ping(PHONE_HOTSPOT_IP)
