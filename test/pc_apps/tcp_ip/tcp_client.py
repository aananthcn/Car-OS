#
# Created on Wed Feb 21 2024 3:33:48 PM
#
# The MIT License (MIT)
# Copyright (c) 2024 Aananth C N
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
import socket
import time


def get_current_time():
    current_time = time.time()
    milliseconds = int((current_time - int(current_time)) * 1000)
    formatted_time = time.strftime("%H:%M:%S", time.localtime(current_time))
    return f"{formatted_time}.{milliseconds:03d}"


def main():
    # Define the server IP address and port
    server_ip = '192.168.3.100'
    server_port = 1000

    try:
        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        client_socket.connect((server_ip, server_port))
        print(f"[{get_current_time()}] Connected to {server_ip}:{server_port}")

        while True:
            # Send the message
            message = "Hello AUTOSAR TcpIp!"
            client_socket.sendall(message.encode())
            print(f"[{get_current_time()}] Sent: {message}")

            # Receive the response
            client_socket.settimeout(5.0)
            try:
                response = client_socket.recv(1024).decode()
                print(f"[{get_current_time()}] Received: {response}")
            except TimeoutError:
                print("TimeoutError: timed out!")

            # Wait for X second
            time.sleep(2)

    except ConnectionRefusedError:
        print("Connection refused. Make sure the server is running.")
    except KeyboardInterrupt:
        print("\nClient terminated by user.")
    finally:
        # Close the socket
        client_socket.close()


if __name__ == "__main__":
    main()