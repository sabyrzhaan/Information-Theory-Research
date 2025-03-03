from concurrent.futures import ThreadPoolExecutor


# Function to perform multi-threaded compression
def compress_data(data):
    start_time = time.time()


compressed_data = zlib.compress(data.encode())
compression_time = time.time() - start_time

return compressed_data, compression_time

# Sample data for compression
data = "This is a sample text for compression testing." * 1000

# Using multi-threading for compression
with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(compress_data, [data] * 4))  # Running compression in parallel

# Displaying compression times for each thread
for i, (compressed, comp_time) in enumerate(results):
    print(f"Thread {i + 1}: Compression Time = {comp_time:.6f} seconds")

    pass

with ThreadPoolExecutor() as executor:
    executor.map(compress_data, [data] * 4)
