# import the necessary packages
from __future__ import print_function
import Database
from PIL import Image
from PIL import ImageTk
import tkinter as tki
from tkinter import ttk
from tkinter.messagebox import showinfo
import threading
import datetime
import imutils
import cv2
import os
from pyzbar import pyzbar


class QRDetector:
    def _init(self, vs):
        # store the video stream object and output path, then initialize
        # the most recently read frame, thread for reading frames, and
        # the thread stop event
        self.found = set()
        self.vs = vs
        self.frame = None
        self.thread = None
        self.stopEvent = None
        # initialize the root window and image panel
        self.root = tki.Tk()
        self.panel = None
        # start a thread that constantly pools the video sensor for
        # the most recently read frame
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()
        # set a callback to handle when the window is closed
        self.root.wm_title("qr")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

        def onClose(self):
                # set the stop event, cleanup the camera, and allow the rest of
                # the quit process to continue
                print("[INFO] closing...")
                self.stopEvent.set()
                self.vs.stop()
                self.root.quit()

        def open_popup(code):
                top = tki.Toplevel(self.root)
                top.geometry("750x250")
                top.title("Barcode exists!")
                tki.Label(top, text="Item already exists, continue?", font=('Mistral 18 bold')).place(x=150, y=80)
                B1 = ttk.Button(top, text="Register!", command=Database.insert(code) and top.destroy())
                B1.pack()


        def videoLoop(self):
                try:
                 # keep looping over frames until we are instructed to stop
                    while not self.stopEvent.is_set():
                    # grab the frame from the video stream and resize it to
                    # have a maximum width of 300 pixels
                        self.frame = self.vs.read()
                        self.frame = imutils.resize(self.frame, width=300)
                    # OpenCV represents images in BGR order; however PIL
                    # represents images in RGB order, so we need to swap
                    # the channels, then convert to PIL and ImageTk format
                        image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                        image = Image.fromarray(image)
                        image = ImageTk.PhotoImage(image)
                     # Extract barcode if found
                        barcodes = pyzbar.decode(image)
                        for barcode in barcodes:
                            (x, y, w, h) = barcode.rect
                            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                            barcode_data = barcode.data.decode("utf-8")
                            if barcode_data not in self.found:
                                self.found.add(barcode_data)
                                Database.insert(barcode_data)
                            else:
                                open_popup(barcode_data)

                        key = cv2.waitKey(1) & 0xFF
                        if key == ord("s"):
                            onClose(self)

                        # if the panel is not None, we need to initialize it
                        if self.panel is None:
                            self.panel = tki.Label(image=image)
                            self.panel.image = image
                            self.panel.pack(side="left", padx=10, pady=10)
                        # otherwise, simply update the panel
                        else:
                            self.panel.configure(image=image)
                            self.panel.image = image

                except RuntimeError as e:
                    print("[INFO] caught a RuntimeError")
