import sys

def caesar():
    if len(sys.argv) == 4 and (sys.argv[1] == 'encode' or sys.argv[1] == 'decode'):
        text = sys.argv[2]
        if not text.isascii():
            raise Exception("Text is not ascii")
        
        code(text, sys.argv[1])     
    else:
        raise Exception("Wrong usage")
    


def code(text, status):
    result = ''
    for letter in text:
        if letter.isalpha():
                shift = int(sys.argv[3])
                if status == 'decode':
                    shift = -1*shift

                if letter.islower():
                    shifted = (ord(letter) - ord('a') + shift) % 26
                    result += chr(ord('a') + shifted)
                else:
                    shifted = (ord(letter) - ord('A') + shift) % 26
                    result += chr(ord('A') + shifted)

        else:
            result += letter

    print(result)


if __name__ == '__main__':
    try:
        caesar()
    except Exception as e:
        print(e)
