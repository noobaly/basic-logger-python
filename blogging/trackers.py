# Imports

import os

from pathlib import Path

from datetime import datetime

import blogging.iofunctions as iofuncs

# ------------------


kilobytes1 = 1000 # bytes

megabyte1 = 1000000 # bytes

gigabyte1 = 1000000000 # bytes

tday = datetime.today()

day, month, year, hour, minute = str(tday.day), str(tday.month), str(tday.year), str(tday.hour), str(tday.minute)

def create_old_backup(path, passage):

    if not passage:
        return 
    fname = f"{os.path.basename(path)} {day} {month} {year} {hour} {minute}"

    old_file = os.path.abspath(path).replace(f"{os.path.basename(path)}", "") + fname
    
    if os.path.exists(old_file):
        fname = fname + str(datetime.today().second)

    with open(path, "r") as f:

        data = None
        i = 0
        iofuncs.overwrite(old_file, "")
        for line in f.readlines():
            iofuncs.write(old_file, line)

def log_file_size(path: str, size: list, create_old: bool):


    should_raise = True

    log_size: int = os.path.getsize(path)

    size_type = size[1]
    size_int = int(size[0])

    refresh_message = f"INFORMATION: Limited size for the log file was reached so the log file was refreshed!\n"
    
    if "kb" == size_type:


        if log_size // kilobytes1 > size_int:

            create_old_backup(path, create_old)
            iofuncs.overwrite(path, "INFORMATION: Limited size for the log file was reached so the log file was refreshed!\n")
    

        should_raise = False

    elif "mb" == size_type:
        if log_size // megabyte1 > size_int:

            create_old_backup(path, create_old)
            iofuncs.overwrite(path, "INFORMATION: Limited size for the log file was reached so the log file was refreshed!\n")


        should_raise = False

    elif "gb" == size_type:

        if log_size // gigabyte1 > size_int:

            create_old_backup(path, create_old)
            iofuncs.overwrite(path, f"INFORMATION: Limited size for the log file was reached so the log file was refreshed!\n")
            

        should_raise = False

    if should_raise:

        raise Exception("Declare a unit (kb/mb/gb) for the file size")






    


