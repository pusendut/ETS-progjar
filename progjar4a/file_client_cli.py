import socket
import json
import base64
import logging

server_address = ('127.0.0.1', 6666)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message ")

        if isinstance(command_str, dict):
            message = json.dumps(command_str) + "\r\n\r\n"
            sock.sendall(message.encode())
        else:
            sock.sendall((command_str + "\r\n\r\n").encode())

        data_received = ""
        while True:
            data = sock.recv(1024)
            if data:
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                break

        hasil = json.loads(data_received.strip("\r\n\r\n"))
        logging.warning("data received from server:")
        return hasil
    except Exception as e:
        logging.warning(f"error during data receiving: {e}")
        return False



def remote_list():
    command_str=f"LIST"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        print("daftar file : ")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
        return True
    else:
        print("Gagal")
        return False

def remote_get(filename=""):
    command_str=f"GET {filename}"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        #proses file dalam bentuk base64 ke bentuk bytes
        namafile= hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        fp = open(namafile,'wb+')
        fp.write(isifile)
        fp.close()
        return True
    else:
        print("Gagal")
        return False

def remote_upload(filename=""):
    try:
        with open(filename, 'rb') as f:
            content = base64.b64encode(f.read()).decode()
        command_dict = {
            "command": "upload",
            "filename": filename,
            "content": content
        }
        hasil = send_command(command_dict)
        if hasil['status'] == 'OK':
            print(f"Upload berhasil: {hasil['data']}")
            return True
        else:
            print("Upload gagal:", hasil['data'])
            return False
    except Exception as e:
        print("Error:", e)
        return False

if __name__=='__main__':
    server_address = ('127.0.0.1', 6666)
    remote_list()
    remote_get('donalbebek.jpg')

