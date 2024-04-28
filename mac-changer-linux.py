#!/usr/bin/python3
import re # module expressions régulières
import subprocess # permet d'exécuter des commandes système
import optparse # permet de mettre en place des commandes utilisables sur Linux

def search_mac_address(string): # permet d'identifier l'adresse MAC grace au module d'expressions régulières
    match = re.search(r'([0-9A-F]{2}[:-]){5}([0-9A-F]{2})', str(string)) # on recherche une chaine de caractères qui correspond au format d'une adresse MAC
    if match:
        return match.group(0) # group(0) permet de récupérer l'ensemble de la chaine de caractères
    else:
        return str
        

def get_arguments(): # permet de définir l'interface réseau et l'adresse MAC que l'on souhaite
    parser = optparse.OptionParser() # lit les options définies dans le parser
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address") # définit l'option : interface
    parser.add_option("-m", "--mac", dest="new_mac_address", help="New MAC address") # définit l'option : nouvelle adressse MAC
    (options, arguments) = parser.parse_args() # lit les arguments rentrés par l'utilisateur
    if not options.interface: # vérifie que l'interface a bien été définie
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac_address: # vérifie que l'adresse MAC a bien été définie
        parser.error("[-] Please specify a new mac address, use --help for more info.")
    return options

def set_new_mac_address(interface, new_mac_address): # permet de communiquer avec l'interface dans ifconfig pour changer l'adresse MAC
    print("[+] Changing MAC address for " + interface + " to " + new_mac_address)
    subprocess.call("ifconfig " + interface + " down", shell=True) # éteint l'interface réseau
    subprocess.call("ifconfig " + interface + " hw ether " + new_mac_address, shell=True) # changement de l'adresse MAC de l'interface réseau
    subprocess.call("ifconfig " + interface + " up", shell=True) # remise en marche de l'interface réseau avec la nouvelle adresse MAC

def get_mac_address_from_interface(interface): # on récupère l'adresse MAC depuis l'interface
    ifconfig_result = subprocess.check_output(["ifconfig", interface]) # on ouvre ifconfig
    mac_address_search_result = search_mac_address(ifconfig_result) # on recherche l'adresse MAC dans ifconfig

    if mac_address_search_result: # on vérifie que l'on retrouve bien l'adresse MAC dans ifconfig
        return mac_address_search_result
    else:
        print("[-] Could not read MAC address.")

options = get_arguments()
current_mac_address = str(get_mac_address_from_interface(options.interface)) # on récupère l'adresse MAC de l'interface
print("Current MAC address for interface " + options.interface + " is : " + current_mac_address)


set_new_mac_address(options.interface, options.new_mac_address) # on récupère les options concernant l'interface et la nouvelle adresse MAC, puis on communique avec l'interface pour effectuer le changement dans ifconfig

new_mac_address = get_mac_address_from_interface(options.interface) # on récupère la nouvelle adresse MAC dans ifconfig
if new_mac_address == options.new_mac_address: # on vérifie que le changement a bien été effectué
    print("[+] MAC address was successfully changed to " + new_mac_address + ".")
else:
    print("[-] MAC address did not get changed.")

