#!/usr/bin/env/ python3
import subprocess, optparse, re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its mac address")
    parser.add_option('-m', '--mac', dest='new_mac', help='New MAC address')
    (options, arguments) = parser.parse_args()

    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify a new mac, use --help for more info.")
    else:
        return options


def change_mac(interface, new_mac):
    print(f"[+] Changing MAC address for {interface} to {new_mac}")
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    command_output = subprocess.check_output(['ifconfig', interface])
    command_output = command_output.decode('utf-8')

    mac_address_search_result = re.search(r"(\w\w:){5}\w\w", command_output)

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address.")
        exit(0)


options = get_arguments()
current_mac = get_current_mac(options.interface)
print('Current MAC = ', current_mac)
change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)

if current_mac == options.new_mac:
    print("[+] MAC address was successfully changed to", current_mac)
else:
    print("[-] MAC address did not changed.")
