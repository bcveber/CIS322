from passlib.apps import custom_app_context as pwd_context

def hash_password(password):
    return pwd_context.encrypt(password)

def verify_password(password, hashVal):
    return pwd_context.verify(password, hashVal)

if __name__ == "__main__":
    testPass = "UOCIS322"
    hVal = hash_password(testPass)
    print (hVal)
    if verify_password(testPass, hVal):
        print ("Success")
    else:
        print ("Failure")
