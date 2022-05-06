from __future__ import print_function
from PIL import Image
from PIL import ImageTk
import tkinter as tki
import threading
import cv2
import time

class Point(object):
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

	def __add__(self, other):
		return Point(self.x + other.x, self.y + other.y)

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

class MazeSolver:

	def __init__(self, vs):
		self.vs = vs
		self.frame = None
		self.thread = None
		self.stopEvent = None
		self.solving = False
		self.mouse_click_status = 0
		self.start = None
		self.end = None
		self.searchthread = None

		self.root = tki.Tk()
		#self.root.geometry("800x480")
		self.root.configure(background='black')
		self.panel = None

		self.btn = tki.Button(self.root, text="Save Image",
			command=self.takeSnapshot)
		self.btn.pack(side="bottom", fill="both", expand="yes", padx=10,
			pady=10)

		# starting the video thread
		self.stopEvent = threading.Event()
		self.videothread = threading.Thread(target=self.videoLoop, args=())
		self.videothread.daemon = True
		self.videothread.start()
		# set a callback to handle when the window is closed
		self.root.wm_title("Maze Solver")
		self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

	

	def bfs(self):
		print("starting bfs")
		s = self.start
		e = self.end
		h, w = self.frame.shape[:2]
 


		# directions of surrounding nodes for BFS
		directions = [Point(0, -1), Point(0, 1), Point(1, 0), Point(-1, 0)]

		found = False

		# queue to perform BFS
		queue = []

		# visited matrix of size width*height of the image with each element = 0
		visited = [[0 for j in range(w)] for i in range(h)]

		# parent matrix of size width*height of the image with each element = empty Point object
		parent = [[Point() for j in range(w)] for i in range(h)]

		# storing starting Point and marking it 1 in visited matrix
		queue.append(s)
		visited[s.y][s.x] = 1

		# looping until queue is not empty
		while len(queue) > 0:
			# popping one element from queue and storing in p
			p = queue.pop(0)

			# surrounding elements
			for d in directions:
				cell = p + d

				# if cell(a surrounding pixel) is in range of image, not visited, !(B==0 && G==0 && R==0) i.e. pixel is
				# not black as black represents border
				if (0 <= cell.x < w and 0 <= cell.y < h and visited[cell.y][cell.x] == 0 and (self.frame[cell.y][cell.x][0] != 0 or self.frame[cell.y][cell.x][1] != 0 or self.frame[cell.y][cell.x][2] != 0)):

					queue.append(cell)

					# marking cell as visited
					visited[cell.y][cell.x] = 1
					# changing the pixel color to purple
					self.frame[cell.y][cell.x] = [255, 0, 255]

					# string the value of p in parent matrix to trace path
					parent[cell.y][cell.x] = p

					# if end is found break
					if cell == e:
						found = True
						del queue[:]
						break

		# list to trace path
		path = []
		if found:
			print("solved!")
			p = e
			while p != s:
				path.append(p)
				p = parent[p.y][p.x]

			path.append(p)
			path.reverse()

			# changing the pixel of resulting path to green
			for p in path:
				self.frame[p.y][p.x] = [0, 255, 0]
		return

	def videoLoop(self):
		try:
			# keep looping over frames until we are instructed to stop
			while not self.stopEvent.is_set():
				if not self.solving:
					self.frame = self.vs.read()
					self.frame = cv2.resize(self.frame, (800, 480), interpolation=cv2.INTER_NEAREST)
				image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
				image = Image.fromarray(self.frame)
				image = ImageTk.PhotoImage(image)
				
				if self.panel is None:
					self.panel = tki.Label(image=image)
					self.panel.configure(background='black')
					self.panel.image = image
					self.panel.pack(side="left", padx=10, pady=10)

				else:
					self.panel.configure(image=image)
					self.panel.image = image
				time.sleep(0.1)
		except (RuntimeError):
			print("[INFO] caught a RuntimeError")

	def mouse_click(self, event):

		if self.mouse_click_status == 0:
			cv2.rectangle(self.frame, (event.x-4, event.y-4), (event.x+4, event.y+4), (0, 0, 255), -1)
			self.start = Point(event.x, event.y)
			# change status to 1
			self.mouse_click_status = self.mouse_click_status + 1

		# second click
		elif self.mouse_click_status == 1:
			cv2.rectangle(self.frame, (event.x-4, event.y-4), (event.x+4, event.y+4), (255, 0, 0), -1)
			self.end = Point(event.x, event.y)
			# change status to 2
			self.mouse_click_status = self.mouse_click_status + 1
			self.panel.unbind('<Button-1>')
			self.searchthread = threading.Thread(target=self.bfs, args=())
			#self.searchthread.daemon = True
			self.searchthread.start()
			

	def takeSnapshot(self):
		# temporarily rebind the button to switch back to video stream
		self.btn.configure(text="Cancel", command=self.stopsolving)
		self.solving = True
		self.panel.bind('<Button-1>', self.mouse_click)
		self.frame = cv2.cvtColor(self.frame, cv2.COLOR_RGB2GRAY)
		_, self.frame = cv2.threshold(self.frame, 120, 255, cv2.THRESH_TOZERO)
    	# img object, threshold value, color of threshold, thresh_tozero to darken blacks without affecting lighter pixels
		self.frame = cv2.cvtColor(self.frame, cv2.COLOR_GRAY2BGR)
	
	def stopsolving(self):
		self.btn.configure(text="Snapshot!", command=self.takeSnapshot)
		self.solving = False
		self.mouse_click_status = 0

	def onClose(self):
		print("[INFO] closing...")
		self.stopEvent.set()
		self.vs.stop()
		self.root.quit()

