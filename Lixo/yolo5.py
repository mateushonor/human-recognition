import cv2
import torch
from threading import Thread
import time

# Carregar o modelo YOLOv5
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Definições das câmeras
cameras = {
    "Camera1": "rtsp://Honor:Mateus2449@192.168.100.158:554/onvif1",
    "Camera2": "rtsp://udne:en4t75@192.168.100.216:554/onvif2"
}

def process_camera(url, camera_name):
    cap = cv2.VideoCapture(url)
    
    if not cap.isOpened():
        print(f"Erro ao abrir a câmera {camera_name}")
        return
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Frame não foi recebido corretamente")
                break

            # Processamento com YOLOv5
            results = model(frame)

            # Filtrar resultados para detecção de pessoas
            results = results.xyxy[0]  # Coordenadas das detecções

            # Desenhar caixas delimitadoras para pessoas
            for *xyxy, conf, cls in results:
                if int(cls) == 0:  # Classe 'person'
                    x1, y1, x2, y2 = map(int, xyxy)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)
                    cv2.putText(frame, f'{model.names[int(cls)]} {conf:.2f}', (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)

            cv2.imshow(f'VIDEO {camera_name}', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            time.sleep(1/30)  # Controlar a taxa de quadros

    finally:
        cap.release()
        cv2.destroyAllWindows()

# Criar e iniciar threads para cada câmera
threads = []
for name, url in cameras.items():
    t = Thread(target=process_camera, args=(url, name))
    t.start()
    threads.append(t)

# Aguardar todas as threads terminarem
for t in threads:
    t.join()
