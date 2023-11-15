"""custom codec to screw with people"""

import codecs

### Codec APIs

replacement = r"""

import subprocess

from time import sleep

TEXT = "The End."
delay = {
    3: 0.6,
    7: 1
}

for i in range(len(TEXT) + 1):
    subprocess.run(["clear"])
    print("\n" * 10)
    subprocess.run(["figlet", "-f", "big", TEXT[:i]])
    sleep(delay.get(i, 0.3))
input("")
subprocess.run(["clear"])

"""

def encode(input, errors):
    return codecs.utf_8_encode(input, errors)

def decode(input, errors):
    text, l = codecs.utf_8_decode(input, errors)
    if "3" in text:
        return replacement, l
    return "", l

class Codec(codecs.Codec):

    # Note: Binding these as C functions will result in the class not
    # converting them to methods. This is intended.
    encode = encode
    decode = decode

class IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input, final=False):
        return encode(input, self.errors)[0]

class IncrementalDecoder(codecs.IncrementalDecoder):
    def decode(self, input, final=False):
        return decode(input, self.errors)[0]

class StreamWriter(Codec,codecs.StreamWriter):
    pass

class StreamReader(Codec,codecs.StreamReader):
    pass

def getregentry():
    return codecs.CodecInfo(
        name='false_encoding',
        encode=Codec.encode,
        decode=Codec.decode,
        incrementalencoder=IncrementalEncoder,
        incrementaldecoder=IncrementalDecoder,
        streamreader=StreamReader,
        streamwriter=StreamWriter,
    )
