#(lng,lat)
from staticmap import StaticMap, Line, CircleMarker
import time
import math

class Mapping:
    def __init__(self):
        self.reset()

    def set_home(self, h_coord):
        self.home = h_coord

    def set_start(self, s_coord):
        self.start = s_coord

    def set_info(self, tar, c_coord): # sets the gives info
        self.set_home(c_coord)
        self.set_start(c_coord)
        self.prev_location.append(c_coord)
        for t in tar:
            self.targets.append(t) #edit t depending on how the gui stores the values

    def set_zoom(self, zoom):
        self.zoom = zoom

    def reset(self):
        self.start = ()
        self.targets = []
        self.home = ()
        self.zoom = 20
        self.prev_location = []

    def display_start_map(self): # Not Using
        m = StaticMap(1200, 950)

        marker_outline = CircleMarker(self.start, 'white', 18)
        marker = CircleMarker(self.start, '#0036FF', 12)

        m.add_marker(marker_outline)
        m.add_marker(marker)

        image = m.render(zoom=self.zoom)
        image.save(r'GMap\start_map.png')

    
    def find_drone_path(self): # desired path of drone
        m = StaticMap(1200, 950)

        marker_outline = CircleMarker(self.start, 'white', 18)
        marker = CircleMarker(self.start, '#0036FF', 12)

        m.add_marker(marker_outline)
        m.add_marker(marker)

        for t in self.targets:
            target_marker_outline = CircleMarker(t, 'white', 18)
            target_marker = CircleMarker(t, 'red', 12)

            m.add_marker(target_marker_outline)
            m.add_marker(target_marker)
            
        path = []
        path.append(self.start)
        for t in self.targets:
            path.append(t)
        
        m.add_line(Line(path, 'blue', 3))
    
        image = m.render(zoom=self.zoom)
        image.save(r'GMap\drone_path.png')

    def track_drone(self, current_location): # drone's path
        if self.prev_location[-1] != current_location:
            m = StaticMap(1200, 950)

            tar = self.targets
    
            self.prev_location.append(current_location)

            marker_outline = CircleMarker(current_location, 'white', 18)
            marker = CircleMarker(current_location, '#0036FF', 12)

            m.add_marker(marker_outline)
            m.add_marker(marker)

            for t in self.targets:
                if(current_location!=t):
                    target_marker_outline = CircleMarker(t, 'white', 18)
                    target_marker = CircleMarker(t, 'red', 12)
                else:
                    target_marker_outline = CircleMarker(t, 'white', 18)
                    target_marker = CircleMarker(t, 'green', 12)
                    tar.remove(t)

                m.add_marker(target_marker_outline)
                m.add_marker(target_marker)

            self.targets = tar
            path = []
            path.append(self.start)
            for p in self.prev_location:
                 path.append(p)
    
            m.add_line(Line(path, 'green', 3))
        
            image = m.render(zoom=self.zoom)
            image.save(r'GMap\drone_path.png')

    def GUIpath(self, tar, coord):
        self.set_info(tar, coord)
        self.display_start_map()
        self.find_drone_path()

if __name__ == '__main__':
    target_list =[]

    s = (-117.8194082, 33.6481343)

    UHS = [-117.8227978, 33.6513922]

    Albertsons = [-117.8315102, 33.6501168]

    CUI = [-117.8087492, 33.6536018]

    target_list.append((UHS[0],UHS[1]))
    target_list.append((Albertsons[0],Albertsons[1]))
    target_list.append((CUI[0],CUI[1]))

    mapping = Mapping()

    mapping.GUIpath(target_list, s)

    prev = [(-117.8194082, 33.6481343),
            (-117.820453, 33.648328),
            (-117.821249, 33.648509),
            (-117.821633, 33.649247),
            (-117.821861, 33.650053),
            (-117.821800, 33.650622),
            (-117.8227978, 33.6513922),
            (-117.824379, 33.650235),
            (-117.826139, 33.649842),
            (-117.828371, 33.649360),
            (-117.830549, 33.649458),
            (-117.8315102, 33.6501168),
            (-117.831085, 33.648761),
            (-117.829411, 33.649145),
            (-117.827142, 33.649612),
            (-117.825079, 33.650067),
            (-117.821560, 33.650835),
            (-117.819472, 33.650813),
            (-117.817895, 33.651233),
            (-117.815717, 33.651680),
            (-117.814206, 33.652299),
            (-117.811867, 33.652969),
            (-117.810065, 33.653505),
            (-117.8087492, 33.6536018),
            (-117.811653, 33.652121),
            (-117.813327, 33.651219),
            (-117.815024, 33.650330),
            (-117.816279, 33.649687),
            (-117.817266, 33.649169),
            (-117.818607, 33.648669),
            (-117.8194082, 33.6481343)]

    for p in prev:
        mapping.track_drone(p)
        time.sleep(0.1)
        
    mapping.reset()
