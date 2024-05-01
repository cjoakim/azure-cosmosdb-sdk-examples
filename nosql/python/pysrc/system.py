""" module system.py, Chris Joakim, Microsoft, 2023 """

import os
import platform
import socket
import sys
import time
import traceback

import psutil

class System():
    """
    This class is an interface to system information such as memory usage.
    """

    @classmethod
    def command_line_args(cls) -> list[str]:
        """ Return sys.argv """
        return sys.argv

    @classmethod
    def platform(cls) -> str:
        """ Return the platform.system() string. """
        return platform.system()

    @classmethod
    def is_windows(cls) -> bool:
        """ Return True if the platform is Windows, else False. """
        return 'win' in cls.platform().lower()

    @classmethod
    def is_mac(cls) -> bool:
        """ Return True if the platform is Apple macOS, else False. """
        return 'darwin' in cls.platform().lower()

    @classmethod
    def pid(cls) -> int:
        """ Return the current process id int. """
        return os.getpid()

    @classmethod
    def process_name(cls) -> str:
        """ Return the current process name. """
        return psutil.Process().name()

    @classmethod
    def user(cls) -> str:
        """ Return the current user name; os.getlogin(). """
        return os.getlogin()

    @classmethod
    def hostname(cls) -> str:
        """ Return the current hostname; socket.gethostname(). """
        try:
            return socket.gethostname()
        except Exception as excp:
            print(str(excp))
            print(traceback.format_exc())
            return 'unknown'

    @classmethod
    def cwd(cls) -> str:
        """ Return the current working directory; Process.cwd(). """
        return psutil.Process().cwd()

    @classmethod
    def pwd(cls) -> str:
        """ Return the current working directory; os.getcwd() """
        return os.getcwd()

    @classmethod
    def platform_info(cls) -> str:
        """ Return a string with the platform info including processor. """
        return f'{platform.platform()} : {platform.processor()}'

    @classmethod
    def cpu_count(cls) -> int:
        """ Return the number of CPUs on the system. """
        return psutil.cpu_count(logical=False)

    @classmethod
    def memory_info(cls):
        """ Return the memory info for the current process. """
        return psutil.Process().memory_info()

    @classmethod
    def virtual_memory(cls):
        """ Return the virtual memory info for the current process. """
        return psutil.virtual_memory()

    @classmethod
    def epoch(cls) -> float:
        """ Return the current epoch time in seconds, as a float """
        return time.time()

    @classmethod
    def sleep(cls, seconds=1.0) -> None:
        """ Sleep for the given number of float seconds. """
        time.sleep(seconds)
