#Chuck's Rush Hour Game

#It's rush hour!
#Connect those dots!
#Get the passenengers to
#their destination!
#ASAP!

#Controls:
#Clink on a station and then click on a new station to create a line
#Double click on a line to delete the line
#Click the icons on the upper-right side to change game speed
#Click the icons on the lower-right side to change line selection
#The passenger will get on the train and disappear when they arrive at their destination

# Game Pitch Sheet: https://dl.dropbox.com/s/lzxz96254mmlfu9/Rush%20Hour%20-%20Chuck%20Wang.pdf?dl=0

#Developing note

# in line station connect: on
# transparent line: roll back point : version 33


#Phase one: basic framework
#			  in this phase, I will build a metro system with
#             three stations that works on themselves
#Phase 1 ends at Version 15 of user43_YOieCoiga0

#Phase two: visual effects
#			in this phase, I will make the link look like metro map
#    		and all the trains turn at each station
#Phase 2 ends at Version 0 of user43_rZkLD0LkLW

#Phase three: mouse click system
#			in this phase, I will build a line creation system and a tracking system 
#			that allows me to modify line with mouth drag
#Phase 3 ends ar Version 20 of user43_rZkLD0LkLW

#Phase four: menu, level and tutorial
#			in this phase, I will build three level with different difficulty
#			a user interface, and a tutorial
#Phase 4 ends ar Version 35 of user43_rZkLD0LkLW


import simplegui
import random
import math

#--------------------------Global
STATION_TYPE = ["Circle", "Square", "Triangle"]
COLORS = ["Red", "Blue", "Green", "Yellow", "Orange"]
SPEED = 2

score = 0
game_over_message = ""
tutorial_message = ""
station_station_click = []
line_click = []
station_spawn_list = []
station_spawn_timer = 0
temporary_timer = 0
tutorial_step = 0
screen = "Menu"
start = False
tutorial = True
double_speed = False
line_selection = "Red"

station_spawn_interval = 60
spawn_interval = 240
crowded_limit = 600

#--------------------Helper Functions

def draw_station(canvas, type, location, crowded_time):
    # draw the station overcrowd image
    crowded = float(crowded_time) / crowded_limit
    color_str = "rgba(255, 0, 0, %f)" % crowded
    canvas.draw_circle(location, 20, 40, color_str, color_str)    

    # draw station to location given
    if type == "Circle":
        canvas.draw_circle(location, 10, 4, 'Black', 'White')
    if type == "Square":
        point_list = [[location[0] - 9, location[1] - 9], [location[0] - 9, location[1] + 9], [location[0] + 9, location[1] + 9], [location[0] + 9, location[1] - 9]]
        canvas.draw_polygon(point_list, 4, 'Black', 'White')
    if type == "Triangle":
        point_list = [[location[0], location[1] - 7], [location[0] - 8.66, location[1] + 9], [location[0] + 8.66, location[1] + 9]]
        canvas.draw_polygon(point_list, 4, 'Black', 'White')
        
def draw_line(location1, location2, canvas, color):
    # draw line to the two stations given
    if color == line_selection:
        color_str = color
    else:
        if color == "Red":
            color_str = "rgba(255, 0, 0, 0.5)"

        if color == "Blue":
            color_str = "rgba(0, 0, 255, 0.5)"

        if color == "Green":
            color_str = "rgba(0, 255, 0, 0.5)"

        if color == "Yellow":
            color_str = "rgba(255, 255, 0, 0.5)"

        if color == "Orange":
            color_str = "rgba(255, 165, 0, 0.5)"
    
    canvas.draw_line(location1, location2, 10, color_str)
    
    """ old version: non transparent line\\\\\\\\\\\\\\\
    canvas.draw_line(location1, location2, 10, color)
    """
    
def draw_train(canvas, location, rotation):
    canvas.draw_image(black_train_pic, (18, 9), (36, 18), location, (48, 24), rotation)
    
def draw_station_passenger(canvas, station_location, passengers):
    location = [station_location[0] + 20, station_location[1] - 2.5]
    for passenger in passengers:
        destination = passenger.destination
        if destination == "Circle":
            canvas.draw_circle(location, 2.5, 4, 'Black', 'Black')
        if destination == "Square":
            point_list = [[location[0] - 2.25, location[1] - 2.25], [location[0] - 2.25, location[1] + 2.25], [location[0] + 2.25, location[1] + 2.25], [location[0] + 2.25, location[1] - 2.25]]
            canvas.draw_polygon(point_list, 4, 'Black', 'Black')
        if destination == "Triangle":
            point_list = [[location[0], location[1] - 1.75], [location[0] - 2.16, location[1] + 2.25], [location[0] + 2.16, location[1] + 2.25]]
            canvas.draw_polygon(point_list, 4, 'Black', 'Black')
        location = [location[0] + 10, location[1]]
        
def draw_train_passenger(canvas, position, passengers):
    location = [position[0] - 12, position[1] - 4.5]
    passenger_no = 0
    for passenger in passengers:
        if passenger.destination == "Circle":
            canvas.draw_circle(location, 2.5, 4, 'white', )
        if passenger.destination == "Square":
            point_list = [[location[0] - 2.25, location[1] - 2.25], [location[0] - 2.25, location[1] + 2.25], [location[0] + 2.25, location[1] + 2.25], [location[0] + 2.25, location[1] - 2.25]]
            canvas.draw_polygon(point_list, 4, 'white', 'white')
        if passenger.destination == "Triangle":
            point_list = [[location[0], location[1] - 1.75], [location[0] - 2.16, location[1] + 2.25], [location[0] + 2.16, location[1] + 2.25]]
            canvas.draw_polygon(point_list, 4, 'white', 'white')
        passenger_no += 1
        if passenger_no == 4:
            location = [position[0] - 12, position[1] + 4.5]
        else:
            location = [location[0] + 9, location[1]]

def draw_selected_station(canvas):
    if len(station_station_click) == 1:
        station = station_station_click[0]
        
        if station.type == "Circle":
            canvas.draw_circle(station.location, 10, 1, 'Black', line_selection)
        if station.type == "Square":
            point_list = [[station.location[0] - 9, station.location[1] - 9], [station.location[0] - 9, station.location[1] + 9], [station.location[0] + 9, station.location[1] + 9], [station.location[0] + 9, station.location[1] - 9]]
            canvas.draw_polygon(point_list, 1, 'Black', line_selection)
        if station.type == "Triangle":
            point_list = [[station.location[0], station.location[1] - 7], [station.location[0] - 8.66, station.location[1] + 9], [station.location[0] + 8.66, station.location[1] + 9]]
            canvas.draw_polygon(point_list, 1, 'Black', line_selection)

def draw_line_ui(canvas):
    if line_selection == "Red":
        point = (720,410)
        draw_position = [(point[0], point[1] - 9),(point[0] + 60, point[1] - 9),(point[0] + 60, point[1] + 9),(point[0], point[1] + 9)]
        canvas.draw_polygon(draw_position, 4, "black")
    
    elif line_selection == "Blue":
        point = (720, 430)
        draw_position = [(point[0], point[1] - 9),(point[0] + 60, point[1] - 9),(point[0] + 60, point[1] + 9),(point[0], point[1] + 9)]
        canvas.draw_polygon(draw_position, 4, "black")
    
    elif line_selection == "Green":
        point = (720, 450)
        draw_position = [(point[0], point[1] - 9),(point[0] + 60, point[1] - 9),(point[0] + 60, point[1] + 9),(point[0], point[1] + 9)]
        canvas.draw_polygon(draw_position, 4, "black")
    
    elif line_selection == "Yellow":
        point = (720, 470)
        draw_position = [(point[0], point[1] - 9),(point[0] + 60, point[1] - 9),(point[0] + 60, point[1] + 9),(point[0], point[1] + 9)]
        canvas.draw_polygon(draw_position, 4, "black")
    
    elif line_selection == "Orange":
        point = (720, 490)
        draw_position = [(point[0], point[1] - 9),(point[0] + 60, point[1] - 9),(point[0] + 60, point[1] + 9),(point[0], point[1] + 9)]
        canvas.draw_polygon(draw_position, 4, "black")
        
            
def get_point(location1, location2):
    # get the turning point for the rail between two given station position
    if location1[0] == location2[0]:
        return None
    if location1[1] == location2[1]:
        return None
    if math.fabs(location1[0] - location2[0]) == math.fabs(location1[1] - location2[1]):
        return None
    if location1[0] > location2[0]:
        if location1[1] > location2[1]:
            if math.fabs(location1[0] - location2[0]) > math.fabs(location1[1] - location2[1]):
                return [location2[0] + location1[1] - location2[1], location1[1]]
            else:
                return [location1[0], location2[1] + location1[0] - location2[0]]
        else:
            if math.fabs(location1[0] - location2[0]) > math.fabs(location1[1] - location2[1]):
                return [location2[0] + location2[1] - location1[1], location1[1]]
            else:
                return [location1[0], location2[1] + location2[0] - location1[0]]
    else:
        if location1[1] > location2[1]:
            if math.fabs(location1[0] - location2[0]) > math.fabs(location1[1] - location2[1]):
                return [location2[0] + location2[1] - location1[1], location1[1]]
            else:
                return [location1[0], location2[1] + location2[0] - location1[0]]
        else:
            if math.fabs(location1[0] - location2[0]) > math.fabs(location1[1] - location2[1]):
                return [location2[0] + location1[1] - location2[1], location1[1]]
            else:
                return [location1[0], location2[1] + location1[0] - location2[0]]
    
def point_line_dist(point, line_point1, line_point2): 
    # get the shortest distance between the imported point and line segment
    px = line_point2[0]-line_point1[0]
    py = line_point2[1]-line_point1[1]

    lenth = px*px + py*py

    u =  ((point[0] - line_point1[0]) * px + (point[1] - line_point1[1]) * py) / float(lenth)

    if u > 1:
        u = 1
    elif u < 0:
        u = 0

    x = line_point1[0] + u * px
    y = line_point1[1] + u * py

    dx = x - point[0]
    dy = y - point[1]

    dist = math.sqrt(dx*dx + dy*dy)

    return dist
    
def connect(station1, station2):
    # take two stations and add them to the last line in line_group
    if not station1 in line_group.line_list[-1].stations:
        line_group.line_list[-1].add(station1)
    if not station2 in line_group.line_list[-1].stations:
        line_group.line_list[-1].add(station2)
    line_group.line_list[-1].update_point()

def create_new_line():
    new_line = Line()
    line_group.line_list.append(new_line)
    
def station_station_click_update():
    global station_station_click, line_selection
    stop = False
    if len(station_station_click) == 2:
        
        # cancel on double click
        if station_station_click[0] == station_station_click[1]:
            station_station_click = []
            # update line
            line.update_point()
            line.update_structure()

            #reset tracker
            station_station_click = []
            return None
        
        # add station on selected line
        for line in line_group.line_list:
            if line.color == line_selection:
                if station_station_click[0] == line.stations[-1] or station_station_click[1] == line.stations[-1] or station_station_click[0] == line.stations[0] or station_station_click[1] == line.stations[0]:
                    if station_station_click[0] == line.stations[-1] and (station_station_click[1] in line.stations):
                        #reset tracker
                        station_station_click = []
                        return None
                    
                    elif station_station_click[0] == line.stations[0] and (station_station_click[1] in line.stations):
                        #reset tracker
                        station_station_click = []
                        return None
                    
                    elif station_station_click[0] == line.stations[-1]:
                        line.stations.append(station_station_click[1])

                        #update line
                        line.update_point()
                        line.update_structure()

                        #reset tracker
                        station_station_click = []
                        return None
                    
                    elif station_station_click[1] == line.stations[-1]:
                        line.stations.append(station_station_click[0])

                        #update line
                        line.update_point()
                        line.update_structure()

                        #reset tracker
                        station_station_click = []
                        return None
                
                    elif station_station_click[0] == line.stations[0]:
                        line.stations.insert(0, station_station_click[1])
                        # update train position when add station at the beginning
                        if get_point(station_station_click[0].location, station_station_click[1].location) == None:
                            for train in train_group.train_list:
                                if train.line == line:
                                    train.current += 1
                                    train.current_point += 1
                        else:
                            for train in train_group.train_list:
                                if train.line == line:
                                    train.current += 1
                                    train.current_point += 2

                        # update line
                        line.update_point()
                        line.update_structure()

                        #reset tracker
                        station_station_click = []
                        return None
                    
                    elif station_station_click[1] == line.stations[0]:
                        line.stations.insert(0, station_station_click[0])
                        # update train position when add station at the beginning
                        if get_point(station_station_click[0].location, station_station_click[1].location) == None:
                            for train in train_group.train_list:
                                if train.line == line:
                                    train.current += 1
                                    train.current_point += 1
                        else:
                            for train in train_group.train_list:
                                if train.line == line:
                                    train.current += 1
                                    train.current_point += 2

                        # update line
                        line.update_point()
                        line.update_structure()

                        #reset tracker
                        station_station_click = []
                        return None
                
                elif (station_station_click[0] in line.stations) or (station_station_click[1] in line.stations):
                    # update line
                    line.update_point()
                    line.update_structure()

                    #reset tracker
                    station_station_click = []
                    return None

        
        
        # if the stations are not at the end of the line, make a new line
        if len(line_group.line_list) < 6:
            new_line = Line(line_selection)
            line_group.line_list.append(new_line)
            new_line.stations.append(station_station_click[0])
            new_line.stations.append(station_station_click[1])
            new_line.update_point()
            new_line.update_structure()
            new_line.add_train()

            # reset tracker
            station_station_click = []

        #reset tracker
        station_station_click = []
        return None
    
def line_click_update():
    global line_click
    if len(line_click) == 2:
        if line_click[0] == line_click [1]:
            line_group.line_list.remove(line_click[0])
            for train in train_group.train_list:
                if train.line == line_click[0]:
                    train_group.train_list.remove(train)
        line_click = []

def tutorial_update():
    global start, tutorial, tutorial_step, tutorial_message, temporary_timer
    if screen == "Game":
        if tutorial_step == 0:
            tutorial_message = "Click on two stations to build a line between them."
            if not len(line_group.line_list) == 0:
                tutorial_step = 1

        if tutorial_step == 1:
            tutorial_message = "Great Job! Now add the third station to your line!"
            if len(line_group.line_list[0].stations) == 3:
                tutorial_step = 3
            if len(line_group.line_list) == 2:
                tutorial_step = 2

        if tutorial_step == 2:
            tutorial_message = "Oops you created a 2nd line, double click on the line to delete it."
            if len(line_group.line_list) == 1:
                tutorial_step = 1

        if tutorial_step == 3:
            tutorial_message = "Cool, we now have a passenger at our station!"
            if temporary_timer == 0:
                line_group.line_list[0].stations[0].new_passenger()
            temporary_timer += 1
            if len(line_group.line_list[0].stations[0].passengers) == 0:
                tutorial_step = 4
                temporary_timer = 0

        if tutorial_step == 4:
            tutorial_message = "Once the passenger arrive at his station, you will get a point!"
            if score == 1:
                tutorial_step = 5

        if tutorial_step == 5:
            tutorial_message = "The new station is crowded! create a new line to get passengers moving!"
            if temporary_timer == 0:
                new_station = Station([130,50], "Circle")
                new_station.crowded_time = 50
                new_station.new_passenger()
                new_station.new_passenger()
                new_station.new_passenger()
                new_station.new_passenger()
                new_station.new_passenger()
                new_station.new_passenger()
                station_group.add(new_station)
            temporary_timer += 1
            if station_group.station_list[3].crowded_time == 0:
                temporary_timer = 0
                tutorial_step = 6

        if tutorial_step == 6:
            tutorial_message = "Now you've learn the basics, go and start building!"
            temporary_timer += 1
            if temporary_timer == 10:
                tutorial = False
                temporary_timer = 0
                tutorial_message = ""
                tutorial_step = 0
                start = True
            

def station_spawner():
    global station_spawn_timer
    if station_spawn_timer >= station_spawn_interval:
        if not len(station_spawn_list) == 0:
            station_group.station_list.append(station_spawn_list.pop(0))
            station_spawn_timer = 0
    station_spawn_timer += 1
    if double_speed:
        station_spawn_timer += 1

        
def game_over():
    global game_over_message, start, screen
    game_over_message = "Game Over"
    start = False
    screen = "Menu"
        
#--------------------------Classes
class Passengers:
    def __init__():
        pass
    
    def draw():
        pass
    
class Passenger:
    def __init__(self, destination):
        self.destination = destination
    
    def draw():
        pass

class Trains:
    def __init__(self):
        self.train_list = []
    
    def draw(self, canvas):
        for train in self.train_list:
            train.draw(canvas)
            
    def update(self):
        for train in self.train_list:
            train.update()

class Train:
    def __init__(self, position, line, current_station, current_point, next_station, next_point):
        self.position = [position[0], position[1]]
        self.waiting = True
        self.turn = True
        self.line = line
        self.current = current_station
        self.current_point = current_point
        self.next_station = next_station
        self.next_point = next_point
        self.direction = True
        self.wait = 0
        self.passenger = []
        self.rotation = 0
        self.passenger_pickup()
    
    def draw(self, canvas):
        draw_train(canvas, self.position, self.rotation)
        draw_train_passenger(canvas, self.position, self.passenger)
    
    def update(self):
        station_vector = [self.next_station.location[0] - self.position[0], self.next_station.location[1] - self.position[1]]
        station_distance = math.sqrt(math.pow(station_vector[0], 2) + math.pow(station_vector[1], 2))
        point_vector = [self.next_point[0] - self.position[0], self.next_point[1] - self.position[1]]
        point_distance = math.sqrt(math.pow(point_vector[0], 2) + math.pow(point_vector[1], 2))
        speed_co = SPEED / (point_distance + 0.0001)
        point_rotation = math.atan2(point_vector[1], point_vector[0])

        if self.waiting:
            # if stop, check for move, and wait
            if self.wait >= 60:
                self.waiting = False
                self.wait = 0
            else:
                self.wait += 1
                if double_speed:
                    self.wait += 1
        elif self.turn:
            if math.fabs(self.rotation - point_rotation) < 0.1:
                self.rotation = point_rotation
                self.turn = False
            else:
                if self.rotation > point_rotation:
                    self.rotation -= 0.1
                    if double_speed:
                        self.rotation -= 0.1
                else:
                    self.rotation += 0.1
                    if double_speed:
                        self.rotation += 0.1
        else:
            # if moving, check for stop, and move
            if station_distance < 2:
                self.waiting = True
                self.turn = True
                self.destination_update()
                self.point_update()
                self.passenger_dropoff()
                self.passenger_pickup()
            elif point_distance < 2:
                self.turn = True
                self.point_update()
            else: 
                self.position[0] += point_vector[0] * speed_co
                self.position[1] += point_vector[1] * speed_co
                if double_speed:
                    self.position[0] += point_vector[0] * speed_co
                    self.position[1] += point_vector[1] * speed_co
                
    def point_update(self):
        if self.direction:
            self.current_point += 1
            if self.current_point == len(self.line.point_list) - 1:
                self.direction = False
                self.next_point = self.line.point_list[self.current_point - 1]
            else:
                self.next_point = self.line.point_list[self.current_point + 1]
        else:
            self.current_point -= 1
            if self.current_point == 0:
                self.direction = True
                self.next_point = self.line.point_list[self.current_point + 1]
            else:
                self.next_point = self.line.point_list[self.current_point - 1]        
    
    def destination_update(self):
        # find if the train is at the end and update the direction and destination of the train
        if self.direction:
            self.current += 1
            if self.current == len(self.line.stations) - 1:
                #self.direction = False
                self.next_station = self.line.stations[self.current - 1]
            else:
                self.next_station = self.line.stations[self.current + 1]
        else:
            self.current -= 1
            if self.current == 0:
                #self.direction = True
                self.next_station = self.line.stations[self.current + 1]
            else:
                self.next_station = self.line.stations[self.current - 1]
            
    def passenger_dropoff(self):
        # Delete passenger that arrives at destination and add score
        for passenger in set(self.passenger):
            if self.line.stations[self.current].type == passenger.destination:
                self.passenger.remove(passenger)
                global score
                score += 1
    
    def passenger_pickup(self):
        for passenger in set(self.line.stations[self.current].passengers):
            available_destination = []
            if self.direction:
                for a in range(self.current + 1, len(self.line.stations)):
                    available_destination.append(self.line.stations[a].type)
            else:
                for a in range(0, self.current):
                    available_destination.append(self.line.stations[a].type)
                    
            if passenger.destination in available_destination:
                if len(self.passenger) < 8:
                    self.line.stations[self.current].passengers.remove(passenger)
                    self.passenger.append(passenger)
    
class Stations:
    def __init__(self):
        self.station_list = []
    
    def draw(self, canvas):
        for station in self.station_list:
            station.draw(canvas)
    
    def add(self, station):
        self.station_list.append(station)
        
    def update(self):
        for station in self.station_list:
            station.update()
    
class Station:
    def __init__(self, location, type):
        self.location = [location[0], location[1]]
        self.passengers = []
        self.crowded_time = 0
        self.type = type
        self.timer = 0
    
    def draw(self, canvas):
        draw_station(canvas, self.type, self.location, self.crowded_time)
        draw_station_passenger(canvas, self.location, self.passengers)
    
    def add_passenger(self, passenger):
        self.passengers.append(passenger)
        
    def new_passenger(self):
        destination = list(STATION_TYPE)
        destination.remove(self.type)
        new_passenger = Passenger(random.choice(destination))
        self.passengers.append(new_passenger)
        
    def update(self):
        # creat new passenger every spawn interval
        if self.timer >= spawn_interval:
            if start:
                self.new_passenger()
                self.timer = 0
        else:
            self.timer += 1
            if double_speed:
                self.timer += 1
        # station overload timer
        if len(self.passengers) >= 6:
            if self.crowded_time > crowded_limit:
                game_over()
            else:
                self.crowded_time += 1
                if double_speed:
                    self.crowded_time += 1
        else:
            if not self.crowded_time == 0:
                self.crowded_time -= 1
                if double_speed:
                    self.crowded_time -=1
            

class Lines:
    def __init__(self):
        self.line_list = []        
        
class Line:
    def __init__(self, color):
        self.stations = []
        self.point_list = []
        self.structure = []
        self.color = color
    
    def add(self, station):
        self.stations.append(station)
        
    def update_point(self):
        self.point_list = []
        i = 1
        self.point_list.append(self.stations[0].location)
        while i < len(self.stations):
            point = get_point(self.stations[i-1].location, self.stations[i].location)
            if not point == None:
                self.point_list.append(point)
            self.point_list.append(self.stations[i].location)
            i += 1
            
    def update_structure(self):
        # update all the segments in the line
        # (point1, point2, station1, station2)
        self.structure = []
        i = 1
        while i < len(self.stations):
            point = get_point(self.stations[i-1].location, self.stations[i].location)
            if point == None:
                self.structure.append([self.stations[i-1].location, self.stations[i].location, i-1, i])
            else:
                self.structure.append([self.stations[i-1].location, point, i-1, i])
                self.structure.append([point, self.stations[i].location, i-1, i])
            i += 1
        
        
    def draw(self, canvas):
        i = 1
        while i < len(self.point_list):
            draw_line(self.point_list[i-1], self.point_list[i], canvas, self.color)
            i += 1
            
    def add_train(self):
        new_train = Train(self.stations[0].location, self, 0, 0, self.stations[1], self.point_list[1])
        train_group.train_list.append(new_train)
        

        

#------------------Define event handlers

def draw_handler(canvas):
    if screen == "Game":
        # draw game elements
        if not len(line_group.line_list) == 0:
            i = 0
            highlight = False
            for line in set(line_group.line_list):
                color = COLORS[i]
                if color == line_selection:
                    line_highlight = line
                    color_highlight = color
                    highlight = True
                else:
                    line.draw(canvas)
                i += 1
            if highlight:
                line_highlight.draw(canvas)
            i = 0

        train_group.update()
        if not len(train_group.train_list) == 0:
            train_group.draw(canvas)  
        station_group.draw(canvas)
        
        # call frame updates
        station_group.update()
        station_station_click_update()
        line_click_update()        
        
        # draw UI elements
        # screen message
        canvas.draw_text("Score: " + str(score), (700, 20), 24, 'Black')
        canvas.draw_text(game_over_message, (50, 250), 24, 'Black')
        lines_left = 5 - len(line_group.line_list)
        canvas.draw_text("Lines left: " + str(lines_left), (20, 480), 24, 'Black')
        
        # speed buttons
        canvas.draw_polygon([[740, 40], [740, 60], [756, 50]], 1, 'Black', 'Black')
        canvas.draw_polygon([[730, 70], [730, 90], [746, 80]], 1, 'Black', 'Black')
        canvas.draw_polygon([[750, 70], [750, 90], [766, 80]], 1, 'Black', 'Black')
        
        # tutorial message
        canvas.draw_text(tutorial_message, (50, 400), 24, 'Black')
        
        # station selection UI
        draw_selected_station(canvas)
        
        #line selection
        
        canvas.draw_line((720, 410), (780, 410), 14, "Red")
        canvas.draw_line((720, 430), (780, 430), 14, "Blue")
        canvas.draw_line((720, 450), (780, 450), 14, "Green")
        canvas.draw_line((720, 470), (780, 470), 14, "Yellow")
        canvas.draw_line((720, 490), (780, 490), 14, "Orange")
        
        # highlight selected UI
        draw_line_ui(canvas)
        
        
    if screen == "Menu":
        canvas.draw_image(menu, (1147,722), (2294,1444), (400,250), (800,500))
        canvas.draw_text("Tutorial", (250, 370), 48, 'Black')
        canvas.draw_text("Easy", (550, 370), 48, 'Black')
        canvas.draw_text("Medium", (250, 460), 48, 'Black')
        canvas.draw_text("Hard", (550, 460), 48, 'Black')
    
def timer_handler():
    # if in tutorial, run the tutotial handler
    if tutorial:
        tutorial_update()
    
    # if the game start, run the station spawner
    if start:
        station_spawner()
        
    
def key_handler(key):
    if screen == "Game":
        if key == simplegui.KEY_MAP['1']:
            create_new_line()
            connect(my_station1, my_station2)
            line_group.line_list[0].add_train()
        if key == simplegui.KEY_MAP['2']:
            connect(my_station2, my_station3)
        
    if screen == "Menu":
        pass
        
def mouse_handler(position):
    global double_speed, line_selection
    if screen == "Game":
        # Line draw selection
        if position[0] > 720 and position[0] < 780:
            if position[1] > 400 and position[1] < 420:
                line_selection = "Red"
            if position[1] > 420 and position[1] < 440:
                line_selection = "Blue"
            if position[1] > 440 and position[1] < 460:
                line_selection = "Green"
            if position[1] > 460 and position[1] < 480:
                line_selection = "Yellow"
            if position[1] > 480 and position[1] < 500:
                line_selection = "Orange"
        
        # Game speed control
        if position[0] < 770 and position[0] > 730 and position[1] > 40 and position[1] < 60:
            double_speed = False
        
        if position[0] < 770 and position[0] > 730 and position[1] > 70 and position[1] < 90:
            double_speed = True
        
        # check if mouse click near a station
        for station in station_group.station_list:
            distance = math.sqrt(math.pow(station.location[0] - position[0], 2) + math.pow(station.location[1] - position[1], 2))
            if distance < 15:
                if len(station_station_click) == 0:
                    station_station_click.append(station)
                else:
                    if not station == station_station_click[0]:
                        station_station_click.append(station)
                return None

        # check if mouse click near a line
        for line in line_group.line_list:
            for segment in line.structure:
                distance = point_line_dist(position, segment[0], segment[1])
                if distance < 5:
                    line_click.append(line)
                        
    if screen == "Menu":
        if position[0] > 250 and position[0] < 450 and position[1] < 370 and position[1] > 320:
            # click on Tutorial Button
            reset("Tutorial")
            
        if position[0] > 550 and position[0] < 750 and position[1] < 370 and position[1] > 320:
            # click on Easy Button
            reset("Easy")
            
        if position[0] > 250 and position[0] < 450 and position[1] < 460 and position[1] > 410: 
            # click on Medium Button
            reset("Medium")
            
        if position[0] > 550 and position[0] < 750 and position[1] < 460 and position[1] > 410:
            # click on Hard Button
            reset("Hard")
            
        
            
def start_game():
    global start
    start = True
    
def reset(mode):
    global score, game_over_message, tutorial_message, station_station_click, start, screen, tutorial
    global station_group, line_group, train_group
    global station_spawn_interval, spawn_interval, crowded_limit
    
    if mode == "Tutorial":
        # Reset all globals
        score = 0
        game_over_message = ""
        station_station_click = []
        start = False
        tutorial = True
        screen = "Game"
        station_spawn_interval = 30
        spawn_interval = 600
        crowded_limit = 1200

        
        # Stations initialize
        station_group = Stations()
        my_station1 = Station([430,50], "Circle")
        my_station2 = Station([350,230], "Square")
        my_station3 = Station([150,200], "Triangle")
        my_station4 = Station([550,300], "Triangle")
        my_station5 = Station([220,100], "Circle")
        my_station6 = Station([550,200], "Triangle")
        my_station7 = Station([430,380], "Circle")
        my_station8 = Station([240,400], "Square")
        my_station9 = Station([170,300], "Triangle")
        my_station10 = Station([430,200], "Circle")
        my_station11 = Station([540,400], "Square")

        station_group.add(my_station1)
        station_group.add(my_station2)
        station_group.add(my_station3)

        station_spawn_list.append(my_station4)
        station_spawn_list.append(my_station5)
        station_spawn_list.append(my_station6)
        station_spawn_list.append(my_station7)
        station_spawn_list.append(my_station8)
        station_spawn_list.append(my_station9)
        station_spawn_list.append(my_station10)
        station_spawn_list.append(my_station11)

        line_group = Lines()
        train_group = Trains()
        
    if mode == "Easy":
        # Reset all globals
        score = 0
        game_over_message = ""
        station_station_click = []
        start = True
        tutorial = False
        screen = "Game"
        station_spawn_interval = 20
        spawn_interval = 600
        crowded_limit = 1200


        # Stations initialize
        station_group = Stations()
        my_station1 = Station([430,50], "Circle")
        my_station2 = Station([350,230], "Square")
        my_station3 = Station([150,200], "Triangle")
        my_station4 = Station([550,300], "Triangle")
        my_station5 = Station([220,100], "Circle")
        my_station6 = Station([550,200], "Triangle")
        my_station7 = Station([430,380], "Circle")
        my_station8 = Station([240,400], "Square")
        my_station9 = Station([170,300], "Triangle")
        my_station10 = Station([430,200], "Circle")
        my_station11 = Station([540,400], "Square")

        station_group.add(my_station1)
        station_group.add(my_station2)
        station_group.add(my_station3)
        station_group.add(my_station4)
        
        station_spawn_list.append(my_station5)
        station_spawn_list.append(my_station6)
        station_spawn_list.append(my_station7)
        station_spawn_list.append(my_station8)
        station_spawn_list.append(my_station9)
        station_spawn_list.append(my_station10)
        station_spawn_list.append(my_station11)

        line_group = Lines()
        train_group = Trains()
    
    if mode == "Medium":
        # Reset all globals
        score = 0
        game_over_message = ""
        station_station_click = []
        start = True
        tutorial = False
        screen = "Game"
        station_spawn_interval = 20
        spawn_interval = 420
        crowded_limit = 900


        # Stations initialize
        station_group = Stations()
        my_station1 = Station([430,50], "Circle")
        my_station2 = Station([350,230], "Square")
        my_station3 = Station([150,200], "Triangle")
        my_station4 = Station([550,300], "Triangle")
        my_station5 = Station([220,100], "Circle")
        my_station6 = Station([550,200], "Triangle")
        my_station7 = Station([430,380], "Circle")
        my_station8 = Station([240,400], "Square")
        my_station9 = Station([170,300], "Triangle")
        my_station10 = Station([430,200], "Circle")
        my_station11 = Station([540,400], "Square")

        station_group.add(my_station1)
        station_group.add(my_station2)
        station_group.add(my_station3)
        station_group.add(my_station4)
        station_group.add(my_station5)
        station_group.add(my_station6)
        
        station_spawn_list.append(my_station7)
        station_spawn_list.append(my_station8)
        station_spawn_list.append(my_station9)
        station_spawn_list.append(my_station10)
        station_spawn_list.append(my_station11)

        line_group = Lines()
        train_group = Trains()
    
    if mode == "Hard":
        # Reset all globals
        score = 0
        game_over_message = ""
        station_station_click = []
        start = True
        tutorial = False
        screen = "Game"
        station_spawn_interval = 20
        spawn_interval = 300
        crowded_limit = 900


        # Stations initialize
        station_group = Stations()
        my_station1 = Station([430,50], "Circle")
        my_station2 = Station([350,230], "Square")
        my_station3 = Station([150,200], "Triangle")
        my_station4 = Station([550,300], "Triangle")
        my_station5 = Station([220,100], "Circle")
        my_station6 = Station([550,200], "Triangle")
        my_station7 = Station([430,380], "Circle")
        my_station8 = Station([240,400], "Square")
        my_station9 = Station([170,300], "Triangle")
        my_station10 = Station([430,200], "Circle")
        my_station11 = Station([540,400], "Square")

        station_group.add(my_station1)
        station_group.add(my_station2)
        station_group.add(my_station3)
        station_group.add(my_station4)
        station_group.add(my_station5)
        station_group.add(my_station6)
        station_group.add(my_station7)
        station_group.add(my_station8)
        station_group.add(my_station9)
        
        station_spawn_list.append(my_station10)
        station_spawn_list.append(my_station11)

        line_group = Lines()
        train_group = Trains()
    

station_group = Stations()
line_group = Lines()
train_group = Trains()
#----------------------Create a frame
black_train_pic = simplegui.load_image("https://dl.dropbox.com/s/3jss4r73a5q0wiq/black_train.jpg?dl=0")
menu = simplegui.load_image("https://dl.dropbox.com/s/7f2ewottnbte37q/menu.jpg?dl=0")

frame = simplegui.create_frame('Game', 800, 500)
frame.set_canvas_background('rgb(247,233,206)')
frame.set_draw_handler(draw_handler)
frame.set_mouseclick_handler(mouse_handler)
start_button = frame.add_button('Rush Hour!', start_game)
reset_button = frame.add_button('New Game', reset)

timer = simplegui.create_timer(1000, timer_handler)


#temporary codes
frame.set_keydown_handler(key_handler)

#-----------------Register event handlers

#------------------Start frame and timer

frame.start()
timer.start()