import wave
import math

def getbytes(bitData):
    byteLength = math.ceil(len(bitData)/4)
    byteData = bytearray(byteLength)
    bitConvert = [0] * 4
    for i in range(byteLength):
        bitConvert[0] = bitData[4*i]
        bitConvert[1] = (bitData[4*i + 1])<<2
        bitConvert[2] = (bitData[4*i + 2])<<4
        bitConvert[3] = (bitData[4*i + 3])<<6

        byteData[i] = bitConvert[0] + bitConvert[1] + bitConvert[2] + bitConvert[3]

    byteDataOutput = bytes(byteData)
    return byteDataOutput

def getMaxSize(soundData):
    maxSize = soundData.getnframes()*2
    return maxSize

def fileSizeStoreBits(maxSize):
    storeBit = math.log2(maxSize)
    storeBits = math.ceil(storeBit/2)
    return storeBits

soundFileName = input("Input sound file (insert path or name):")
messageFileName = input("Output file (insert path or name):")

sound = wave.open(soundFileName,"rb")

soundFrames = [bytearray(4)]*sound.getnframes()
for i in range(sound.getnframes()):
    soundFrames[i] = bytearray(sound.readframes(1))

numFrames = sound.getnframes()
maxSize = getMaxSize(sound)
storeBitsSize = fileSizeStoreBits(maxSize)
sound.close()

bitFileSize = [0] * storeBitsSize

for i in range(storeBitsSize):
    bitFileSize[i] = (soundFrames[numFrames-1-i][0])&3

bitLength = 0

for i in range(storeBitsSize):
    bitLength = bitLength + (bitFileSize[i]<<(2*i))

messageBits = [0] * bitLength

for i in range(bitLength):
    messageBits[i] = soundFrames[i][0]&3
    
message = open(messageFileName,"wb")

messageBytes = getbytes(messageBits)

message.write(messageBytes)
message.close()