import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

def calculate_psnr(img1, img2):
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return float('inf')
    PIXEL_MAX = 255.0
    return 20 * np.log10(PIXEL_MAX / np.sqrt(mse))

video_path = '/Users/sabyrzhanolzhabay/PycharmProjects/pythonProject/ICT/sample_movie.mp4'
cap = cv2.VideoCapture(video_path)

# Read all frames into memory (for testing)
frames = []
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame_resized = cv2.resize(frame, (640, 480))
    frames.append(frame_resized)
cap.release()

# Save compressed video using default settings
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640, 480))
for frame in frames:
    out.write(frame)
out.release()

# Read compressed video
cap2 = cv2.VideoCapture('output.mp4')
compressed_frames = []
while cap2.isOpened():
    ret, frame = cap2.read()
    if not ret:
        break
    frame_resized = cv2.resize(frame, (640, 480))
    compressed_frames.append(frame_resized)
cap2.release()

# Compare PSNR and SSIM for the first frame
if frames and compressed_frames:
    original = frames[0]
    compressed = compressed_frames[0]

    psnr_value = calculate_psnr(original, compressed)
    ssim_value = ssim(original, compressed, channel_axis=-1)

    print(f"PSNR: {psnr_value:.2f}, SSIM: {ssim_value:.4f}")
else:
    print("Error reading frames for comparison.")
