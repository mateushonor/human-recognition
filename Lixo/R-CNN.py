import cv2
import torch
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from threading import Thread
import time

# Carregar o modelo Faster R-CNN pré-treinado
model = fasterrcnn_resnet50_fpn(pretrained=True)
model.eval()  # Colocar o modelo em modo de avaliação

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
        last_time = time.time()
        while True:
            ret, frame = cap.read()
           

            # Processar somente um frame a cada 5 segundos
            current_time = time.time()
            if current_time - last_time < 5:
                continue  # Pula para o próximo loop sem processar o frame
            last_time = current_time

            # Converter frame para tensor
            frame_tensor = torch.from_numpy(frame).permute(2, 0, 1).float().unsqueeze(0)
            frame_tensor = frame_tensor / 255.0  # Normalizar para o intervalo [0, 1]

            # Processamento com Faster R-CNN
            results = model(frame_tensor)

            # Filtrar resultados para detecção de pessoas
            for result in zip(results[0]["boxes"], results[0]["labels"], results[0]["scores"]):
                box, label, score = result
                if label == 1 and score >= 0.5:  # Classe 'person' e confiança mínima
                    x1, y1, x2, y2 = map(int, box)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f'Person {score:.2f}', (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            cv2.imshow(f'VIDEO {camera_name}', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

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
