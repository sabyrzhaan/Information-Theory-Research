import psutil

# Function to measure CPU/Memory usage
def measure_usage():
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    return cpu_usage, memory_usage

cpu, memory = measure_usage()
print(f"CPU Usage: {cpu}%, Memory Usage: {memory}%")
