class Color:
    # ANSI escape codes for text colors
    RED = '\033[91m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    BLACK = '\033[0m'
    def __init__(self):
        print("color")

    @staticmethod
    def red(text):
        return (f"{Color.BLACK}{Color.RED}{str(text)}{Color.RED}{Color.BLACK}")

    @staticmethod
    def yellow(text):
        return (f"{Color.BLACK}{Color.YELLOW}{str(text)}{Color.YELLOW}{Color.BLACK}")

    @staticmethod
    def green(text):
        return (f"{Color.BLACK}{Color.GREEN}{str(text)}{Color.GREEN}{Color.BLACK}")

    @staticmethod
    def black(text):
        return (f"{Color.BLACK}{str(text)}{Color.BLACK}")
