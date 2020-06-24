#(lng,lat)
import time
import math

################################ Automatic ##########################################################

class Controls:
    def __init__(self):
        self.reset()

    def set_home(self, h_coord):
        self.home = h_coord

    def set_prev(self, p_coord):
        self.prev_location = p_coord

    def set_info(self, tar, c_coord):
        self.set_home(c_coord)
        self.set_prev(c_coord)
        for t in tar:
            self.targets.append(t)
    
    def reset(self):
        self.targets = []
        self.home = ()
        self.prev_location = ()

    #prev_location[-1] aka Current_location, targets[0]

    #prev_location[-1] aka Current_location, prev_location[-2]

    #0->North
    #90->East
    #180->South
    #270->West

    def _facing_direction(self, coord1, coord2):
        result = 0
        degree_lng = math.radians(coord2[0]-coord1[0])
        lat1 = math.radians(coord1[1])
        lat2 = math.radians(coord2[1])
        angle1 = math.sin(degree_lng) * math.cos(lat2)
        angle2 = math.sin(lat1) * math.cos(lat2) * math.cos(degree_lng)
        angle2 = math.cos(lat1) * math.sin(lat2) - angle2
        angle2 = math.atan2(angle1, angle2)
        if (angle2 < 0.0):
            angle2 += 2*math.pi
        result = math.degrees(angle2)
        return result;

    #compare facing_direction(prev_location[-1], targets[0]), facing_direction(prev_location[-1], prev_location[-2]) with
    #neg degree = counterclockwise
    #pos degree = clockwise

    def desired_direction(self, c_coord):
        result = 0
        deg1 = 0
        deg2 = 0
        if len(self.targets) != 0:
            deg1 = self._facing_direction(c_coord, self.targets[0])
            deg2 = self._facing_direction(self.prev_location, c_coord)
        else:
            deg1 = self._facing_direction(c_coord, self.home)
            deg2 = self._facing_direction(self.prev_location, c_coord)
        result = deg2-deg1
        return result;

    def _distance(self, coord1, coord2):
        result = 0
        lng_angle = math.radians(coord1[0]-coord2[0])
        sin_deg_lng = math.sin(lng_angle)
        cos_deg_lng = math.cos(lng_angle)
        lat1 = math.radians(coord1[1])
        lat2 = math.radians(coord2[1])
        sin_lat1 = math.sin(lat1)
        cos_lat1 = math.cos(lat1)
        sin_lat2 = math.sin(lat2)
        cos_lat2 = math.cos(lat2)
        lng_angle = (cos_lat1 * sin_lat2) - (sin_lat1 * cos_lat2 * cos_deg_lng)
        lng_angle = math.pow(lng_angle, 2)
        lng_angle += math.pow(cos_lat2 * sin_deg_lng, 2)
        lng_angle = math.sqrt(lng_angle)
        denom = (sin_lat1 * sin_lat2) + (cos_lat1 * cos_lat2 * cos_deg_lng)
        lng_angle = math.atan2(lng_angle, denom)
        result = lng_angle * 6372795
        return result;

    def desired_distance(self, c_coord):
        result = 0
        if len(self.targets) != 0:
            result = self._distance(c_coord, self.targets[0])
        else:
            result = self._distance(c_coord, self.home)
        return result;

    '''def desired_path(self, c_coord):
        result = [0,0]
        result[0] = self.desired_direction(c_coord)
        result[1] = self.desired_distance(c_coord)
        self.set_prev(c_coord)
        return result;'''

class Automatic_Values: # all values come from arduino/gui
    def __init__(self, throttle, yaw, pitch, roll, targets, coord):
        self.controls = Controls()
        self.controls.set_info(targets, coord)
        self.throttle = throttle
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll
        self.speed = 50 #50 m/sec could change later if needed

    def foward_backwards(self, pitch, c_coord):
        dis = controls.desired_distance(c_coord)
        time = dis/self.speed
        while time != 0:
            self.pitch = pitch #positive = foward, negative = backwards
            time = time - 1
        self.pitch = 0 #idle value

    def up_down(self, throttle, dis): #if needed
        time = dis/self.speed
        while time != 0:
            self.throttle = throttle #positive = up, negative = down
            time = time - 1
        self.throttle = 0 #idle value

    def rotate_left_right(self, yaw, c_coord):
        rot = controls.desired_direction(c_coord)
        time = rot/self.speed
        while time != 0:
            self.yaw = yaw #positive = right rotation, negative = left rotation
            time = time - 1
        self.yaw = 0 #idle value

    def move_left_right(self, roll, c_coord):
        dis = controls.desired_distance(c_coord)
        time = dis/self.speed
        while time != 0:
            self.roll = roll #positive = move right, negative = move left
            time = time - 1
        self.roll = 0 #idle value

################################ Manual ##########################################################
    
class Manual_Values: # all values come from arduino/gui
    def __init__(self, throttle, yaw, pitch, roll):
        self.throttle = throttle
        self.yaw = yaw
        self.pitch = pitch
        self.roll = roll

    def foward_backwards(self, pitch):
        self.pitch = pitch #positive = foward, negative = backwards

    def up_down(self, throttle):
        self.throttle = throttle #positive = up, negative = down

    def rotate_left_right(self, yaw):
        self.yaw = yaw #positive = right rotation, negative = left rotation

    def move_left_right(self, roll):
        self.roll = roll #positive = move right, negative = move left
