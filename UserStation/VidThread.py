# lets make the client code
import cv2, socket, pickle, struct
import socket
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap

class VidThread(QThread):

	def __init__(self,parent=None):
		self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.host_ip = '127.0.0.1' # paste your server ip address here
		self.port = 9999
		#self.client_socket.connect((self.host_ip,self.port)) # a tuple
		self.data = b""
		self.payload_size = struct.calcsize("Q")
		self.client_socket.connect((self.host_ip,self.port)) # a tuple

		Signal = pyqtSignal(QPixmap)

		QThread.__init__(self)

# create socket
	def run(self):
		
		while True:
			while len(self.data) < self.payload_size:
				self.packet = self.client_socket.recv(4*1024) # 4K
				if not self.packet: break
				self.data+=self.packet
			self.packed_msg_size = self.data[:self.payload_size]
			self.data = self.data[self.payload_size:]
			self.msg_size = struct.unpack("Q",self.packed_msg_size)[0]
	
			while len(data) < self.msg_size:
				self.data += self.client_socket.recv(4*1024)
			self.frame_data = self.data[:msg_size]
			self.data  = self.data[msg_size:]
			self.frame = pickle.loads(self.frame_data)
			cv2.imshow("RECEIVING VIDEO",self.frame)
			self.key = cv2.waitKey(1) & 0xFF
			if self.key  == ord('q'):
				break
		self.client_socket.close()


#MyVideo = VidThread()

#MyVideo.start()