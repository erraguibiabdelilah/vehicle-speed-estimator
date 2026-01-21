import cv2
import numpy as np

video_path = "car2.mp4"
cap = cv2.VideoCapture(video_path)

ret, old_frame = cap.read()
if not ret:
    print("Impossible de lire la vidéo")
    cap.release()
    exit()

old_frame = cv2.resize(old_frame, (640, 480))
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

# Sélection manuelle du point
clicked_point = (612,291)


# Initialisation point Lucas-Kanade
p0 = np.array([[[clicked_point[0], clicked_point[1]]]], dtype=np.float32)

lk_params = dict(
    winSize=(21, 21),
    maxLevel=3,
    criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 0.01)
)

mask_draw = np.zeros_like(old_frame)
old_gray_copy = old_gray.copy()

cv2.namedWindow("Trajectoire", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Trajectoire", 900, 600)

# =============================
# Boucle principale
# =============================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray_copy, frame_gray, p0, None, **lk_params)

    if p1 is not None and st[0] == 1:
        new = p1[0][0]
        old = p0[0][0]

        a, b = int(new[0]), int(new[1])
        c, d = int(old[0]), int(old[1])

        # Dessin du vecteur de mouvement
        cv2.arrowedLine(frame, (c, d), (a, b), (0, 255, 0), 2, tipLength=0.3)
        # Trajectoire
        mask_draw = cv2.line(mask_draw, (a, b), (c, d), (0, 0, 255), 2)
        # Point courant
        frame = cv2.circle(frame, (a, b), 5, (255, 0, 0), -1)

        # Mise à jour
        old_gray_copy = frame_gray.copy()
        p0 = p1.copy()

    img = cv2.add(frame, mask_draw)
    cv2.imshow("Trajectoire", img)

    if cv2.waitKey(30) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
