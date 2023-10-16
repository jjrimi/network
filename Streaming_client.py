import tkinter as tk
import threading
import cv2
import socket
import numpy as np
from PIL import Image, ImageTk

SERVER_IP = 'localhost'
SERVER_PORT = 8001

class VideoStreamThread(threading.Thread):
    def __init__(self, server_socket):
        super().__init__()
        self.server_socket = server_socket

    def run(self):
        cap = cv2.VideoCapture(0)  # 웹캠 캡처
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            _, img_encoded = cv2.imencode('.jpg', frame)
            img_bytes = img_encoded.tobytes()
            self.server_socket.sendall(img_bytes)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))
root = tk.Tk()
root.title("Video Streaming Client")
frame = tk.Label(root)
frame.pack()
def receive_video_stream(frame_label=None):
    while True:
        try:
            img_bytes = client_socket.recv(1024)
            img_encoded = np.frombuffer(img_bytes, dtype=np.uint8)
            frame = cv2.imdecode(img_encoded, cv2.IMREAD_COLOR)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            frame_label.config(image=photo)
            frame_label.image = photo
        except Exception as e:
            print(e)
            break

video_thread = threading.Thread(target=receive_video_stream)
video_thread.daemon = True
video_thread.start()

def send_message():
    message = entry.get()
    client_socket.sendall(message.encode())
    entry.delete(0, tk.END)

entry = tk.Entry(root, width=50)
entry.pack()
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack()
root.mainloop()
client_socket.close()