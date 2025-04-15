import cv2
import os
import numpy as np
import pickle

# Initialiser ansiktsgjenkjenner
recognizer = cv2.face.LBPHFaceRecognizer_create()
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

faces = []
labels = []
label_map = {}

label_id = 0
for name in os.listdir("dataset"):
    person_path = os.path.join("dataset", name)
    if not os.path.isdir(person_path):
        continue

    label_map[label_id] = name

    for image_name in os.listdir(person_path):
        image_path = os.path.join(person_path, image_name)
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        if image is None:
            continue

        faces_rect = face_cascade.detectMultiScale(image, scaleFactor=1.3, minNeighbors=5)
        for (x, y, w, h) in faces_rect:
            roi = image[y:y+h, x:x+w]
            faces.append(roi)
            labels.append(label_id)

    label_id += 1

# Tren og lagre modellen
recognizer.train(faces, np.array(labels))
recognizer.save("trainer.yml")

with open("labels.pkl", "wb") as f:
    pickle.dump(label_map, f)

print("[INFO] Modell trent og lagret som 'trainer.yml'")
print("[INFO] Navneetiketter lagret som 'labels.pkl'")
