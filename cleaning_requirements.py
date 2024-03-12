import subprocess
import re

requirements_file = 'requirements.txt'

def pip_uninstall(package_name): subprocess.call(['pip', 'uninstall', '-y', package_name])

def pip_install(package_name): subprocess.call(['pip', 'install', package_name])

with open(requirements_file, 'r') as file:
    for line in file:
        if '==' not in line:
            package_name = line.split('@')[0].strip()
            if package_name:
                print(f"Uninstalling {package_name}...")
                pip_uninstall(package_name)
                print(f"Reinstalling {package_name}...")
                pip_install(package_name)
        else:
            continue

print("Done processing requirements.txt.")
