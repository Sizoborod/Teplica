from random import sample, shuffle, choice
from sys import stdin
from string import digits, ascii_letters


def generate_token():
    token = ''
    letters = list(set(ascii_letters) - {'O', 'o', 'l', 'I', '1', '0'})
    for i in range(15):
        token += choice(letters)
    return token


def main(n, m):
    passwords = []
    for i in range(n):
        while (password := generate_token()) in passwords:
            pass
        passwords.append(password)

    return passwords

print(main(10, 0))