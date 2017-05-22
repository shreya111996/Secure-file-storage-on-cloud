# Transposition Cipher Encrypt/Decrypt File


import os
def encrypt(inputFilename, key,doc):

    fileObj = open(inputFilename,'rb')
    message = fileObj.read()
    fileObj.close()
    outputFilename = inputFilename + "(encrypted)"
    index = 0
    count = 0
    cipher = []

    for letter in message:
        cipher.append(message[index])
        index += key

        if index > len(message) - 1:
            count += 1
            index = count

    translated = ''.join(cipher)
    outputFileObj = open(outputFilename, 'wb')
    outputFileObj.write(translated)
    outputFileObj.close()
    s = os.path.getsize(outputFilename)
    doc.size2=s


def decrypt(filename, key):

    fileObj = open(filename,'rb')
    cipher = fileObj.read()
    fileObj.close()
    outputFilename = filename + "(decrypted)"
    message = [''] * len(cipher)
    index = 0
    count = 0

    for letter in cipher:
        message[index] = letter
        index += key
        if index > len(cipher) - 1:
            count += 1
            index = count

    translated = ''.join(message)
    outputFileObj = open(outputFilename, 'wb')
    outputFileObj.write(translated)
    outputFileObj.close()

def main():
    inputFilename = raw_input("Enter input filename")

    myKey = 10
    myMode = raw_input("Enter choice encrypt or decrypt( E or D )"); # set to 'encrypt' or 'decrypt'



    if myMode == 'E':
         encrypt(inputFilename, myKey)
    elif myMode == 'D':
         decrypt(inputFilename, myKey)


if __name__ == '__main__':
     main()