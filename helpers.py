from string import ascii_lowercase
import random

def random_str(digit=7):
    return "".join([random.choice(ascii_lowercase) for i in range(digit)])