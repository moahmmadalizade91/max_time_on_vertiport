class Vertiport:
    def __init__(self, id_, pads, aircrafts, position, name, capacity):
        self.id_ = id_
        self.pads = pads
        self.position = position
        self.name = name
        self.aircrafts = aircrafts
        self.capacity = capacity
        self.holding_aircrafts = []
        
        
class Pad:
    def __init__(self, id_, name):
        self.id_ = id_
        self.name = name
        self.status = 'ready'
        self.schedule_list = []
        self.occupied_aircraft = None
        self.position_end =[]


class Aircraft:
    def __init__(self, id_, status, schedule_list, arrival_time):
        self.id_ = id_
        self.status = status
        self.schedule_list = schedule_list
        self.pad_id = None
        self.flight_hours = 0
        self.holding_violation = False
        self.arrival_time = arrival_time