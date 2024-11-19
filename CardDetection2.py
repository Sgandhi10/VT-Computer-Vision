import cv2
import numpy as np

# Load the image
image = cv2.imread('test_images/card_detect2.jpg')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply thresholding to create a binary image
_, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

# Find contours
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Create a list to store rectangles
rectangles = []

# Minimum size for width and height of the blob
min_width = 200
min_height = 200

# Iterate over the contours and add bounding rectangles
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    if w >= min_width or h >= min_height:
        rectangles.append([x, y, x + w, y + h])

# Merge overlapping or nearby rectangles
def merge_rectangles(rects, threshold=10):
    merged_rects = []
    while rects:
        rect = rects.pop(0)
        x1, y1, x2, y2 = rect
        index = 0
        while index < len(rects):
            nx1, ny1, nx2, ny2 = rects[index]
            # Check if rectangles are close or overlapping
            if (x1 - threshold < nx2 and x2 + threshold > nx1 and
                y1 - threshold < ny2 and y2 + threshold > ny1):
                # Merge the rectangles
                x1 = min(x1, nx1)
                y1 = min(y1, ny1)
                x2 = max(x2, nx2)
                y2 = max(y2, ny2)
                rects.pop(index)
            else:
                index += 1
        merged_rects.append([x1, y1, x2, y2])
    return merged_rects

# Merge rectangles that are nearby or overlapping
merged_rectangles = merge_rectangles(rectangles)

# Draw the merged rectangles
for rect in merged_rectangles:
    x1, y1, x2, y2 = rect
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Display the result
cv2.imwrite('out/merged_rectangles.jpg', image)
