from MazeSolver3 import MazeSolver
from imutils.video import VideoStream
import argparse
import time

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())

print("[INFO] warming up camera...")
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)

# start the app
solver = MazeSolver(vs)
solver.root.mainloop()