from PIL import Image
import math

def getbits(byteData):
    bitData = [0] * len(byteData) * 4
    for i in range(len(byteData)):
        bitData[4*i] = byteData[i]&3
        bitData[4*i+1] = (byteData[i]&12)>>2
        bitData[4*i+2] = (byteData[i]&48)>>4
        bitData[4*i+3] = (byteData[i]&192)>>6
    return bitData

def getMaxSize(imgData):
    maxSize = imgData.size[0]*imgData.size[1]*6
    return maxSize

def fileSizeStoreBits(maxSize):
    storeBit = math.log2(maxSize)
    storePixels = math.ceil(storeBit/6)
    storeBits = storePixels*3
    return storeBits

imageFileName = input("Input image (insert path or name):")
messageInFileName = input("Input file (insert path or name):")
imageOutFileName = input("Output image (insert path or name):")

message = open(messageInFileName,"rb")

messageBytes = message.read()

message.close()

messageBits = getbits(messageBytes)

img = Image.open(imageFileName)

pixels = img.load()

position = 0
nextColor = 0
finish = False

bitsLength = len(messageBits)
maxSize = getMaxSize(img)
storeBitsSize = fileSizeStoreBits(maxSize)

if bitsLength*2 < (maxSize - storeBitsSize*2):

    bitFileSize = [0] * storeBitsSize

    for i in range(storeBitsSize):
        mask = 3<<(2*i)
        bitFileSize[i] = (bitsLength&mask)>>(2*i)


    for i in range(math.ceil(storeBitsSize/3)):
        colorReplace = [0] * 3

        colorReplace[0] = (pixels[img.size[0]-1,img.size[1]-1-i][0]&252) + bitFileSize[3*i]
        colorReplace[1] = (pixels[img.size[0]-1,img.size[1]-1-i][1]&252) + bitFileSize[3*i+1]
        colorReplace[2] = (pixels[img.size[0]-1,img.size[1]-1-i][2]&252) + bitFileSize[3*i+2]

        pixels[img.size[0]-1,img.size[1]-1-i] = (colorReplace[0],colorReplace[1],colorReplace[2])


    for i in range(img.size[0]):
        for j in range(img.size[1]):
            currentBitsInt = [0] * 3
            for k in range(3):
                if 3*position + k < bitsLength:
                    currentBitsInt[k] = messageBits[3*position + k]
                else:
                    finish = True
                    currentBitsInt[k] = 0
        
            position += 1

            colorReplace = [0] * 3

            colorReplace[0] = (pixels[i,j][0]&252) + currentBitsInt[0]
            colorReplace[1] = (pixels[i,j][1]&252) + currentBitsInt[1]
            colorReplace[2] = (pixels[i,j][2]&252) + currentBitsInt[2]

            pixels[i,j] = (colorReplace[0],colorReplace[1],colorReplace[2])

            if finish:
                break
            
        if finish:
            break    

    img.save(imageOutFileName)

    print("Finished creating the output image!("+imageOutFileName+")")

else:
    print("Input file is too big for this image!")
    print("Max File Size: "+str(math.floor((maxSize - 2*storeBitsSize)/8))+" bytes")
    print("File Size: "+str(math.floor((bitsLength)/4))+" bytes")
    print("Get an image with a higher resolution or shorten your input file")

response = input("\n\nPress Enter to exit...\n")


