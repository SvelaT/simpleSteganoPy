# simpleSteganoPy

## A simple implementation of the steganography technique with PNG images(not tested with other image types)

## How to use?

1. You will need to have a file and an image or sound file(only tested on png's and wav's)
2. Put the image / sound, the input, the steganoImagePut.py / steganoSoundPut.py and the steganoImageGet.py / steganoSoundGet.py files on the same directory(it also works from seperate directories but you will have to specify the paths)
2. Run steganoImagePut.py / steganoSoundPut.py and follow the prompts, it should create an output image / sound file at the end
4. Run steganoImageGet.py / steganoSoundGet.py and follow the prompts to get the file back from the image / sound file

## Warnings

1. The files are not encripted! You could encript them before storing them on the image / sound file
2. Do not set the output image type to jpg or any other lossy compression image types as the file will be lost due to the lossy compression. They can be used as input images though.
3. For sound files only use wav files(input and output)

### Made by SvelaT

Watch my video: https://www.youtube.com/watch?v=t7xeyP9BGU8
