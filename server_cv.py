from numpysocket import NumpySocket
import cv2
import time
import threading


print('ata')
#host_ip = '192.168.1.143'  # change me

#host_ip = '172.27.3.3'
host_ip = '192.168.1.143'

cap = cv2.VideoCapture(0)
npSocket = NumpySocket()
npSocket.startServer(host_ip, 9999)

time.sleep(2)

thread_socket = NumpySocket()
thread_socket.startServer(host_ip, 9900)



recieve_socket = NumpySocket()
recieve_socket.startClient(9001)




def thread_function(my_socket, data):
    
     my_socket.sendNumpy(data)





# Read until video is completed
n_frame = 0
while(cap.isOpened()):
    #print('h')
    ret, frame = cap.read()
    #print(frame, ret)
    #ref_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_resize = frame[::2, ::2]
    n_frame +=1
    npSocket.sendNumpy(frame_resize[:120])
    th = threading.Thread(target=thread_function, args=(thread_socket, frame_resize[120:], ))
    th.start()
    recieve_socket.recieveAck()
        
# When everything done, release the video capture object
npSocket.endServer()
cap.release()

