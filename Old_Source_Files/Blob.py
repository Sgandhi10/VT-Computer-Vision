import numpy as np
import cv2

class Blob:
    def __init__(self):
        self.pixels = []  # List of (x, y) coordinates of blob pixels

    def add_pixel(self, x, y):
        self.pixels.append((x, y))

    # return mins x,y and max x,y
    def return_rect():
        min_x = min(self.pixel, key=lambda x: x[0])[0]
        min_y = min(self.pixel, key=lambda x: x[1])[1]
        max_x = max(self.pixel, key=lambda x: x[0])[0]
        max_y = max(self.pixel, key=lambda x: x[1])[1]
        return min_x, min_y, max_x, max_y

    def __repr__(self):
        return f"Blob with {len(self.pixels)} pixels"

def detect_blobs(image):
    """
    Detect blobs in a binary image and return a list of Blob objects.
    :param image: 2D binary NumPy array (0 for background, 255 for foreground)
    :return: List of Blob objects
    """
    rows, cols = image.shape
    visited = np.zeros_like(image, dtype=bool)  # Keep track of visited pixels
    blobs = []  # List to store Blob objects

    def flood_fill(x, y, blob):
        """Flood-fill to find all connected pixels of a blob."""
        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            if (0 <= cx < rows and 0 <= cy < cols and
                    not visited[cx, cy] and image[cx, cy] == 255):
                visited[cx, cy] = True
                blob.add_pixel(cx, cy)
                # Add neighbors (8-connectivity)
                # Add neighbors within a 9x9 kernel (radius = 4)
                neighbors = [
                    (cx + dx, cy + dy)
                    for dx in range(-4, 5)  # Offset from -4 to 4 (inclusive)
                    for dy in range(-4, 5)
                    if dx != 0 or dy != 0  # Exclude the current pixel
                ]
                stack.extend(neighbors)

    # Traverse the image in raster order
    for x in range(rows):
        for y in range(cols):
            if image[x, y] == 255 and not visited[x, y]:
                # Start a new blob
                blob = Blob()
                flood_fill(x, y, blob)
                blobs.append(blob)

    return blobs

# Example usage
if __name__ == "__main__":
    # Example binary image (0 = background, 255 = foreground)
    binary_image = cv2.imread("out/mask.jpg", cv2.IMREAD_GRAYSCALE)

    binary_mask = np.array([
    [0, 0, 255, 255, 255, 0, 0, 0, 0],
    [0, 255, 255, 0, 255, 255, 0, 0, 0],
    [0, 255, 0, 0, 0, 255, 0, 255, 255],
    [0, 0, 0, 0, 255, 255, 255, 255, 255],
    [0, 0, 255, 255, 255, 0, 0, 0, 0],
    [255, 255, 255, 0, 0, 0, 0, 255, 255],
    [0, 0, 0, 0, 0, 0, 255, 255, 0],
    [0, 0, 0, 255, 255, 255, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ], dtype=np.uint8)

    # Detect connected components
    num_labels, labels = cv2.connectedComponents(binary_image)
    print(str(num_labels))
   
