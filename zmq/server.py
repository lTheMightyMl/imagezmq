import numpy as np
import imagezmq

import imutils
import cv2
import time
import threading

# initialize the ImageHub object
imageHub = imagezmq.ImageHub()
thread_imageHub = imagezmq.ImageHub(open_port='tcp://*:5556')

thread_frame = None


def thread_recv():
    global rpiName, thread_frame
    (rpiName, thread_frame) = thread_imageHub.recv_image()
    thread_imageHub.send_reply(b'OK')


print('here')

# start looping over all the frames
time.sleep(10)
start = time.time()
num_of_frames = 0

while True:
    # receive RPi name and frame from the RPi and acknowledge
    # the receipt
    th = threading.Thread(target=thread_recv)
    th.start()
    (rpiName, frame) = imageHub.recv_image()
    # print(time.time() - start)
    # print(frame.shape)
    imageHub.send_reply(b'OK')
    th.join()

    # frame = imutils.resize(frame, width=400)
    num_of_frames += 1


    cv2.imshow('frame', np.vstack((thread_frame, frame)))
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# do a bit of cleanup


fps = num_of_frames / (time.time() - start)
print("fps is: ")
print(fps)
cv2.destroyAllWindows()
