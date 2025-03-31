#Более интеллектуальный выбор алгоритма

import time
import zlib
import lzma
import cv2
import numpy as np
import soundfile as sf
import os
import psutil
from skimage.metrics import structural_similarity as ssim
from scipy.io import wavfile
from concurrent.futures import ThreadPoolExecutor

# Получение метрик системы
def get_system_metrics():
    process = psutil.Process()
    cpu_usage = psutil.cpu_percent(interval=0.1)
    memory_usage = process.memory_info().rss / (1024 * 1024)
    return cpu_usage, memory_usage

# Вычисление степени сжатия
def calculate_compression_ratio(input_path, output_path):
    original_size = os.path.getsize(input_path)
    compressed_size = os.path.getsize(output_path)
    return original_size / compressed_size

# Сжатие изображений в формате JPEG
def compress_image_jpeg(input_image_path, output_image_path, quality=90):
    image = cv2.imread(input_image_path)
    start_time = time.time()
    cv2.imwrite(output_image_path, image, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
    compression_time = time.time() - start_time
    return compression_time

# Сжатие видео с использованием H.264
def compress_video_h264(input_video_path, output_video_path):
    cap = cv2.VideoCapture(input_video_path)
    fourcc = cv2.VideoWriter_fourcc(*'X264')
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
    start_time = time.time()
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
    compression_time = time.time() - start_time
    cap.release()
    out.release()
    return compression_time

# Сжатие аудио с использованием FLAC
def compress_audio_flac(input_audio_path, output_audio_path):
    data, samplerate = sf.read(input_audio_path)
    start_time = time.time()
    sf.write(output_audio_path, data, samplerate, format='FLAC')
    compression_time = time.time() - start_time
    return compression_time

# Декомпрессия файла
def decompress_file(input_path, output_path, algorithm):
    start_time = time.time()
    if algorithm == 'zlib':
        with open(input_path, 'rb') as f:
            compressed_data = f.read()
            decompressed_data = zlib.decompress(compressed_data)
            with open(output_path, 'wb') as df:
                df.write(decompressed_data)
    elif algorithm == 'lzma':
        with lzma.open(input_path, 'rb') as f:
            decompressed_data = f.read()
            with open(output_path, 'wb') as df:
                df.write(decompressed_data)
    decompression_time = time.time() - start_time
    return decompression_time

# Интеллектуальный выбор алгоритма на основе сценария использования
def choose_best_algorithm(data_type, file_size, real_time=False):
    if real_time:
        if data_type == 'video':
            return 'h264'
        elif data_type == 'audio':
            return 'flac'
        else:
            return 'zlib'
    else:
        if data_type == 'image':
            return 'jpeg' if file_size < 5 * 1024 * 1024 else 'lzma'
        elif data_type == 'video':
            return 'h264'
        elif data_type == 'audio':
            return 'flac' if file_size < 10 * 1024 * 1024 else 'lzma'
        else:
            return 'lzma' if file_size > 1 * 1024 * 1024 else 'zlib'

# Запуск эксперимента с измерением метрик
def run_experiment(input_path, output_path, data_type, real_time=False):
    file_size = os.path.getsize(input_path)
    algorithm = choose_best_algorithm(data_type, file_size, real_time)
    start_cpu, start_memory = get_system_metrics()

    compression_time = 0
    if algorithm == 'jpeg':
        compression_time = compress_image_jpeg(input_path, output_path)
    elif algorithm == 'h264':
        compression_time = compress_video_h264(input_path, output_path)
    elif algorithm == 'flac':
        compression_time = compress_audio_flac(input_path, output_path)
    else:
        with open(input_path, 'rb') as f:
            data = f.read()
            start_time = time.time()
            compressed_data = zlib.compress(data)
            compression_time = time.time() - start_time
            with open(output_path, 'wb') as cf:
                cf.write(compressed_data)

    decompression_time = decompress_file(output_path, 'decompressed_'+output_path, algorithm)
    compression_ratio = calculate_compression_ratio(input_path, output_path)
    end_cpu, end_memory = get_system_metrics()
    cpu_usage = abs(end_cpu - start_cpu)
    memory_usage = abs(end_memory - start_memory)

    print(f"Algorithm: {algorithm}")
    print(f"Compression Time: {compression_time:.4f} seconds")
    print(f"Decompression Time: {decompression_time:.4f} seconds")
    print(f"Compression Ratio: {compression_ratio:.2f}")
    print(f"CPU Usage: {cpu_usage:.2f}%")
    print(f"Memory Usage: {memory_usage:.2f} MB")

# Пример запуска экспериментов
run_experiment('example.jpg', 'compressed.jpg', 'image')
run_experiment('example.mp4', 'compressed.mp4', 'video', real_time=True)
run_experiment('example.wav', 'compressed.flac', 'audio', real_time=True)
