# Imports

import blogging.iofunctions as writer

import blogging.trackers

from threading import currentThread as this

from datetime import datetime

import pip._vendor.colorama as colorama

import sys


# ------------------
INFORMATIVE = "INFORMATION"
ERROR = "ERROR"
CRITICAL = "CRITICAL"
WARNING = "WARNING"


class logger:
    tday = datetime.today()

    day, month, year, hour, minute = str(tday.day), str(tday.month), str(tday.year), str(tday.hour), str(tday.minute)   

    def __init__(self, **kwargs):

        """
        Parameters:

        file = str //Path to file

        filler = str //Decorator for the log file, default is an empty string

        tracksize = str //Whether the log file's size should be maintained
        Usage is a little interesting, here's how:

        356-kb -> means 356 kilobytes is the size limit for the log file once it hits the limit it gets refreshed.

        528-mb -> means 528 megabytes

        5-gb -> means 5 gigabytes

        after the "tracksize" parameter you can also pass in the:
        create_old = bool parameter. This creates an old version of the log file before refreshing

        thread_info = bool //Whether the log info should have the name of the thread it was ran on.

        timestamp = bool //Whether the log info should have the the time when log command was executed.

        colorise = bool //Whether the console logs should be colorised or not.
        
        """

        keys = kwargs.keys()

        if "file" in keys:

            self.is_file = True

            if "filler" in keys:

                self.filler = kwargs['filler']
            else:
                self.filler = ""

            if "tracksize" in keys:

                if kwargs['tracksize'].find("-") == -1:
                    raise Exception("Wrong size format!\nExamples of good size format: \"10-kb\", \"200-mb\" , \"2-gb\"")     

                self.should_tracksize = True
                self.size = kwargs['tracksize'].split("-")

                if "create_old" in keys:

                    self.create_olds = kwargs['create_old']

                else:
                    self.create_olds = False
                    

            else:

                self.should_tracksize = False

            self.LOG_FILE = kwargs['file']

        if "thread_info" in keys and kwargs['thread_info']:

            self.should_thread_sensetive = True

        else:
            self.should_thread_sensetive = False

        if "timestamp" in keys and kwargs['timestamp']:

            self.timer = True

        else:

            self.timer = False

        if "colorise" in keys:

            self.is_colorised = kwargs['colorise']

        else:

            self.is_colorised = False



    def file_log(self, message: str, level: str):

        """Used to log informantion to a file
        
            message = str //The information you want to log

            level = str //Level of severity you can use logger.level, level being one of these:
                    (INFORMATIVE, WARNING, ERROR, CRITICAL)
        """

        old_message = message
        message = ""

        if self.should_thread_sensetive:
            thread_name = this().name
            thread = "main" if thread_name == "MainThread" else thread_name
            message = f"from {thread}: "

        if level == INFORMATIVE:

            message += f"{INFORMATIVE}: {old_message}\n" if not self.timer else f"{INFORMATIVE}: {old_message} at ({f'{self.month}-{self.day}-{self.year}, {self.hour}:{self.minute}'})\n"

        elif level == ERROR:
            message += f"{ERROR}: {old_message}\n" if not self.timer else f"{ERROR}: {old_message} at ({f'{self.month}-{self.day}-{self.year}, {self.hour}:{self.minute}'})\n"

        elif level == CRITICAL:
            message += f"{CRITICAL}: {old_message}\n" if not self.timer else f"{CRITICAL}: {old_message} at ({f'{self.month}-{self.day}-{self.year}, {self.hour}:{self.minute}'})\n"

        
        elif level == WARNING:
            message += f"{CRITICAL}: {old_message}\n" if not self.timer else f"{WARNING}: {old_message} at ({f'{self.month}-{self.day}-{self.year}, {self.hour}:{self.minute}'})\n"


        else:
            message += f"{level}: {old_message}\n" if not self.timer else f"{level}: {old_message}\n" if not self.timer else f"{level}: ({f'{self.month}-{self.day}-{self.year}, {self.hour}:{self.minute}'}) {old_message}\n"


        message += self.filler*20 + "\n"

        writer.write(path = self.LOG_FILE, message=message)

        if self.should_tracksize:
            blogging.trackers.log_file_size(path=self.LOG_FILE, size=self.size, create_old=self.create_olds)

        del old_message


        del message

    def console_log(self, message: str, level: str):

        """Used to log informantion to the console
        
            message = str //The information you want to log

            level = str //Level of severity you can use logger.level, level being one of these:
                    (INFORMATIVE, WARNING, ERROR, CRITICAL)
        """

        if self.is_colorised:    

            if level == INFORMATIVE: 
                message = colorama.Fore.GREEN + level+ ":" + colorama.Fore.WHITE + " " + message

            elif level == WARNING: 
                message = colorama.Fore.YELLOW + level+ ":" + colorama.Fore.WHITE  + " " +message

            elif level == CRITICAL: 
                message = colorama.Fore.RED + level+ ":" + colorama.Fore.WHITE + " " + message

            elif level == ERROR: 
                message = colorama.Fore.RED + level+ ":" + colorama.Fore.WHITE  + " " + message

            else: 
                
                message = level+ ":" + " " + message

        else: 
            
            message = level+ ":" + " " + message

        if self.should_thread_sensetive:
            thread_name = this().name
            thread = "main" if thread_name == "MainThread" else thread_name
            message = f"from {thread}: {message}" if not message else f"from {thread}: {message}"

        if self.timer:

            message += f" at ({f'{self.month}-{self.day}-{self.year}, {self.hour}:{self.minute}'})"


        out = sys.stdout

        out.write(message + "\n")

        out.flush()

    def log_both(self, message: str, level: str):

        """Used to log informantion to the console and to a file at the same time
        
            message = str //The information you want to log

            level = str //Level of severity you can use logger.level, level being one of these:
                    (INFORMATIVE, WARNING, ERROR, CRITICAL)
        """

        self.file_log(message, level)

        self.console_log(message, level)

    
