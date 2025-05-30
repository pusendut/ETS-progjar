import socket
import logging
from multiprocessing import Pool
from file_protocol import FileProtocol

fp = FileProtocol()

def handle_client(data):
    address, message = data
    hasil = fp.proses_string(message.decode())
    hasil += "\r\n\r\n"
    return (address, hasil.encode())

def main(ip='0.0.0.0', port=6666, workers=5):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((ip, port))
    sock.listen(100)
    logging.warning(f"server listening on {ip}:{port} with process pool {workers}")
    
    pool = Pool(workers)
    while True:
        conn, addr = sock.accept()
        data = conn.recv(1024)
        if not data:
            continue
        result = pool.apply(handle_client, [(addr, data)])
        if result:
            conn.sendall(result[1])
        conn.close()

if __name__ == "__main__":
    main()