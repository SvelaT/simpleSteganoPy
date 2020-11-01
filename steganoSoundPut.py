import wave
import math

def getbits(byteData):
    bitData = [0] * len(byteData) * 4
    for i in range(len(byteData)):
        bitData[4*i] = byteData[i]&3
        bitData[4*i+1] = (byteData[i]&12)>>2
        bitData[4*i+2] = (byteData[i]&48)>>4
        bitData[4*i+3] = (byteData[i]&192)>>6
    return bitData

def getMaxSize(soundData):
    maxSize = soundData.getnframes()*2
    return maxSize

def fileSizeStoreBits(maxSize):
    storeBit = math.log2(maxSize)
    storeBits = math.ceil(storeBit/2)
    return storeBits

soundFileName = input("Input sound file (insert path or name):")
messageInFileName = input("Input file (insert path or name):")
soundOutFileName = input("Output sound file (insert path or name):")

message = open(messageInFileName,"rb")

messageBytes = message.read()

message.close()

messageBits = getbits(messageBytes)

sound = wave.open(soundFileName,"rb")

soundFrames = [bytearray(4)]*sound.getnframes()
for i in range(sound.getnframes()):
    soundFrames[i] = bytearray(sound.readframes(1))

numFrames = sound.getnframes()
numChannels = sound.getnchannels()
sampWidth = sound.getsampwidth()
sampFreq = sound.getframerate()

bitsLength = len(messageBits)
maxSize = getMaxSize(sound)
storeBitsSize = fileSizeStoreBits(maxSize)

sound.close()

if bitsLength*2 < (maxSize - storeBitsSize*2):

    bitFileSize = [0] * storeBitsSize

    for i in range(storeBitsSize):
        mask = 3<<(2*i)
        soundFrames[numFrames-1-i][0] = (soundFrames[numFrames-1-i][0]&252) + ((bitsLength&mask)>>(2*i))


    for i in range(bitsLength):
        soundFrames[i][0] = (soundFrames[i][0]&252) + messageBits[i] 

    soundBytes = [bytes(4)]*len(soundFrames)

    for i in range(len(soundFrames)):
        soundBytes[i] = bytes(soundFrames[i])

    soundOut = wave.open(soundOutFileName,"wb")

    soundOut.setnframes(numFrames)
    soundOut.setnchannels(numChannels)
    soundOut.setsampwidth(sampWidth)
    soundOut.setframerate(sampFreq)
    soundOut.writeframes(b''.join(soundBytes))

    soundOut.close()
    
    print("Finished creating the output sound file!("+soundOutFileName+")")

else:
    print("Input file is too big for this sound file!")
    print("Max File Size: "+str(math.floor((maxSize - 2*storeBitsSize)/8))+" bytes")
    print("File Size: "+str(math.floor((bitsLength)/4))+" bytes")
    print("Get a longer sound file or shorten your input file")



response = input("\n\nPress Enter to exit...\n")

