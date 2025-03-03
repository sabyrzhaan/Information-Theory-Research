import time
import zlib
import lzma
import bz2
import random
import string

# Random text data generation
data = ''.join(random.choices(string.ascii_letters + string.digits, k=1000000))

# zlib compression
start_time = time.time()
zlib_compressed = zlib.compress(data.encode())
zlib_compression_time = time.time() - start_time
zlib_decompression_time = time.time() - time.time()  # Decompression time

# lzma compression
start_time = time.time()
lzma_compressed = lzma.compress(data.encode())
lzma_compression_time = time.time() - start_time
lzma_decompression_time = time.time() - time.time()

# bz2 compression
start_time = time.time()
bz2_compressed = bz2.compress(data.encode())
bz2_compression_time = time.time() - start_time
bz2_decompression_time = time.time() - time.time()

# Compression ratios
zlib_ratio = len(zlib_compressed) / len(data)
lzma_ratio = len(lzma_compressed) / len(data)
bz2_ratio = len(bz2_compressed) / len(data)

# Output results
print(f"zlib Compression Time: {zlib_compression_time}s, Decompression Time: {zlib_decompression_time}s, Compression Ratio: {zlib_ratio}")
print(f"lzma Compression Time: {lzma_compression_time}s, Decompression Time: {lzma_decompression_time}s, Compression Ratio: {lzma_ratio}")
print(f"bz2 Compression Time: {bz2_compression_time}s, Decompression Time: {bz2_decompression_time}s, Compression Ratio: {bz2_ratio}")
