import tkinter as tk
import cv2
from PIL import Image, ImageTk
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 8001
server_socket.bind(('localhost', port))
server_socket.listen(1)

def update():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        label.config(image=photo)
        label.image = photo
    window.after(10, update)

def send_message():
    message = entry.get()
    chat_text.config(state=tk.NORMAL)
    chat_text.insert(tk.END, "나: " + message + "\n")
    chat_text.config(state=tk.DISABLED)
    entry.delete(0, tk.END)

window = tk.Tk()
window.title("화상 채팅")
cap = cv2.VideoCapture(0)

label = tk.Label(window)
label.grid(row=0, column=0, padx=10, pady=10, rowspan=2, sticky="nsew")

chat_text = tk.Text(window, wrap=tk.WORD, state=tk.DISABLED)
chat_text.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

entry = tk.Entry(window)
entry.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

send_button = tk.Button(window, text="보내기", command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10, sticky="se")

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=4)  # 비디오 화면이 80% 차지
window.grid_columnconfigure(1, weight=1)  # 채팅 창이 20% 차지

update()
window.mainloop()
cap.release()