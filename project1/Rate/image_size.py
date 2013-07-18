import StringIO
import struct
import urllib2

def getRemoteImageInfo(url):
    image = urllib2.urlopen(url)
    data = str(image.read(2))
    height = -1
    width = -1
    content_type = ''
    
    if data.startswith('\377\330'):
        content_type = 'image/jpeg'
        b = image.read(1)
        try:
            while (b and ord(b) != 0xDA):
                while (ord(b) != 0xFF): b = image.read(1)
                while (ord(b) == 0xFF): b = image.read(1)
                if (ord(b) >= 0xC0 and ord(b) <= 0xC3):
                    image.read(3)
                    h, w = struct.unpack(">HH", image.read(4))
                    break
                else:
                    image.read(int(struct.unpack(">H", image.read(2))[0])-2)
                b = image.read(1)
            width = int(w)
            height = int(h)
        except struct.error:
            pass
        except ValueError:
            pass
    return content_type, width, height

# imag2 = "http://i.imgur.com/rapwX.jpg"
# print getRemoteImageInfo(imag2)