
from input import input #import the input function from input.py


Ethernet=tuple[str,str,str]
Ip=tuple[str,str,str,str,str,str,str,str,str,str,str]
Tcp=tuple[str,str,str,str,int,str,str,str,str]

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
    protocol = ip_header[9]
    source_address = ''.join(ip_header[12:16])
    destination_address = ''.join(ip_header[16:20])
    options:str = ''.join(ip_header[20:ihl_int])
    flags,fragment_offset=extract_flags(fragment_offset_and_flags)
    return (version,ihl,total_length,identification,flags,fragment_offset,protocol,source_address,destination_address,options)


def value_to_ip(value:int)->str:
    return str(value>>24)+"."+str((value>>16)&0xFF)+"."+str((value>>8)&0xFF)+"."+str(value&0xFF)

def str_to_ip(ch:str)->str:
    return str(int(ch[0:2],16))+"."+str(int(ch[2:4],16))+"."+str(int(ch[4:6],16))+"."+str(int(ch[6:8],16))
# dissociate flags from fragment offset
# warning : returned values are in base 2
def extract_flags(fragment_offset_and_flags:str)->tuple[str,str]:
    #format( "016b") to have 16 bits in binary
    bits = str(format(int(fragment_offset_and_flags,16),"016b"))
    flags = bits[0:3]
    fragment_offset = bits[3:]
    return (flags,fragment_offset)
    
def check_if_ip(packet)->bool:
    return (packet[12:14]==['08','00'] and packet[14][0]=='4')

def check_if_tcp(packet)->bool:
    return packet[23]=='06'



def extract_tcp(packet)->Tcp:
    # check ip header length
    ihl_int = int(packet[14][1],16)*4
    # check tcp header length
    tcp_header_length_byte = str(format(int(packet[14+ihl_int+12],16),"08b"))
    tcp_header_length = int(tcp_header_length_byte[0:4],2)*4

    tcp_header=packet[14+ihl_int:14+ihl_int+tcp_header_length]

    source_port = ''.join(tcp_header[0:2])
    destination_port = ''.join(tcp_header[2:4])
    sequence_number = ''.join(tcp_header[4:8])
    acknowledgement_number = ''.join(tcp_header[8:12])
    flags_and_stuff=''.join(tcp_header[12:14])
    flags=extract_tcp_flags(flags_and_stuff)
    window_size = ''.join(tcp_header[14:16])
    checksum = ''.join(tcp_header[16:18])
    urgent_pointer = ''.join(tcp_header[18:20])
    options = ''.join(tcp_header[20:])

    return (source_port,destination_port,sequence_number,acknowledgement_number,tcp_header_length,flags,window_size,checksum,urgent_pointer,options)

def check_if_http(packet)->bool:
    tcp=extract_tcp(packet)
    if (tcp[0]=='50' or tcp[1]=='50'):
        return True

def extract_tcp_flags(flags_and_stuff:str)->tuple[str,str,str,str,str,str,str,str]:
    bits = str(format(int(flags_and_stuff,16),"016b"))
    urg = bits[10]
    ack = bits[11]
    psh = bits[12]
    rst = bits[13]
    syn = bits[14]
    fin = bits[15]
    return (urg,ack,psh,rst,syn,fin)

def extract_http(packet)->str:
    ihl_int = int(packet[14][1],16)*4
    tcp_header_length_byte = str(format(int(packet[14+ihl_int+12],16),"08b"))
    tcp_header_length = int(tcp_header_length_byte[0:4],2)*4
    http = packet[14+ihl_int+tcp_header_length:]
    res=""
    for o in http:
        if (o=="0d"):
            break
        res=res+chr(int(o,16))
    return res
# print("-------------------")
# print(extract_ethernet_header(input()[0]))
# print(extract_ip_header(input()[0]))
# extract_flags(extract_ip_header(input()[0])[4])

# print(extract_flags(extract_ip_header(input()[0])[4]))
# print(extract_tcp(input()[0]))


