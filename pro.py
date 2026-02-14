import cv2
import numpy as np
import mediapipe as mp
import time
from math import hypot

W, H = 640, 480
WINDOW_NAME = "Virtual Paint"

cap = cv2.VideoCapture(0)
cap.set(3, W)
cap.set(4, H)

canvas = np.zeros((H, W, 3), np.uint8)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

palette = [
    (0, 0, 255),
    (0, 255, 0),
    (255, 0, 0),
    (0, 255, 255),
    (255, 255, 255)
]
palette_names = ["Red", "Green", "Blue", "Yellow", "White"]
selected_idx = 0
draw_color = palette[selected_idx]

brush_thickness = 7
eraser_thickness = 50
pinch_px = 35

xp, yp = 0, 0
last_save_time = 0
last_color_time = 0
cooldown = 0.5


def fingers_up(lms):
    tip_ids = [4, 8, 12, 16, 20]
    res = []
    thumb_is_open = lms.landmark[tip_ids[0]].x < lms.landmark[tip_ids[0] - 1].x
    res.append(1 if thumb_is_open else 0)
    for i in range(1, 5):
        tip = lms.landmark[tip_ids[i]].y
        pip = lms.landmark[tip_ids[i] - 2].y
        res.append(1 if tip < pip else 0)
    return res


def draw_toolbar(frame, selected_idx):
    cell_w = W // len(palette)
    for i, color in enumerate(palette):
        x1, x2 = i * cell_w, (i + 1) * cell_w
        y1, y2 = 0, 80
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, -1)
        if i == selected_idx:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 3)
        cv2.putText(frame, palette_names[i], (x1 + 10, 55),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)


def select_color_by_x(x):
    cell_w = W // len(palette)
    return min(len(palette) - 1, max(0, x // cell_w))


def next_colour():
    global selected_idx, draw_color
    selected_idx = (selected_idx + 1) % len(palette)
    draw_color = palette[selected_idx]


def combine(frame, canvas):
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, inv = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY_INV)
    inv = cv2.cvtColor(inv, cv2.COLOR_GRAY2BGR)
    frame = cv2.bitwise_and(frame, inv)
    frame = cv2.bitwise_or(frame, canvas)
    return frame


print("Controls:")
print("  Index finger = Draw")
print("  Pinch (index+thumb) = Erase")
print("  Index+Middle = Change colour")
print("  Five fingers = Clear canvas")
print("  's' = save | 'q' or Esc = quit")

cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)

while True:
    ok, frame = cap.read()
    if not ok:
        break
    frame = cv2.flip(frame, 1)
    draw_toolbar(frame, selected_idx)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        lms = results.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, lms, mp_hands.HAND_CONNECTIONS)

        h, w, _ = frame.shape
        ix, iy = int(lms.landmark[8].x * w), int(lms.landmark[8].y * h)
        mx, my = int(lms.landmark[12].x * w), int(lms.landmark[12].y * h)
        tx, ty = int(lms.landmark[4].x * w), int(lms.landmark[4].y * h)

        fingers = fingers_up(lms)

        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0 and iy < 80:
            selected_idx = select_color_by_x(ix)
            draw_color = palette[selected_idx]
            xp, yp = 0, 0
            cv2.putText(frame, f"Color: {palette_names[selected_idx]}",
                        (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (50, 50, 50), 2)

        elif fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0 and iy >= 80:
            if time.time() - last_color_time > cooldown:
                next_colour()
                last_color_time = time.time()
            xp, yp = 0, 0
            cv2.putText(frame, f"Brush: {palette_names[selected_idx]}",
                        (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (50, 50, 50), 2)

        elif hypot(ix - tx, iy - ty) < pinch_px:
            if xp == 0 and yp == 0:
                xp, yp = ix, iy
            cv2.circle(frame, (ix, iy), 18, (0, 0, 0), -1)
            cv2.line(canvas, (xp, yp), (ix, iy), (0, 0, 0), eraser_thickness)
            xp, yp = ix, iy

        elif fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
            cv2.circle(frame, (ix, iy), 7, draw_color, -1)
            if xp == 0 and yp == 0:
                xp, yp = ix, iy
            cv2.line(canvas, (xp, yp), (ix, iy), draw_color, brush_thickness)
            xp, yp = ix, iy

        elif sum(fingers) == 5:
            canvas[:] = 0
            xp, yp = 0, 0
            cv2.putText(frame, "Canvas Cleared", (10, 110),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        else:
            xp, yp = 0, 0

    out = combine(frame, canvas)
    cv2.putText(out, f"Brush: {palette_names[selected_idx]}  Thickness:{brush_thickness}",
                (10, H - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (30, 30, 30), 2)

    cv2.imshow(WINDOW_NAME, out)
    if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
        break

    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        now = int(time.time())
        fname = f"paint_{now}.png"
        cv2.imwrite(fname, out)
        last_save_time = now
        print(f"Saved {fname}")

    if key in (ord('q'), 27):
        break

cap.release()
cv2.destroyAllWindows()
