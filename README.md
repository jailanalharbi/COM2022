# COM2022

## Project title
Real Time Video Broadcasting protocol (RTVB) using UDP.\
Language used: Python


## Project description
Real Time Video Broadcasting is an accurate and efficient protocol designed to send video communication in a network. \
The protocol was designed to handle various actions such as the number of clients, video feeds from webcams and mp.4 video files, as well as the source of the video being streamed through a network. 


## Imports
`import socket`\
`import numpy as np`\
`import base64`



## MacOs
Run this command in the terminal.\
`sudo sysctl -w net.inet.udp.maxdgram=65535`


## Using webcam instead of mp4
1. Open server.py file
2. `vid = cv2.VideoCapture("cats.mp4")`
3. Replace `("cats.mp4")` with `(0)`


## How to run the code
1. Run the server.py file using this command in the terminal (python3 server.py)
2. Run the client.py file using this command in the terminal (python3 client.py)


## Testing with multiple clients
Run the client file multiple times (careful: there's a limit on the number of clients allowed)
 
## Testing on different machines
 In the client.py file, replace `(host_ip = '0.0.0.0')` with the IP address of the recieiving machine. 
 
