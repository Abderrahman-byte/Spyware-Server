import bcrypt

def hashStr (text) : 
    if type(text) == str : text = text.encode()
    hashed = bcrypt.hashpw(text, bcrypt.gensalt())
    return hashed.decode()

def checkHash (hashed, text) :
    if type(hashed) == str : hashed = hashed.encode()
    if type(text) == str : text = text.encode()
    return bcrypt.checkpw(text, hashed)