import sys
from datetime import datetime
import threading
import time
import cv2
import Database
from PIL import Image, ImageTk
import tkinter as tk


def popup():
    result = Database.inquiry()
    if result is not None:
        popupRoot = tk.Tk()
        tk.Label(popupRoot, text="Datums un laiks", font=('Mistral 18 bold')).pack()
        for i in result:
            dt = datetime.fromtimestamp(i[1]).strftime('%Y-%m-%d %H:%M:%S')
            tk.Label(popupRoot, text="{0}, {1}".format(i[0], dt), font=('Mistral 18 bold')).pack()
        popupRoot.mainloop()


def ok_popup(code):
    popupRoot = tk.Tk()
    tk.Label(popupRoot, text="Atrastais QR : {0}".format(code)).pack()
    tk.Button(popupRoot, text="OK!", font=("Verdana", 18), bg="yellow", command=popupRoot.destroy).pack()
    return popupRoot


def onClose():
    print("[INFO] closing...")
    stopEvent.set()
    cap.release()
    root.quit()
    sys.exit(0)


def video_loop():
    global panel
    try:
        while not stopEvent.is_set():
            _, frame = cap.read()
            frame = read_barcodes(frame)
            frame = cv2.flip(frame, 1)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("s"):
                onClose()
            if panel is None:
                panel = tk.Label(image=imgtk)
                panel.image = imgtk
                panel.pack(side="left", padx=10, pady=10)
            else:
                panel.configure(image=imgtk)
                panel.image = imgtk
    except RuntimeError as e:
        print("[INFO] caught a RuntimeError")


def read_barcodes(frame):
    data, points, _ = decoder.detectAndDecode(frame)
    if points is not None:
        points = points[0]
        for i in range(len(points)):
            pt1 = [int(val) for val in points[i]]
            pt2 = [int(val) for val in points[(i + 1) % 4]]
            cv2.line(frame, pt1, pt2, color=(255, 0, 0), thickness=3)
        print(data)
        if data != '' or "":
            Database.insert(data)
            ok = ok_popup(data)
            ok.mainloop()
    return frame


stopEvent = threading.Event()
panel = None
decoder = cv2.QRCodeDetector()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("SCANNER")
    root.config(background='black')
    panel = tk.Label(root)
    panel.grid(row=0, column=0)

    cap = cv2.VideoCapture(0)
    time.sleep(2.0)
    detector = cv2.QRCodeDetector()
    thread = threading.Thread(target=video_loop, args=())
    thread.start()
    # set a callback to handle when the window is closed
    root.wm_title("qr")
    root.wm_protocol("WM_DELETE_WINDOW", onClose)
    popupButton = tk.Button(root, text="Izvadīt esošos QR", font=("Verdana", 12), bg="yellow", command=popup)
    popupButton.grid(row=1, column=0)
    root.mainloop()

