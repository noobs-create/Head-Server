import sys
import colorama

from datetime import datetime, timezone, timedelta
from colorama import Fore

colorama.init(autoreset=True)

def _GetTimeStamp() -> str:
    now = datetime.now()
    
    return str(now.strftime("%d/%m/%Y At %H:%M:%S"))

def _GetCaller() -> str:
    try:
        script_name = str(sys._getframe(2).f_globals.get('__name__', 'Unknown'))
        
        if str(script_name) == "__main__":
            return "Bootstrap"
        else:
            return str(script_name)
    except Exception:
        return "Unknown"

def _PrintHelp(ForeColor, TypeString: str, Console: str, Caller: str, TimeStamp: str):
    print(f"{str(TimeStamp)} - [{ForeColor}{str(TypeString)}{Fore.RESET}]: {str(Console)} | {Fore.CYAN}[{str(Caller)}]{Fore.RESET}", flush=True)


def error(Text: str):
    _PrintHelp(ForeColor=Fore.RED, TypeString="ERROR", Console=Text, Caller=str(_GetCaller()), TimeStamp=str(_GetTimeStamp()))


def info(Text: str):
    _PrintHelp(ForeColor=Fore.BLUE, TypeString="INFO", Console=Text, Caller=str(_GetCaller()), TimeStamp=str(_GetTimeStamp()))


def log(Text: str):
    _PrintHelp(ForeColor=Fore.GREEN, TypeString="LOG", Console=Text, Caller=str(_GetCaller()), TimeStamp=str(_GetTimeStamp()))


def warn(Text: str):
    _PrintHelp(ForeColor=Fore.YELLOW, TypeString="WARN", Console=Text, Caller=str(_GetCaller()), TimeStamp=str(_GetTimeStamp()))


def debug(Text: str):
    _PrintHelp(ForeColor=Fore.MAGENTA, TypeString="DEBUG", Console=Text, Caller=str(_GetCaller()), TimeStamp=str(_GetTimeStamp()))