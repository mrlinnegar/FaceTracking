from imutils.video import VideoStream
from imutils.video import FPS
import unicornhathd
import imutils
import numpy as np
import cv2
import sys
import os
import math

import time

model = "res10_300x300_ssd_iter_140000.caffemodel"
prototxt = "deploy.prototxt.txt"

net = cv2.dnn.readNetFromCaffe(prototxt, model)
vs = VideoStream(src=0).start()

time.sleep(2.0)

try:
    print("Starting face tracking")

    while True:

        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300,300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
        net.setInput(blob)
        detections = net.forward()
        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence < 0.5:
                continue

            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            text = "{:.2f}%".format(confidence * 100)
            y = startY - 10 if startY - 10 > 10 else startY + 10
    #        cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)
    #        cv2.putText(frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
            print(text);
    #    cv2.imshow("Frame", frame)
    #    key = cv2.waitKey(1) & 0xFF

        #if key == ord("q"):
        #    break

    #cv2.destroyAllWindows()
    vs.stop()


except KeyboardInterrupt:
    unicornhathd.off()
    print("Face Tracking Ending")
