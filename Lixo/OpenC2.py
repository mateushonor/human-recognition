import cv2
from ultralytics import YOLO
import os
import math

# model
model = YOLO("yolo-Weights/yolov8n.pt")

# object classes
classNames = ["person"]  # Supondo que 'person' é índice 0

USERNAME = 'udne'
PASSWORD = 'en4t75'
IP = '192.168.100.216'
PORT = '554'

os.environ["OPENCV_FFMPEG_CAPTURE_OPTION"] = "rtsp_transport;udp"

URL = f'rtsp://{USERNAME}:{PASSWORD}@{IP}:{PORT}/onvif1'

cap = cv2.VideoCapture(URL, cv2.CAP_FFMPEG)

while True:
    ret, frame = cap.read()
    
    results = model(frame, stream=True)

    for r in results:
        boxes = r.boxes
        for box in boxes:
            # class name
            cls = int(box.cls[0])
            
            # Verifica se a classe detectada é 'person'
            if cls == 0:  # 0 é o índice para 'person' em classNames
                # bounding box
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # desenha o retângulo no frame
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

                # confiança
                confidence = math.ceil((box.conf[0] * 100)) / 100
                print("Confidence --->", confidence)

                # Detalhes do objeto
                org = (x1, y1)
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                color = (255, 0, 0)
                thickness = 2
                cv2.putText(frame, f'{classNames[cls]} {confidence}', org, font, fontScale, color, thickness)
    
    # Exibe o frame resultante
    cv2.imshow('VIDEO', frame)
    
    # Pressione 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera o objeto de captura e fecha as janelas
cap.release()
cv2.destroyAllWindows()