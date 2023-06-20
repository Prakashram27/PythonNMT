#!/usr/bin/env python3
# coding: utf-8

# In[1]:

import os
import json
import subprocess
import re
#import datetime

# In[2]:


debug = 1
sudo_password = None

# In[3]:


def get_physical_interfaces(
    file_loc="/home/chiefnet/ChiefNet/ConfigurationFiles",
    debug=0
):
    try:
        with open(file_loc+"/SystemConfiguration.json", "r") as f:
            system_config = json.load(f)
            print(system_config)
        # Get list from json file
        wan_interfaces_list = system_config["system_information"]["wan_interfaces"]
        lan_interfaces_list = system_config["system_information"]["lan_interfaces"]

        wifi_interfaces = []
        lan_interfaces = []
        wan_interfaces = []

        for interface in lan_interfaces_list:
            if (interface.lower().startswith("wl")):
                wifi_interfaces.append(interface)
            else:
                lan_interfaces.append(interface)

        wan_interfaces = [interface for interface in wan_interfaces_list
                          if not (interface.startswith("tun"))
                          ]

        return wan_interfaces, lan_interfaces, wifi_interfaces
    except Exception as e:
        if debug:
            raise e
        else:
            pass


# In[4]:


def get_active_interfaces(interfaces, debug=0):
    """
    Function to retrieve active interfaces that are currently in UP state.
    """
    str_out = ""
    out = {}
    # Variable to store active interfaces.
    actives_interfaces = set()
    # cmd to get all the interfaces.
    command = f'ip -j address'

    # Executing the cmd
    cmd1 = subprocess.Popen(command.split(), stdout=subprocess.PIPE)

    # Parsing the json to get desired "interfaces" only if its "operstate" is "UP".
    try:
        # Decoding cmd output
        str_out = cmd1.stdout.read().decode()

        # Decoding to dict format
        out = json.loads(str_out)

        # Looping through all the interfaces.
        for i in out:
            # Checking if the interface is in desired set of interfaces.
            if ((i.get("ifname")) != None):
                if (i["ifname"] in interfaces):
                    # Add to active interfaces set if state is UP.
                    if (i["operstate"].lower() == "up"):
                        actives_interfaces.add(i["ifname"])
                    # Add to active interfaces set if state is UNKNOWN.
                    elif (i["operstate"].lower() == "unknown"):
                        actives_interfaces.add(i["ifname"])
                    # Add to logs if state is neither UP nor DOWN.
                    elif (i["operstate"].lower() != 'down'):
                        pass

    except Exception as e:
        if debug:
            raise e
        else:
            pass
#    print(actives_interfaces)
    return actives_interfaces, str(str_out)


# In[5]:


def size(val):
    """
    Parsing the value in Bytes for a given value.
    """
    val = val.lower()
    if (val[-1] == "b"):
        val = val[:-1]

        if ("g" in val):
            return val.lower().replace("g", "0"*9)
        elif ("m" in val):
            return val.lower().replace("m", "0"*6)
        elif ("k" in val):
            return val.lower().replace("k", "0"*3)
        else:
            return val
    else:
        return "0"


def get_iftop(interface, sudo_password=None, debug=0):
    """
    Getting the iftop values and parsing it as per line protocol.
    """

    # iftop command for each interface
   # command = f'iftop -bBP -i {interface} -s 1s -o 10s -L 100 -t'
    command = f'iftop -nNb -i {interface} -s 1s -o 10s -L 100 -t'

    # For inserting password in cmd line
    #cmd1 = subprocess.Popen(['echo',sudo_password], stdout=subprocess.PIPE)
    # Getting iftop command output
    cmd2 = subprocess.Popen(command.split(), stdout=subprocess.PIPE)

    # decoding output from cmd  
    lines = cmd2.stdout.read().decode()
    lines_lst = lines.split("\n")

    # Parsing each line and getting the output in line protocol.
    for i, line in enumerate(lines_lst):
        # Getting list values of each line
        lst = line.split()
        try:
            # initializing fields
            sender, sent, receiver, received = 0, 0, 0, 0

            # Checking for valid lines in the output
            if (len(lst) > 1):
                if (lst[0].isdigit()):
                    # print(lst[0])

                    # Validity check with length for sent
                    if (len(lst) == 7):
                        # Getting sender and send rate
                        sender, sent = (lst[1], size(val=lst[4]))
                        # print(lst)
                    nxt_line_lst = lines_lst[i+1].split()
                    # Validity check with length for received
                    if (len(nxt_line_lst) == 6):
                        # Getting receiver and received rate
                        receiver, received = (
                            nxt_line_lst[0], size(val=nxt_line_lst[3]))
                        # print(nxt_line_lst)

                        # printing values in line protocol format
                        # Validity check to prevent unnecessary values.
#                        print("--------------------------------------")
                        if (sent == "0"):
                            # printing values in line protocol format
                            print()
                            print(
                                f'iftop_traffic,interface={interface},sender={sender}{ip_locator(sender)},receiver={receiver}{ip_locator(receiver)} receiveRate={float(received)}')
                        elif (received == "0"):
                            print(
                                f'iftop_traffic,interface={interface},sender={sender}{ip_locator(sender)},receiver={receiver}{ip_locator(receiver)} sendRate={float(sent)}')
                        else:
                            print(
                                f'iftop_traffic,interface={interface},sender={sender}{ip_locator(sender)},receiver={receiver}{ip_locator(receiver)} sendRate={float(sent)},receiveRate={float(received)}')

                else:
                    # Skipping unwanted lines.
                    pass
                    # append_new_line("here")

        # Handling exception and storing the output in a log file.
        except Exception as e:
            if debug:
                raise e
            else:
                pass


def ip_locator(ip):

    cmd = "geoiplookup "+ str(ip)

    ip_add_location = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    location, location_err = ip_add_location.communicate()
    if ip_add_location.returncode == 0:
        if "IP Address not found" in location:
            return ""
        else:
            location_li = re.sub(r'[^\w]', ' ', location).split(" ")
            with open(file="/etc/telegraf/custom_scripts/CountryCode.json", mode="r") as country_code:
                country_json = json.load(country_code)
                for country in country_json:
                    if country['code'] == location_li[4]:
                        return ":"+country['flag']
        return ""
    else:
        return ""



# In[ ]:


if __name__ == "__main__":

    try:
       # print(datetime.datetime.now())

        result = get_physical_interfaces(
            r"/etc/telegraf/custom_scripts",
            debug
        )
        if (result == None):
            raise Exception("No interfaces found.")
        wan_interfaces, lan_interfaces, wifi_interfaces = result

        #interfaces = set(list(wan_interface_dict) + list(lan_interface_dict))
        interfaces = set(wan_interfaces + lan_interfaces + wifi_interfaces)
        #interfaces = {"enp1s0","enp2s0","enp3s0","enp4s0"}
        inactives_interfaces = set()

        # Getting active interfaces.
        actives_interfaces, out = get_active_interfaces(interfaces=interfaces,
                                                        debug=debug
                                                        )
        # getting inactive interfaces
        inactives_interfaces = interfaces - actives_interfaces
        
#        print(actives_interfaces)
        # Printing line protocol for interfaces present.
        for interface in actives_interfaces:
            # Iftop data for active interfaces.
            get_iftop(sudo_password=sudo_password,
                      interface=interface,
                      debug=debug
                      )
       # print(datetime.datetime.now())

    except Exception as e:
        if debug:
            raise e
        else:
            pass
