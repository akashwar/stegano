import os,sys
from PIL import Image
import binascii
from Tkinter import Tk
from tkFileDialog import askopenfilename

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

def appender(tup,R,G,B):
    currR=tup[0]
    currG=tup[1]
    currB=tup[2]
    x = bin(currR)[2:].zfill(8)[:5] + bin(R)[2:].zfill(3)
    y = bin(currG)[2:].zfill(8)[:5] + bin(G)[2:].zfill(3)
    z = bin(currB)[2:].zfill(8)[:6] + bin(B)[2:].zfill(2)

    return (int(x,2),int(y,2),int(z,2),255)

def encode(im,digest,lenofstr,size):
    pix = im.load()
    x = 0
    i=0
    j=11
    # Encode the length of the string
    pix[0,11]=(lenofstr,0,0,255)

    for y in range(lenofstr):
        if j + 11 > size[1]:
            j=0
            i=i+1
        else:
            j=j+11
        try:
            R = int(digest[x:x + 3], 2)
            G = int(digest[x + 3:x + 6], 2)
            B = int(digest[x + 6:x + 8], 2)
            pix[i,j] = appender(pix[i,j],R,G,B)
            x = x + 8
        except IndexError:
            print 'Index out of range'
            break
        except ValueError:
            continue


def decode(im1,size):
    pix=im1.load()
    x = 0
    final=[]
    j=11
    i=0
    length=pix[0,j][0]
    for z in range(length):
        if j+11 > size[1]:
            j = 0
            i = i + 1
        else:
            j=j+11

        (R,G,B)=pix[i,j]
        R=bin(R)[2:].zfill(8)[5:]
        G=bin(G)[2:].zfill(8)[5:]
        B=bin(B)[2:].zfill(8)[6:]
        res=R+G+B
        asci=int(res,2)
        try:
            if asci<128 and asci>31:
                r = chr(asci)
                final.append(r)
        except ValueError:
            continue
    print "Decrypted Text: " + ''.join(final)


if __name__ == '__main__':

    Tk().withdraw()
    filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
    im=Image.open(filename)

    plaintext = raw_input('Enter the text to hide:')
    lenofstr = len(plaintext)
    digest = text_to_bits(plaintext)

    encode(im,digest,lenofstr,im.size)
    im.save('temp.png')
    im1=Image.open('temp.png')
    decode(im1,im1.size)
