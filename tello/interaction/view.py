import cv2
from threading import Thread


class View:
    def __init__(self, drone):
        self.toSave = False
        self.drone = drone

        self.thread = Thread(target=self._stream_thread)
        self.thread.daemon = True
        self.thread.start()  


    def _stream_thread(self):
        while True:
            frame = self.drone.read()
            if frame is None or frame.size == 0:
                # add black frame
                continue 
            cv2.imshow("frame",frame)
            cv2.waitKey(1)
        cv2.destroyAllWindows()


    def set_save_mode(self, mode):
        self.toSave = mode