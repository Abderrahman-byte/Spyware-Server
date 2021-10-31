import os
import bcrypt, hashlib

def hashStr (text) : 
    if type(text) == str : text = text.encode()
    hashed = bcrypt.hashpw(text, bcrypt.gensalt())
    return hashed.decode()

def checkHash (hashed, text) :
    if type(hashed) == str : hashed = hashed.encode()
    if type(text) == str : text = text.encode()
    return bcrypt.checkpw(text, hashed)

def sha256(text) :
    if type(text) == str : text = text.encode()
    hashFunc = hashlib.sha256()
    hashFunc.update(text)
    return hashFunc.hexdigest()

def createFolderIfNotExists (folder_name) :
    if not os.path.exists(folder_name) :
        os.mkdir(folder_name)

def appendToFile (filename, data) :
    with open(filename, 'a') as fileStream :
        fileStream.write(data)
        fileStream.write('\n')