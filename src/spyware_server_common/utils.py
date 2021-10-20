import bcrypt

def hashStr (text) : 
    if type(text) == str : text = text.encode()
    hashed = bcrypt.hashpw(text, bcrypt.gensalt())
    return hashed.decode()