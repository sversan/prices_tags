import maskpass
from colorama import Fore

pwd = maskpass.askpass(prompt="Enter Password: ")
print(pwd)
print(Fore.CYAN, "Success, You Can Do IT!")
