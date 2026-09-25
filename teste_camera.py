import cv2

print("Procurando câmera...")

camera = None

# Tenta diferentes índices e formas de acesso
for indice in range(4):
    print(f"Tentando câmera {indice}...")

    cap = cv2.VideoCapture(indice)

    if cap.isOpened():
        camera = cap
        print(f"Câmera encontrada no índice {indice}!")
        break

    cap.release()

if camera is None:
    print("\nERRO: nenhuma câmera foi encontrada.")
    print("Verifique se a câmera está conectada e disponível no Windows.")
    exit()

print("Câmera funcionando!")
print("Pressione Q para fechar.")

while True:
    ret, frame = camera.read()

    if not ret:
        print("Não foi possível capturar a imagem.")
        break

    cv2.imshow("Teste da Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()