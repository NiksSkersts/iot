from imutils.video import VideoStream
from pyzbar import pyzbar
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import datetime
import imutils
import time
import cv2


def detect():
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output", type=str, default="barcodes.csv")
    args = vars(ap.parse_args())
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    found = set()

    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=1080)
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            barcode_data = barcode.data.decode("utf-8")
            if barcode_data not in found:
                found.add(barcode_data)
        cv2.imshow("Barcode Reader", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("s"):
            break
    cv2.destroyAllWindows()
    vs.stop()
    return found
