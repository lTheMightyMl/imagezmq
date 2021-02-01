from imutils.video import VideoStream
import numpy as np
import imagezmq
import argparse
import socket
import time
import cv2
import threading

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()

# ip = '192.168.1.143'
ip = 'localhost'
print('d')
sender = imagezmq.ImageSender(connect_to="tcp://{}:5555".format(ip))
thread_sender = imagezmq.ImageSender(connect_to="tcp://{}:5556".format(ip))

thread_frame = frame = None

rpiName = socket.gethostname()
# vs = VideoStream(usePiCamera=True).start()
# vs = VideoStream(src=0).start()
cap = cv2.VideoCapture(0)
time.sleep(2.0)
i = 0


# cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(1024))
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(768))


def thread_send():
    global thread_sender, rpiName, thread_frame
    thread_sender.send_image(rpiName, thread_frame)


while True:
    # read the frame from the camera and send it to the server
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    thread_frame, frame = np.array_split(frame, 2)


    # i+=1
    th = threading.Thread(target=thread_send)
    th.start()
    sender.send_image(rpiName, frame)
    th.join()
    # print(i)
