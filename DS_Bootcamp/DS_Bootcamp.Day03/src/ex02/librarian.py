import os
import subprocess
import sys

def check_virtual_env():
    try:
        virtual_env = os.environ['VIRTUAL_ENV']
        virtual_env = virtual_env.split("/")
        if virtual_env[len(virtual_env)-1] != "armondvi":
            raise NameError("Неверное название виртуальной среды")
    except KeyError:
        print("Нет активной виртуальной среды.")


def install_libraries():
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'beautifulsoup4', 'pytest', '--break-system-packages'])


def save_requirements():
    with open('requirements.txt', 'w') as f:
        result = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
        print(result.decode('utf-8'))
        f.write(result.decode('utf-8'))

def archive_virtual_env():
    env_path = os.path.dirname(sys.prefix)
    archive_name = 'armondvi.tar.gz'
    subprocess.check_call(['tar', '-czvf', archive_name, env_path])
    print(f"Virtual environment archived as {archive_name}")


if __name__ == "__main__":
    try:
        check_virtual_env()
        install_libraries()
        save_requirements()
        archive_virtual_env()
    except NameError as e:
        print(e)

