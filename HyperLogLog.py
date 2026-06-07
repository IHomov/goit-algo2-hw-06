import re
import time
from datasketch import HyperLogLog

#regular expression for validating IPv4 addresses
IP_PATTERN = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')

def load_logs(file_path: str):

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                match = IP_PATTERN.search(line)
                if match:
                    yield match.group()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return


def exact_count(file_path: str) -> tuple:
    # Use a set to store unique IP addresses
    start_time = time.time()
    unique_ips = set()
    for ip in load_logs(file_path):
        unique_ips.add(ip)
    execution_time = time.time() - start_time
    return len(unique_ips), execution_time

def approximate_count(file_path: str, p: int = 14) -> tuple:
    # Use HyperLogLog for approximate counting of unique IP addresses
    start_time = time.time()
    hll = HyperLogLog(p=p)
    for ip in load_logs(file_path):
        hll.update(ip.encode('utf-8'))
    execution_time = time.time() - start_time
    return hll.count(), execution_time

def display_results(exact_res, exact_time, hll_res, hll_time):

    print("\nResults comparison :")
    print(f"{'':<25} {'Exact Count':<20} {'HyperLogLog':<20}")
    print("-" * 68)
    print(f"{'Unique elements':<25} {exact_res:<20.1f} {hll_res:<20.1f}")
    print(f"{'Execution time (s)':<25} {exact_time:<20.4f} {hll_time:<20.4f}")

    # Calculate and display the percentage error of HyperLogLog compared to the exact count
    error = abs(exact_res - hll_res) / exact_res * 100 if exact_res > 0 else 0
    print(f"\nPercentage error of HyperLogLog: {error:.2f}%")

if __name__ == "__main__":
    file_path = "lms-stage-access.log"  

    print(" Starting an accurate count (set)...")
    exact_res, exact_time = exact_count(file_path)
    
    print("Starting an approximate calculation (HyperLogLog)...")
    hll_res, hll_time = approximate_count(file_path)
    
    # Display the final table
    display_results(exact_res, exact_time, hll_res, hll_time)