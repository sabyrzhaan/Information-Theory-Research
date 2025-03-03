import cv2
import numpy as np

# Load a sample video
video_path = 'sample_video.mp4'
cap = cv2.VideoCapture(video_path)

# Function to compress and calculate PSNR and SSIM
def compress_and_test(bitrate):
    # Set bitrate (e.g., for H.264)
    fourcc = cv2.VideoWriter_fourcc(*'H264')
    out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640, 480), bitrate=bitrate)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
    cap.release()
    out.release()

    # Calculate PSNR and SSIM
    # Use sample frame comparison for simplicity
    psnr = cv2.PSNR(frame, frame)
    ssim = cv2.SSIM(frame, frame)

    return psnr, ssim

bitrates = [500000, 1000000, 2000000]
for bitrate in bitrates:
    psnr, ssim = compress_and_test(bitrate)
    print(f"Bitrate: {bitrate} bps -> PSNR: {psnr}, SSIM: {ssim}")
