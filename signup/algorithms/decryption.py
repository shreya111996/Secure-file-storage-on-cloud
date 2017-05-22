#!/usr/bin/python


import sys, os
import aes
import blow
import dmerge
import trans
kilobytes = 1024
megabytes = kilobytes * 1000



def split(fromfile, todir,doc):
    if not os.path.exists(todir):
        os.mkdir(todir)
    else:
        for fname in os.listdir(todir):  # delete any existing files
            os.remove(os.path.join(todir, fname))
    partnum = 0
    inp = open(fromfile, 'rb')  # use binary mode on Windows
    filesize=os.path.getsize(fromfile)


    for partnum in range(1, 4):
        if(partnum==1):
            chunksize = doc.size1
        elif(partnum==2):
            chunksize = doc.size2
        else:
            chunksize = doc.size3
        chunk = inp.read(chunksize)  # get next part <= chunksize
        buildchunk(chunk,partnum,'w',todir,doc)

    inp.close()
    mergedFilename = os.path.join(todir, 'Merged.txt')
    print('merged filename: '+ mergedFilename) 
    file=dmerge.join(todir,mergedFilename)
    delete(todir)
    return file

def buildchunk(chunk,partnum,type,todir,doc):
    filename = os.path.join(todir, ('part%04d' % partnum))
    if type=='w':
        fileobj = open(filename, 'wb')
    if type=='a':
        fileobj=open(filename, 'a+')
    fileobj.write(chunk)
    fileobj.close()
    if partnum==1:
        key=aes.getKey(doc.key1)
        aes.decrypt(key, filename)
    if partnum==2:
        key=int(doc.key2)
        trans.decrypt(filename,key)
    if partnum==3:
        blow.decrypt(filename,filename+"(decrypted)",doc.key3)

def delete(todir):
    parts = os.listdir(todir)
    for filename in parts:
        if filename.startswith("part"):
            os.remove(os.path.join(todir, filename))


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == '-help':
        print 'Use: split.py [file-to-split target-dir [chunksize]]'
    else:
        if len(sys.argv) < 3:
            interactive = 1
            fromfile = raw_input('File to be split? ')  # input if clicked
            todir = raw_input('Directory to store part files? ')
        else:
            interactive = 0
            fromfile, todir = sys.argv[1:3]
        absfrom, absto = map(os.path.abspath, [fromfile, todir])
        print 'Splitting', absfrom, 'to', absto, 'by'

        try:
            parts = split(fromfile, todir)
        except:
            print 'Error during split:'
            print sys.exc_type, sys.exc_value
        else:
            print 'Split finished:', parts, 'parts are in', absto
        if interactive: raw_input('Press Enter key')