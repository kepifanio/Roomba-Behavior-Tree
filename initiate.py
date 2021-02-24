import sys

def general_clean():
    Y = "Y\n"
    N = "N\n"
    print("Should I perform general cleaning? (Y/N)")
    general_clean = sys.stdin.readline()
    if general_clean == Y:
        return True
    elif general_clean == N:
        return False
    else:
        print("Invalid entry")
        exit()

def spot_clean():
    Y = "Y\n"
    N = "N\n"
    print("Should I perform spot cleaning? (Y/N)")
    spot_clean = sys.stdin.readline()
    if spot_clean == Y:
        return True
    elif spot_clean == N:
        return False
    else:
        print("Invalid entry")
        exit()
