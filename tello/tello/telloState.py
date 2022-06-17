class TelloState():
    def __init__(self):
        self.roll  = 0
        self.pitch = 0
        self.yaw = 0
        self.v_x = 0
        self.v_y = 0
        self.v_z = 0
        self.a_x = 0.0
        self.a_y = 0.0
        self.a_z = 0.0
    def set(self, str):
        sw = str.split(";")
        self.roll = int(sw[1].split(":")[1])
        self.pitch = int(sw[0].split(":")[1])
        self.yaw = int(sw[2].split(":")[1])
        self.v_x = int(sw[3].split(":")[1])
        self.v_y = int(sw[4].split(":")[1])
        self.v_z = int(sw[5].split(":")[1])
        self.a_x = float(sw[13].split(":")[1])
        self.a_y = float(sw[14].split(":")[1])
        self.a_z = float(sw[15].split(":")[1])
    def show(self):
        print("roll: %d\r\npitch: %d\r\nyaw: %d\r\nv_x: %d\r\nv_y: %d\r\nv_z: %d\r\na_x: %d\r\na_y: %d\r\na_z: %d\r\n" % (self.roll, self.pitch, self.yaw, self.v_x, self.v_y, self.v_z, self.a_x, self.a_y, self.a_z))
