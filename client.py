import cv2, imutils, socket
import numpy as np
import time
import base64
from lib2to3.pgen2.token import EQUAL


BUFF_SIZE = 65536


client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client_socket.settimeout(5)


client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
host_name = socket.gethostname()
host_ip = '0.0.0.0' # socket.gethostbyname(host_name) or replace '0.0.0.0' with recieiving machine's IP address. 
print(host_ip)
port = 9995
RTT_list = []


def Average(lst):
    return sum(lst) / len(lst)
  
# Driver Code
lst = [15, 9, 55, 41, 35, 20, 62, 49]
average = Average(lst)


def recieve_video():
    fps,st,frames_to_count,cnt = (0,0,20,0)
    while True:
            initial_time = time.time()
            sent = 'RTT::Jailan'
            client_socket.sendto(base64.b64encode(sent.encode('ascii')),(host_ip,port))
            print('waiting to receive')

            packet,_ = client_socket.recvfrom(BUFF_SIZE)
            ending_time = time.time()
       

            elasped_time = ending_time - initial_time
            print("The time is " + str(elasped_time))

            RTT_list.append(elasped_time)
            data = base64.b64decode(packet,' /').decode('ascii')
            recv_msg = data.split('::')
            npdata = np.fromstring(recv_msg[1],dtype=np.uint8, sep=' ')
            frame = cv2.imdecode(npdata,1)
            frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
            cv2.imshow("RECEIVING VIDEO",frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('Q'):
                message = 'QUIT::Jailan'

                client_socket.sendto(base64.b64encode(message.encode('ascii')),(host_ip,port))
                client_socket.close()
                break
            if cnt == frames_to_count:
                try:
                    fps = round(frames_to_count/(time.time()-st))
                    st=time.time()
                    cnt=0
                except:
                    pass
            cnt+=1

try:
    message = 'LOGIN::Jailan::1234'

    client_socket.sendto(base64.b64encode(message.encode('ascii')),(host_ip,port))
    packet,_ = client_socket.recvfrom(BUFF_SIZE)
    data = base64.b64decode(packet,' /').decode('ascii')
    recv_msg = data.split('::')
    print(recv_msg)
    
    if recv_msg[0]== 'MESSAGE':

        if recv_msg[1] =='AUTHORIZE':
            recieve_video()
        elif recv_msg[1] == 'UNAUTHORIZE':
            print('Incorrect username or password')
        elif recv_msg[1] ==  'FULL':
            print('The server is full')
        elif recv_msg[1] == 'EXIST':
            print('User is already logged in') 
    elif recv_msg[0] == 'FINISH':
        print('Broadcasting is over ')
        exit()
except socket.error as e:
    print(e)
    

if len(RTT_list) != 0 :
     max_RTT = max(RTT_list)
     min_RTT = min(RTT_list)
     avg_RTT = Average(RTT_list)
     print('MAX RTT:'+str(max_RTT))
     print('MIN RTT:'+str(min_RTT))
     print('AVG RTT:'+str(avg_RTT))
else:
     print('Timeout since the first request')



# close the socket
print('closing socket')
client_socket.close
