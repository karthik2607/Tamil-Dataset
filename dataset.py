import cv2
import numpy as np
import os

# Initialize parameters
canvas_size = 512
canvas = np.ones((canvas_size, canvas_size), dtype="uint8") * 255
drawing = False
ix, iy = -1, -1

# Path where the dataset will be saved
dataset_dir = "dataset"

# Create the dataset directory if it doesn't exist
if not os.path.exists(dataset_dir):
    os.makedirs(dataset_dir)
    print(f"Created directory: {dataset_dir}")
else:
    print(f"Directory already exists: {dataset_dir}")

# Function to draw on canvas
def draw(event, x, y, flags, param):
    global ix, iy, drawing, canvas

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.line(canvas, (ix, iy), (x, y), (0, 0, 0), thickness=5)
            ix, iy = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.line(canvas, (ix, iy), (x, y), (0, 0, 0), thickness=5)

# Get the next available filename
def get_next_filename():
    files = os.listdir(dataset_dir)
    if len(files) == 0:
        return "0.png"
    else:
        # Get the largest numbered file and increment it by 1
        latest_file = max([int(f.split('.')[0]) for f in files])
        return f"{latest_file + 1}.png"

cv2.namedWindow("Draw")
cv2.setMouseCallback("Draw", draw)

print("Draw on the window. Press 's' to save the image or 'q' to quit.")

while True:
    cv2.imshow("Draw", canvas)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        # Save the image with the next available filename
        filename = get_next_filename()
        save_path = os.path.join(dataset_dir, filename)
        cv2.imwrite(save_path, canvas)
        print(f"Image saved as {save_path}")
        canvas = np.ones((canvas_size, canvas_size), dtype="uint8") * 255  # Reset the canvas
    
    elif key == ord('q'):
        break

cv2.destroyAllWindows()
