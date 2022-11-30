
from input import input #import the input function from input.py


Ethernet=tuple[str,str,str]
Ip=tuple[int,int,int,str,str,str,int,int,str,str,str,str]

# Define a empty value in tuple : put None

#Extraction of the Ethernet header (type stored in base 10)
def extract_ethernet_header(packet)->Ethernet:
    ethernet_header = packet[0:14]
    return (ethernet_header[0]+":"+ethernet_header[1]+":"+ethernet_header[2]+":"+ethernet_header[3]+":"+ethernet_header[4]+":"+ethernet_header[5],ethernet_header[6]+":"+ethernet_header[7]+":"+ethernet_header[8]+":"+ethernet_header[9]+":"+ethernet_header[10]+":"+ethernet_header[11],''.join(ethernet_header[12:14]))


# extract ip header from packet
#initial ip header length is 20 bytes
def extract_ip_header(packet)->Ip:
    #determine the ip header length
    #ip header length is in the 4th byte of the ip header

    total_length = int(''.join(packet[16:18]),16)
    ip_header = packet[14:14+total_length]
    version = int(ip_header[0][0],16)
    ihl = int(ip_header[0][1],16)*4 # ip header length in bytes
    identification = int(''.join(ip_header[4:6]),16)
    flags = int(ip_header[6][0],16)
    fragment_offset = int(''.join(ip_header[6:8]),16)
    ttl = int(ip_header[8],16) # time to live
    protocol = int(ip_header[9],16)
    header_checksum = ''.join(ip_header[10:12])
    source_address = int(''.join(ip_header[12:16]),16)
    destination_address = int(''.join(ip_header[16:20]),16)
    options:str = ''.join(ip_header[20:ihl])
    return (version,ihl,total_length,identification,flags,fragment_offset,ttl,protocol,header_checksum,source_address,destination_address,options)

    

def value_to_ip(value:int)->str:
    return str(value>>24)+"."+str((value>>16)&0xFF)+"."+str((value>>8)&0xFF)+"."+str(value&0xFF)




print("-------------------")
print(extract_ethernet_header(input()[0]))
print(extract_ip_header(input()[0]))