# Imports


# --------------------

def write(path: str, message: str):

    with open(path, "a") as file:

        file.write(message)

def overwrite(path: str, message: str):

    with open(path, "w") as file:

        file.write(message)



def console(message: str):
    
    pass

        