import cv2
from ultralytics import YOLO
import os
import math

# Modelo YOLO
model = YOLO("yolo-Weights/yolov8n.pt")

# Credenciais e endereço da câmera IP
USERNAME = 'Honor'
PASSWORD = 'Mateus2449'
IP = '192.168.100.158'
PORT = '554'
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
URL = f'rtsp://{USERNAME}:{PASSWORD}@{IP}:{PORT}/onvif1'

# Inicializa a captura de vídeo
cap = cv2.VideoCapture(URL, cv2.CAP_FFMPEG)
if not cap.isOpened():
    print("Erro ao abrir o fluxo de vídeo")
    exit()

# Inicializa o detector HOG para detecção de pedestres
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

while True:
    ret, frame = cap.read()
    if not ret:
        print("Falha ao recuperar frame")
        continue

    # Processamento inicial com HOG
    (rects, weights) = hog.detectMultiScale(frame, winStride=(4, 4), padding=(8, 8), scale=1.05)

    for (x_hog, y_hog, w_hog, h_hog) in rects:
        roi = frame[y_hog:y_hog + h_hog, x_hog:x_hog + w_hog]
        results = model(roi, stream=True)  # Processamento com YOLO na ROI

        for r in results:
            boxes = r.boxes
            for box in boxes:
                cls = int(box.cls[0])  # Classe detectada
                # Ajusta as coordenadas para o frame original
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                x1 += x_hog
                y1 += y_hog
                x2 += x_hog
                y2 += y_hog
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                confidence = math.ceil((box.conf[0] * 100)) / 100
                org = (x1, y1)
                cv2.putText(frame, f'{confidence}', org, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Exibe o frame resultante
    cv2.imshow('VIDEO', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberação dos recursos
cap.release()
cv2.destroyAllWindows()
