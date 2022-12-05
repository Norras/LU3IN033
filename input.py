
import re


#read a file of frames and return a list of its frames
def input(filename):
    trames = [] # frames list
    cur=[] # current trame
    with open(filename, 'r') as f:
        lines=f.readlines()
        first=lines[0]
        print(f.read())
        previousoffset='0000'

        for line in lines:
            l=line.strip().split(' ')
            if l[0]=='0000':
                if cur!=[]:
                    trames.append(cur)
                    cur=[]
            cleared_line=check_hex(l[3:]) # remove useless data
            if (re.search("^[0-9a-f]{4}   .*$",line)==None): # check if the line is conform to the format
                raise Exception("Trame mal formée")
            if (line==first and l[0]!='0000'): # check if the first line is beginning with offset 0000
                raise Exception("Offset Invalide")
            if (l[0]!='0000' and (int(l[0],16)-int(previousoffset,16))!=len(previousline)): # check if the offset is correct
                raise Exception("Offset invalide")
            [octet.lower() for octet in cleared_line]
            cur.extend(cleared_line)
            previousoffset=l[0]
            previousline=cleared_line
    trames.append(cur)

    return trames


def check_hex(l:list):
    for i in l:
        if (len(i)!=2 or i[0]>'f' or i[1]>'f'):
            l.remove(i)
    return l

# # Path: output.py
# print("-------------------")
# print("Output")
# print(input()[0])
# print("-------------------")