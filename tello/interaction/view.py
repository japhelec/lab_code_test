import cv2
from threading import Thread


class View:
    def __init__(self, drone):
        self.drone = drone

        self.thread = Thread(target=self._stream_thread)
        self.thread.daemon = True
        self.thread.start()  


    def _stream_thread(self):
        while True:
            frame = self.drone.read()
            if frame is None or frame.size == 0:
                continue 
            cv2.imshow("frame",frame)
            cv2.waitKey(1)
        cv2.destroyAllWindows()