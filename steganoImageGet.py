from PIL import Image
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

def getMaxSize(imgData):
    maxSize = imgData.size[0]*imgData.size[1]*6
    return maxSize

def fileSizeStoreBits(maxSize):
    storeBit = math.log2(maxSize)
    storePixels = math.ceil(storeBit/6)
    storeBits = storePixels*3
    return storeBits

imageFileName = input("Input image (insert path or name):")
messageFileName = input("Output file (insert path or name):")

img = Image.open(imageFileName)

pixels = img.load()

maxSize = getMaxSize(img)
storeBitsSize = fileSizeStoreBits(maxSize)

bitFileSize = [0] * storeBitsSize

for i in range(math.ceil(storeBitsSize/3)):

    bitFileSize[3*i] = (pixels[img.size[0]-1,img.size[1]-1-i][0])&3
    bitFileSize[3*i+1] = (pixels[img.size[0]-1,img.size[1]-1-i][1])&3
    bitFileSize[3*i+2] = (pixels[img.size[0]-1,img.size[1]-1-i][2])&3

bitLength = 0

for i in range(storeBitsSize):
    bitLength = bitLength + (bitFileSize[i]<<(2*i))

messageBits = [0] * bitLength

position = 0
finish = False

for i in range(img.size[0]):
    for j in range(img.size[1]):
        currentBitsInt = [0]*3
        
        currentBitsInt[0] = pixels[i,j][0]&3
        currentBitsInt[1] = pixels[i,j][1]&3
        currentBitsInt[2] = pixels[i,j][2]&3

        for k in range(3):
            if position < bitLength:
                messageBits[position] = currentBitsInt[k]
                position += 1
            else:
                finish = True
        
        if finish:
            break

    if finish:
        break

message = open(messageFileName,"wb")

messageBytes = getbytes(messageBits)

message.write(messageBytes)
message.close()