import socket

byte_message = bytes("5", "utf-8")
opened_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
opened_socket.sendto(byte_message, ("192.168.100.100", 4210)) #Please enter device IP address
self.opened_socket.shutdown(socket.SHUT_RDWR)
self.opened_socket.close()
print("Clock started")
