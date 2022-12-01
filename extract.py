
from input import input #import the input function from input.py


Ethernet=tuple[str,str,str]
Ip=tuple[str,str,str,str,str,str,str,str,str,str,str]

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

    total_length_int = int(''.join(packet[16:18]),16)
    total_length=''.join(packet[16:18])
    ip_header = packet[14:14+total_length_int]
    version = ip_header[0][0]
    ihl_int = int(ip_header[0][1],16)*4 # ip header length in bytes
    ihl=ip_header[0][1]
    identification = ''.join(ip_header[4:6])
    fragment_offset_and_flags = ''.join(ip_header[6:8])
    ttl = ip_header[8] # time to live
    protocol = ip_header[9]
    header_checksum = ''.join(ip_header[10:12])
    source_address = ''.join(ip_header[12:16])
    destination_address = ''.join(ip_header[16:20])
    options:str = ''.join(ip_header[20:ihl_int])
    return (version,ihl,total_length,identification,fragment_offset_and_flags,ttl,protocol,header_checksum,source_address,destination_address,options)

    

def value_to_ip(value:int)->str:
    return str(value>>24)+"."+str((value>>16)&0xFF)+"."+str((value>>8)&0xFF)+"."+str(value&0xFF)

# dissociate flags from fragment offset
# warning : returned values are in base 2
def extract_flags(fragment_offset_and_flags:str)->tuple[str,str]:
    #format( "016b") to have 16 bits in binary
    print(int(fragment_offset_and_flags,16))
    bits = str(format(int(fragment_offset_and_flags,16),"016b"))
    flags = bits[0:3]
    fragment_offset = bits[3:]
    return (flags,fragment_offset)
    


print("-------------------")
print(extract_ethernet_header(input()[0]))
print(extract_ip_header(input()[0]))
extract_flags(extract_ip_header(input()[0])[4])
print(extract_flags(extract_ip_header(input()[0])[4]))
print(~10)
