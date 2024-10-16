import cv2
import numpy as np
import matplotlib.pyplot as plt

def snake_contours_A(image, contours, mm_per_pixel):
    """
    ฟังก์ชันแสดงข้อมูลพื้นที่และจำนวนฟอง
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    areas = []  # เก็บพื้นที่ของฟองแต่ละฟอง

    for i, contour in enumerate(contours, 1):
        M = cv2.moments(contour)
        if M['m00'] != 0:
            # คำนวณจุดศูนย์กลางของฟอง
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])

            # คำนวณพื้นที่ในหน่วยพิกเซลและแปลงเป็น mm²
            area_px = cv2.contourArea(contour)
            area_mm = area_px * (mm_per_pixel ** 2)
            areas.append(area_mm)

            # แสดงหมายเลขฟองบนภาพ
            text = f"{i}"
            fontScale = 0.6
            thickness = 1
            cv2.putText(image, text, (cx, cy), font, fontScale, (255, 0, 0), thickness, cv2.LINE_AA)

            # พิมพ์ข้อมูลพื้นที่แต่ละฟอง
            print(f"{i}: Area = {area_mm:.6f} mm²")

    # คำนวณและแสดงค่าเฉลี่ยของพื้นที่
    if areas:
        avg_area = sum(areas) / len(areas)
        print(f"Average area: {avg_area:.6f} mm²")

    # แสดงจำนวนฟองที่ตรวจพบทั้งหมด
    print(f"Total number of bubbles detected: {len(contours)}")

# โหลดและเตรียมรูปภาพ
image = cv2.imread('S1.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Gaussian Blur เพื่อลด noise และ smooth ภาพ
blur = cv2.GaussianBlur(gray, (11, 11), 0)

# ใช้ Canny Edge Detection เพื่อตรวจจับขอบ
canny = cv2.Canny(blur, 30, 150)

# Dilation เพื่อขยายขอบ
dilated = cv2.dilate(canny, (1, 1), iterations=1)

# ค้นหา Contours ของฟอง
contours, _ = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# แปลงภาพเป็น RGB เพื่อวาด Contours
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
cv2.drawContours(rgb, contours, -1, (0, 255, 0), 2)

# **คำนวณ mm/pixel:** ใช้ข้อมูลจากการ Calibration ที่ให้มา
mm_per_pixel = 0.72 / 2.71  # 0.265686 mm/pixel

# เรียกใช้ฟังก์ชัน snake_contours_A เพื่อแสดงข้อมูลฟอง
snake_contours_A(rgb, contours, mm_per_pixel)

# แสดงผลลัพธ์ภาพพร้อม Contours และหมายเลขฟอง
plt.figure("Bubble Detection")
plt.imshow(rgb)
plt.xticks([]), plt.yticks([])
plt.title('Final Detection with Areas')
plt.show()