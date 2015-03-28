#
#  Turn your compressed saved SCN into a OTTN file with:
#
#  dd if=test.scn of=test.ottn.lzma skip=8 bs=1
#  7za x test.ottn.lzma
#  


import struct

from StringIO import StringIO

f   = open('test.ottn','rb')
out = open('new.scn','wb')

out.write( 'OTTN\x00\xC2\x00\x00' )

# Header looks like this
# 4F 54 54 4E  00 C2 00 00

#f.read(8)

done = 0
while not done:
  try:
    chunktype = f.read(4)
    data = f.read(1)
  except:
    done = 1
    chunktype = ''
    data = ''

  if data == '\x02':

    # Just flush the rest after VEHS for now..
    print chunktype,'SPARSE?'
    out.write(chunktype + data + f.read())
    done = 1

    #print chunktype,'SPARSE?'
    #data = f.read(256)
    #print data.encode('hex')

  elif not done and chunktype:
    data = data + f.read(3)
    size = struct.unpack('>I',data)[0]
    print chunktype,data.encode('hex'),size
    data = f.read(size)

    # Let's tweak!
    newdata = StringIO()
    if chunktype == 'MAPT':
      for i in range(0,len(data)):
        #print data[i].encode('hex')
        #if data != '\x00' and data != '\x01':
        #  newdata.write( '\x01' )
        #if data[i] == '\x02':
        #  print i,data[i].encode('hex')

        # This changes all land tiles to black tiles in game..
        # Just to prove this scenario tweaker method works.. More to come! :-)

        if data[i] != '\x60':
          newdata.write( '\x70' )
        else:
          newdata.write( data[i] )
          #print data[i].encode('hex')
      newdata.seek(0)
      data = newdata.getvalue()

    out.write(chunktype+struct.pack('>I',size)+data)
