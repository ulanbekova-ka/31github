import cv2

# Load the pre-trained face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load an image from file
image_path = '/Users/kulanbekova/Downloads/angry.jpeg'
img = cv2.imread(image_path)

# Convert the image to grayscale (face detection works better in grayscale)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

# Draw rectangles around the faces
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

# Display the result
cv2.imshow('Detected Faces', img)

# Wait for a key press and close the window
cv2.waitKey(0)
cv2.destroyAllWindows()
