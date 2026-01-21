import cv2
import numpy as np

video_path = "car2.mp4"
cap = cv2.VideoCapture(video_path)

ret, old_frame = cap.read()
if not ret:
    print("Erreur lecture vidéo")
    cap.release()
    exit()

old_frame = cv2.resize(old_frame, (320, 240))
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

mask_draw = np.zeros_like(old_frame)
traj = []

cv2.namedWindow("Trajectoire automatique", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Trajectoire automatique", 640, 480)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (320, 240))
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Flux optique dense Farneback (rapide et pratique)
    flow = cv2.calcOpticalFlowFarneback(
        old_gray, frame_gray, None,
        0.5, 3, 15, 3, 5, 1.2, 0
    )

    # Calcul de la magnitude
    mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
    # Seuil pour pixels en mouvement
    threshold = 1.0
    moving_pixels = np.where(mag > threshold)

    if len(moving_pixels[0]) > 0:
        # Centre de masse du mouvement
        cy = int(np.mean(moving_pixels[0]))
        cx = int(np.mean(moving_pixels[1]))
        traj.append((cx, cy))

    # Dessiner la trajectoire
    for i in range(1, len(traj)):
        cv2.line(mask_draw, traj[i-1], traj[i], (0,0,255), 2)

    # Dessiner le vecteur direction actuel
    if len(traj) >= 2:
        cv2.arrowedLine(frame, traj[-2], traj[-1], (0,255,0), 2, tipLength=0.3)

    # Point courant
    if len(traj) >= 1:
        cv2.circle(frame, traj[-1], 5, (255,0,0), -1)

    frame = cv2.add(frame, mask_draw)
    cv2.imshow("Trajectoire automatique", frame)

    old_gray = frame_gray.copy()
    if cv2.waitKey(30) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
