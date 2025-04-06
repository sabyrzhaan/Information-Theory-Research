import time
import zlib
import lzma
import bz2
import random
import string

# Random text data generation
data = ''.join(random.choices(string.ascii_letters + string.digits, k=1000000))
encoded_data = data.encode()

# zlib compression
start_time = time.time()
zlib_compressed = zlib.compress(encoded_data)
zlib_compression_time = time.time() - start_time

start_time = time.time()
zlib_decompressed = zlib.decompress(zlib_compressed)
zlib_decompression_time = time.time() - start_time

# lzma compression
start_time = time.time()
lzma_compressed = lzma.compress(encoded_data)
lzma_compression_time = time.time() - start_time

start_time = time.time()
lzma_decompressed = lzma.decompress(lzma_compressed)
lzma_decompression_time = time.time() - start_time

# bz2 compression
start_time = time.time()
bz2_compressed = bz2.compress(encoded_data)
bz2_compression_time = time.time() - start_time

start_time = time.time()
bz2_decompressed = bz2.decompress(bz2_compressed)
bz2_decompression_time = time.time() - start_time

# Compression ratios
zlib_ratio = len(zlib_compressed) / len(encoded_data)
lzma_ratio = len(lzma_compressed) / len(encoded_data)
bz2_ratio = len(bz2_compressed) / len(encoded_data)

# Output results
print(f"zlib - Compression Time: {zlib_compression_time:.4f}s, Decompression Time: {zlib_decompression_time:.4f}s, Compression Ratio: {zlib_ratio:.4f}")
print(f"lzma - Compression Time: {lzma_compression_time:.4f}s, Decompression Time: {lzma_decompression_time:.4f}s, Compression Ratio: {lzma_ratio:.4f}")
print(f"bz2  - Compression Time: {bz2_compression_time:.4f}s, Decompression Time: {bz2_decompression_time:.4f}s, Compression Ratio: {bz2_ratio:.4f}")
