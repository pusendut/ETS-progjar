import json
import logging
import shlex
from file_interface import FileInterface

class FileProtocol:
    def __init__(self):
        self.file = FileInterface()

    def proses_string(self, string_datamasuk=''):
        logging.warning(f"string diproses: {string_datamasuk[:100]}...")
        try:
            # Jika data dalam format JSON (upload)
            if string_datamasuk.strip().startswith('{'):
                data = json.loads(string_datamasuk)
                if data.get("command") == "upload":
                    return json.dumps(
                        self.file.upload([data["filename"], data["content"]])
                    )

            # Jika data dalam format CLI-style (LIST, GET)
            c = shlex.split(string_datamasuk.lower())
            c_request = c[0].strip()
            logging.warning(f"memproses request: {c_request}")
            params = [x for x in c[1:]]
            cl = getattr(self.file, c_request)(params)
            return json.dumps(cl)

        except Exception as e:
            return json.dumps(dict(status='ERROR', data=str(e)))

if __name__ == '__main__':
    fp = FileProtocol()
    print(fp.proses_string("LIST"))
    print(fp.proses_string("GET pokijan.jpg"))
