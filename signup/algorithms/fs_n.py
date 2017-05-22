#!/usr/bin/python

import sys, os,random ,string
import aes
import blow
import merge
import trans

kilobytes = 1024
megabytes = kilobytes * 1000



def split(file, todir,doc):
    """if not os.path.exists(todir):  # caller handles errors
        os.mkdir(todir)  # make dir, read/write parts
    else:
    """
    for fname in os.listdir(todir):  # delete any existing files
            os.remove(os.path.join(todir, fname))
    partnum = 0

    filesize=file.size #os.path.getsize(fromfile)
    chunksize = int(filesize / 3)
    lastchunksize = filesize - 2*chunksize
    for partnum in range(1, 3):  # eof=empty string from read
        chunk = file.read(chunksize)  # get next part <= chunksize
        buildchunk(chunk,partnum,'w',todir,doc)
    chunk=file.read(lastchunksize)
    if chunk :
        buildchunk(chunk,3,'a',todir,doc)
    mergedFilename = os.path.join(todir, ('MergedFile'))
    print('merged filename: '+ mergedFilename)

    f=merge.join(todir,mergedFilename)
    delete(todir)
    return f



def buildchunk(chunk,partnum,type,todir,doc):
    filename = os.path.join(todir, ('part%04d' % partnum))
    if type=='w':
        fileobj = open(filename, 'wb')
    if type=='a':
        fileobj=open(filename, 'a+')
    fileobj.write(chunk)
    fileobj.close()  # or simply open(  ).write(  )
    if partnum==1:
        k1 = randomword(10)
        doc.key1=k1
        key=aes.getKey(k1)
        aes.encrypt(key, filename,doc)
    if partnum==2:
        k2 = random.randint(8, 15)
        doc.key2=str(k2)
        trans.encrypt(filename,k2,doc)
    if partnum==3:
        k3 = randomword(10)
        doc.key3=k3
        blow.encrypt(filename,filename+"(encrypted)",k3,doc)

def delete(todir):
    parts = os.listdir(todir)
    for filename in parts:
        if filename.startswith("part"):
            os.remove(os.path.join(todir, filename))

def randomword(length):
    return ''.join(random.choice(string.lowercase)for i in range(length))
