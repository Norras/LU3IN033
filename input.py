
import re


#read a file of frames and return a list of its frames
def input(filename):
    trames = [] # frames list
    cur=[] # current trame
    with open(filename, 'r') as f:
        lines=f.readlines()
        first=lines[0]
        previousoffset='0000'

        for line in lines:
            l=line.strip().split(' ')
            if l[0]=='0000':
                if cur!=[]:
                    trames.append(cur)
                    cur=[]
            cleared_line=check_hex(l[3:]) # remove useless data
            print(cleared_line)
            if (re.search("^[0-9a-f]{4}   .*$",line)==None): # check if the line is conform to the format
                raise Exception("Trame mal formée")
            if (line==first and l[0]!='0000'): # check if the first line is beginning with offset 0000
                raise Exception("Offset Invalide")
            if (l[0]!='0000' and (int(l[0],16)-int(previousoffset,16))!=len(previousline)): # check if the offset is correct
                raise Exception("Offset invalide")
            cur.extend(cleared_line)
            previousoffset=l[0]
            previousline=cleared_line
    trames.append(cur)

    return trames


hexvalues=['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']

def check_hex(l:list):
    res=[]
    for i in l:
        if ((len(i)==2) and (i[0].lower() in hexvalues) and (i[1].lower() in hexvalues) and (i!='')):
            res.append(i.lower())
        else:
            print(i+" "+str(len(i)))
    return res

# # Path: output.py
# print("-------------------")
# print("Output")
# print(input()[0])
# print("-------------------")