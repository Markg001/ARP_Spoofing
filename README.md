# ARP_Poisoning
**ARP Spoofing**

![arp_poisoning](https://github.com/user-attachments/assets/a805ea03-21fb-4bc5-95fa-fae7a0a18543)

**Overview**

This script performs an ARP spoofing attack on a local network. ARP spoofing, also known as ARP cache poisoning, is a technique where an attacker sends fake ARP (Address Resolution Protocol) messages to deceive network devices, making them associate the attacker's machine with the IP address of another device (usually the gateway or another host). This positions the attacker as a "man-in-the-middle," enabling them to intercept, modify, or monitor the network traffic between devices on the network.

The script is designed to:

  ~ Poison the ARP cache of a target machine and the network gateway.
  
  ~ Trick both the target and the gateway into thinking that the attacker’s machine is the other device.
  
  ~ Enable the attacker to intercept, monitor, or alter traffic between the target and the gateway (e.g., for man-in-the-          middle attacks).
  
  ~ Restore the ARP tables on the target and gateway when the attack is stopped, preventing permanent network disruption.

**What is ARP?**

Address Resolution Protocol (ARP) is a protocol used by network devices to map an IP address to a MAC (Media Access Control) address on a local network. Each device on a network has a unique MAC address that identifies it, and ARP is used to resolve which MAC address corresponds to a given IP address.

When a device wants to communicate with another device, it first checks if it knows the MAC address for the intended IP address (stored in its ARP cache). If not, it broadcasts an ARP request to the entire network, asking “Who has IP address X? Tell me your MAC address.” The device with the corresponding IP replies with its MAC address, and the requesting device updates its ARP cache.

**What is ARP Spoofing?**

ARP spoofing involves sending forged ARP responses to deceive network devices. The goal is to poison the ARP cache of the target device by associating the attacker's MAC address with the IP address of another device, often the network gateway. As a result:

  ~ The target device will send its traffic to the attacker, believing it is sending it to the gateway.
  
  ~ The gateway will send its traffic to the attacker, believing it is communicating with the target.
  
This technique is typically used in Man-in-the-Middle (MITM) attacks, where the attacker can:

  ~ Intercept data: Capture sensitive information like usernames, passwords, and session tokens.
  
  ~ Modify data: Alter data in transit before it reaches its intended destination.
  
  ~ Monitor traffic: Observe all communications between the victim and the gateway.

**Example Scenario:**

  1. Target Machine (192.168.1.5) needs to send data to the internet through the Gateway (192.168.1.1).
  2. The attacker runs an ARP spoofing attack, sending fake ARP responses to both:
      The Target (192.168.1.5) telling it that the attacker's MAC address is the Gateway's IP (192.168.1.1).
      The Gateway (192.168.1.1) telling it that the attacker's MAC address is the Target's IP (192.168.1.5).
  3. Both devices update their ARP tables with the attacker's MAC address, thinking it's the correct device.
Now, all traffic between the target and the gateway goes through the attacker's machine, allowing them to intercept and manipulate the data.

**How the Script Works**
Get MAC Address: The script first attempts to retrieve the MAC address of both the target and the gateway by sending an ARP request to them. If successful, this allows the script to communicate with the devices.

**ARP Spoofing:**

The script repeatedly sends spoofed ARP responses to the target and gateway.
It tells the target that the attacker's MAC address belongs to the gateway's IP and vice versa.
As a result, both devices update their ARP tables and start sending traffic to the attacker's machine, thinking they are talking to the legitimate device.

**Man-in-the-Middle Attack:**

 ![MITM](https://github.com/user-attachments/assets/626fa9e5-07d8-4bb0-9eb4-d833b4bea728)

Once the attack is in place, all network traffic between the target and the gateway is routed through the attacker's machine.
The attacker can now capture, modify, or analyze the data flowing between the two devices.

**Restoring ARP Tables:**

When the attack is stopped (using CTRL + C), the script sends the correct ARP responses to both the target and gateway to restore their ARP tables.
This ensures that the target and gateway return to normal communication without going through the attacker's machine, preventing any further network disruption.

