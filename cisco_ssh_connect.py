#!/usr/bin/env python3


## copyright:   B1 Systems GmbH <info@b1-systems.de>
## license:     GPLv3+, http://www.gnu.org/licenses/gpl-3.0.html
## author:      Ott, Brian <bott@b1-systems.de>
## description: 
## version:     0.1


import paramiko
import threading
import getpass


def main():
    num_switches = int(input("Enter the number of Cisco switches to connect to: "))


    if num_switches == 1:
        hostname = input("Enter the hostname of the switch: ")
        username = input("Enter the SSH username (default is 'admin'): ") or "admin"
        password = getpass.getpass("Enter the password: ")


        ssh_connect(hostname, username, password)


    elif num_switches > 1:
        switches = []
        for i in range(num_switches):
            switch = input(f"Enter the hostname of the switch #{i+1}: ")
            switches.append(switch)


        threads = []
        for switch in switches:
            username = input(f"Enter the SSH username for {switch} (default is 'admin'): ") or "admin"
            password = getpass.getpass(f"Enter the password for {switch}: ")

            
            thread = threading.Thread(target=ssh_connect, args=(switch, username, password))
            threads.append(thread)
            thread.start()


        for thread in threads:
            thread.join()


    else:
        print("Invalid number of switches. Please enter a valid number.")


def ssh_connect(hostname, username, password):
    try:


        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
                hostname,
                username=username,
                password=password, 
                allow_agent=False,
                look_for_keys=False,
                timeout=10
        )


        stdin, stdout, stderr = client.exec_command("show version")
        output = stdout.read().decode('utf-8')


        with open(f"switch_{hostname}.txt", 'w') as file:
            file.write(output)


        print(f"Output for {hostname} retrieved and saved in switch_{hostname}.txt")


    except Exception as e:
        print(f"Error connecting to {hostname}: {str(e)}")


    finally:
        client.close()


if __name__ == '__main__':
    main()
