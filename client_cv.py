# ## From https://stackoverflow.com/questions/30988033/sending-live-video-frame-over-network-in-python-opencv
# import socket
import numpy as np
from numpysocket import NumpySocket
import cv2
import time
import threading



npSocket = NumpySocket()

npSocket.startClient(9999)

thread_socket = NumpySocket()
thread_socket.startClient(9900)




host_ip = '192.168.1.134'
send_socket = NumpySocket()
send_socket.startServer(host_ip, 9001)



done = False
first_part = 'ata'
def thread_function(my_socket):
    global first_part
    while not done:
        
        first_part = my_socket.recieveNumpy()
        #print(first_part)
        

th = threading.Thread(target=thread_function, args=(thread_socket,))

# Read until video is completed

start = time.time()
fps = 0

th.start()

time.sleep(2)
while(True):
    
    # Capture frame-by-frame
    

    frame = npSocket.recieveNumpy()
    #print(frame.shape)
    
    #print(first_part.shape)
    frame = np.concatenate((frame, first_part), axis = 0)
    
    
    #print(frame.shape)

    send_socket.sendAck()
    cv2.imshow('Frame', frame)
    
    fps += 1
    #print(fps)
    # Press Q on keyboard to  exit
    #print(fps)
    if cv2.waitKey(2) & 0xFF == ord('q'):
        done = True
        break
    
print(frame.shape)
print(fps/(time.time() - start))

npSocket.endServer()
print("Closing")
