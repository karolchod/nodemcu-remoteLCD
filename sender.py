import socket
opened_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while 1:
            try:
                text = input()
                if text == "exit":
                    break
                byte_message = bytes(text, "utf-8")
                opened_socket.sendto(byte_message, ("000.000.000.000", 4210)) #Please enter device IP address
            except KeyboardInterrupt:
                print("Powrot")
                # byte_message = bytes("9", "utf-8")
                # opened_socket.sendto(byte_message, ("000.000.000.000", 4210))
                break

self.opened_socket.shutdown(socket.SHUT_RDWR)
self.opened_socket.close()

