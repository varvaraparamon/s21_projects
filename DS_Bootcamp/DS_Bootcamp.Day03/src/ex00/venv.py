import os

def print_virtual_env():
    try:
        virtual_env = os.environ['VIRTUAL_ENV']
        print(f"Ваша текущая виртуальная среда: {virtual_env}")
    except KeyError:
        print("Нет активной виртуальной среды.")

if __name__ == "__main__":
    print_virtual_env()


