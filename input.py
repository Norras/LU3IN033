



#read a file of trames and return a list of trames
def input():
    trames = [] # Liste des trames
    cur=[] # current trame
    with open('realforpy.txt', 'r') as f:
        lines=f.readlines()
        last=lines[-1]
        first=lines[0]
        print(f.read())
        previousoffset='0000'

        for line in lines:
            l=line.strip().split(' ')
            if l[0]=='0000':
                if cur!=[]:
                    trames.append(cur)
                    cur=[]
            check_hex(l[3:])
            if (len(l[3:])!=16 and (line!=last)):
                raise Exception("Trame invalide")
            if (line==first and l[0]!='0000'):
                raise Exception("Offset Invalide")
            if (l[0]!='0000' and (int(l[0],16)-int(previousoffset,16))!=len(previousline)):
                raise Exception("Offset invalide")
            cur.extend(l[3:])
            previousoffset=l[0]
            previousline=l[3:]
    trames.append(cur)

    return trames


def check_hex(l:list):
    for i in l:
        if (len(i)!=2 or i[0]>'f' or i[1]>'f'):
            raise Exception("Hexadecimal invalide : "+ i)

# Path: output.py
print("-------------------")
print("Output")
print(input()[0])
print("-------------------")