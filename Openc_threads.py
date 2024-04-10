import cv2
from ultralytics import YOLO
import threading
import time

# Carregar o modelo YOLO
model = YOLO("yolo-Weights/yolov8n.pt")

# Inicializa o detector HOG
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Definições das câmeras
cameras = {
    "Camera1": "rtsp://Honor:Mateus2449@192.168.100.158:554/onvif1",
    "Camera2": "rtsp://udne:en4t75@192.168.100.216:554/onvif2"
}

def process_camera(url, camera_name):
    cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)
    
    if not cap.isOpened():
        print(f"Erro ao abrir a câmera {camera_name}")
        return
    
    try:
        while True:
            start_time = time.time()

            ret, frame = cap.read()
            if not ret:
                print("Frame não foi recebido corretamente")
                break

            # Detecção preliminar usando HOG
            (rects, weights) = hog.detectMultiScale(frame, winStride=(4, 4), padding=(8, 8), scale=1.05)

            # Processamento com YOLO apenas se HOG detectar uma pessoa
            if len(rects) > 0:
                results = model(frame, stream=True)

                for r in results:
                    boxes = r.boxes
                    for box in boxes:
                        if int(box.cls[0]) == 0:  # Verifica se a classe detectada é 'person'
                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

            cv2.imshow(f'VIDEO {camera_name}', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            time.sleep(max(1.0 / 30 - (time.time() - start_time), 0))  # Taxa de 30 FPS

    finally:
        cap.release()
        cv2.destroyAllWindows()

threads = []
for name, url in cameras.items():
    t = threading.Thread(target=process_camera, args=(url, name))
    t.start()
    threads.append(t)

# Aguardar todas as threads terminarem
for t in threads:
    t.join()
