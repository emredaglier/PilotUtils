import os
from sys import platform
from utils.utils import Parse

head = ("Pilot Utils | Emre Daglier\n"
        "--------------------------\n\n")


def clr():
    if platform == "linux" or platform == "linux2":
        os.system("clear")
    elif platform == "win32":
        os.system("cls")


def menu():
    clr()

    data = (head +
            "[1] Request Weather Data"
            "\n\n")

    print(data)
    Input = input('>>\t')

    navigate(Input)


def navigate(Input):
    if Input == "1":
        clr()
        print(head)

        req = input('ICAO >>\t')
        req_no_refresh = input('Do you want to refresh the cached data (y\\n) >>\t').lower()
        if req_no_refresh == 'y':
            _ = Parse(req, False)

        else:
            _ = Parse(req, True)

        _.main()
        input('\n\nPress Enter to continue...')


    #elif ...

    else:
        pass
