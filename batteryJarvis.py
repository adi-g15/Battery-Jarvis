#!/usr/bin/env python3

import os,time
import subprocess
import getpass

from subprocess import call

"""
   Some systems contain battery information in BAT0 while some have in
   BAT1.Therefore script uses find command to find folder beginning with BAT. Therefore script works on BAT0 or BAT1 according to system.


"""

def get_battery_paths():
    """Return a list of paths to battery devices."""
    files = os.listdir('/sys/class/power_supply')
    return [
        os.path.join('/sys/class/power_supply', x) for x in files if x.startswith('BAT')]

def get_file_content(path):
    """Read a file and return its contents."""
    with open(path, 'r') as f:
        return f.read()

# Uses only the 1st battery found, jyadatar case me to 1 hi hoga
# May contain BAT0 or BAT1 at end
batterypath=get_battery_paths()[0]

charge_now_content=get_file_content(batterypath + "/charge_now")
charge_full_content=get_file_content(batterypath + "/charge_full")
charge_status_content=get_file_content(batterypath + "/status")

"""
  charge_status_content is string consisting of two lines first line contains "Charging" and 2nd line is empty.

  Therefore comparing charge_status_content with "Charging" gave false


  Therefore I used splitlines() to have lines in a list.

  Then I took first element of list .
"""

lines=charge_status_content.splitlines()

charge_status_content=lines[0]

num=int(charge_now_content)*1.0
den=int(charge_full_content)*1.0

res=num/den*100

user=getpass.getuser()

#user=user[:-4]

if res<=15 and charge_status_content!="Charging":
    speech ="Yaar " + user + " Charge karde mereko !"
    call(["espeak",speech])

elif res==100 and charge_status_content!="Discharging":
    speech ="Yaar " + user + ". Jyada charge ho gya re !!"
    call(["espeak",speech])

