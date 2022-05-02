# This code is for the server 
# Lets import the libraries
import cv2, socket, pickle, struct, imutils

def read_camera():
    
    #cascade_src = 'cascade.xml'
    #model_cascade = cv2.CascadeClassifier(cascade_src)

    # Socket Create
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host_name  = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    #print('HOST IP:',host_ip)
    port = 9999
    socket_address = (("0.0.0.0", 9997))

    # Socket Bind
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server_socket.bind(socket_address)

    # Socket Listen
    server_socket.listen(5)
    print("LISTENING AT:",socket_address)

    # Socket Accept
    while True:
        client_socket,addr = server_socket.accept()
        print('GOT CONNECTION FROM:',addr)
        if client_socket:
            vid = cv2.VideoCapture(0)
            
            while(vid.isOpened()):
                img,frame = vid.read()
                #gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                #model = model_cascade.detectMultiScale(gray,1.1,1)
                #for (x,y,w,h) in model:
                 #   cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)

                frame = imutils.resize(frame,width=640)
                a = pickle.dumps(frame)
                message = struct.pack("Q",len(a))+a
                client_socket.sendall(message)
                #cv2.imshow('TRANSMITTING VIDEO',frame)
                key = cv2.waitKey(1) & 0xFF
                if key ==ord('q'):
                    client_socket.close()

#read_camera()

