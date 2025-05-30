import socket
import logging
from concurrent.futures import ThreadPoolExecutor
from file_protocol import FileProtocol

fp = FileProtocol()

def process_client(connection, address):
    logging.warning(f"connection from {address}")
    try:
        buffer = ""
        while True:
            data = connection.recv(1024)
            if not data:
                break
            buffer += data.decode()
            if "\r\n\r\n" in buffer:
                break

        hasil = fp.proses_string(buffer.strip("\r\n\r\n"))
        hasil += "\r\n\r\n"
        connection.sendall(hasil.encode())
    except Exception as e:
        logging.error(f"error: {e}")
    finally:
        connection.close()

def main(ip='0.0.0.0', port=6666, max_workers=1):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((ip, port))
    sock.listen(100)
    logging.warning(f"server listening on {ip}:{port} with thread pool {max_workers}")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        while True:
            conn, addr = sock.accept()
            executor.submit(process_client, conn, addr)

if __name__ == "__main__":
    main()