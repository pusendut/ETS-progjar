import time
import os
import csv
from concurrent.futures import ThreadPoolExecutor
from file_client_cli import remote_upload, remote_get

CSV_FILE = 'stress_results.csv'

def stress_test_worker(op, filename):
    start = time.time()
    success = False
    try:
        if op == 'upload':
            success = remote_upload(filename)
        elif op == 'download':
            success = remote_get(filename)
        else:
            raise Exception("Unknown operation")
    except Exception as e:
        success = False

    end = time.time()
    duration = end - start
    try:
        size = os.path.getsize(filename)
    except:
        size = 0
    throughput = size / duration if duration > 0 else 0
    return (success, duration, throughput)

def run_stress_test(op, file, client_workers, server_workers, volume):
    success_count = 0
    fail_count = 0
    total_time = 0
    total_throughput = 0

    with ThreadPoolExecutor(max_workers=client_workers) as executor:
        futures = [executor.submit(stress_test_worker, op, file) for _ in range(client_workers)]
        for f in futures:
            try:
                success, duration, throughput = f.result()
                if success:
                    success_count += 1
                    total_time += duration
                    total_throughput += throughput
                else:
                    fail_count += 1
            except:
                fail_count += 1

    avg_time = total_time / success_count if success_count else 0
    avg_tp = total_throughput / success_count if success_count else 0

    result = {
        "Operasi": op,
        "Volume": volume,
        "Client Pool": client_workers,
        "Server Pool": server_workers,
        "Waktu Total per Client (s)": round(avg_time, 4),
        "Throughput per Client (B/s)": round(avg_tp, 2),
        "Client Sukses/Gagal": f"{success_count}/{fail_count}",
        "Server Sukses/Gagal": f"{success_count}/{fail_count}"
    }

    save_to_csv(result)
    return result

def save_to_csv(row):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

if __name__ == "__main__":
    hasil = run_stress_test(
        op="download",
        file="donalbebek.jpg",
        client_workers=50,
        server_workers=50,    # ← kamu isikan nilai sesuai server yang sedang jalan
        volume="100MB"        # ← label ukuran file
    )
    print(hasil)
