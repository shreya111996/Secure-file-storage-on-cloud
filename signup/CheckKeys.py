from .algorithms import steg

def check(doc,image):
    text=steg.Steganography.decode(image)
    if "$$DELIMITER$$" not in text:
        return 0
    x,y,z=text.split("$$DELIMITER$$")
    if(x!=doc.key1):
        return 0
    if(y!=doc.key2):
        return 0
    if(z!=doc.key3):
        return 0
    return 1