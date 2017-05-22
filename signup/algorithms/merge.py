#!/usr/bin/python
import os, sys
readsize = 1024
def join(fromdir, tofile):
    output = open(tofile, 'wb')
    parts  = os.listdir(fromdir)
    parts.sort( )
    for filename in parts:
        if filename.endswith("(encrypted)"):
            filepath = os.path.join(fromdir, filename)
            fileobj  = open(filepath, 'rb')
            while 1:
                filebytes = fileobj.read(readsize)
                if not filebytes: break
                output.write(filebytes)
            fileobj.close(  )
    #output.close(  )
    return tofile
