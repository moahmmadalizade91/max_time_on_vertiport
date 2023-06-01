from objects import Vertiport, Pad, Aircraft


def object_finder(objects: list, attribute_dict: dict):
    """
    This function finds an object with the attributes in the attribute_dict.

    Args:
        objects (list)
        attribute_dict (dict): a dict to find objects in this form:
            {attribute: attribute value that we want}

    Returns:
        out_obj : found object.

    """
    out_obj = []
    for obj in objects:
        for attribute in attribute_dict:
            if getattr(obj, attribute) == attribute_dict[attribute]:
                out_obj = [obj]
            else:
                out_obj = []
                break
        if out_obj:
            break
    if not out_obj:
        out_obj = ['object not found']
    return out_obj
    

def find_object_schedule_by_type(obj: Aircraft, schedule_type: str) -> dict:
    """
    This function finds schedule info of schedule type in objects (mostly aircraft).
    """
    for time_schedule in obj.schedule_list:
        if time_schedule['type'].lower() == schedule_type:
            return time_schedule
    return {}


def find_empty_pad(vertiport: Vertiport) -> (None, int):
    """
    This function finds id_ of an empty pad in a vertiport.
    """
    for pad in vertiport.pads:
        if pad.status.lower() == 'ready':
            return pad.id_
    return None


def check_vertiport_capacity(aircraft: Aircraft, destination: Vertiport) -> bool:
    """
    This function checks if destination vertiport have enough capacity for aircraft.
    """
    occupied_capacity = 0
    for aircraft_obj in destination.aircrafts:
        if aircraft_obj.status.lower() in ['ready', 'occupied', 'turnaround', 'landing']:
            occupied_capacity += 1
    first_come_first_serve_flag = True
    if destination.holding_aircrafts:
        if aircraft.id_ in destination.holding_aircrafts:
            first_come_first_serve_flag = destination.holding_aircrafts.index(aircraft.id_) == 0
        else:
            first_come_first_serve_flag = False
    if occupied_capacity < destination.capacity and first_come_first_serve_flag:
        return True
    else:
        return False



def physics_module(vertiport: Vertiport, aircrafts: list, current_epoch: int, 
                   time_on_station: int, takeoff_occupation_time: int, 
                   landing_occupation_time: int,  holding_duration: int):
    """
    This function acts as a manager fot objects. This function moves aircrafts, 
    manage demands, and collect simulation's data.
    All Arguments' description is available in run_simulation module in this file.
    """
    msg_list = []
    holding_violations = 0
    for aircraft in aircrafts:
        if aircraft.holding_violation:
            holding_violations += 1
        if aircraft.status.lower() == 'scheduled' and current_epoch >= aircraft.arrival_time:
            pad_id = find_empty_pad(vertiport)
            vertiport_state = check_vertiport_capacity(aircraft, vertiport) 
            if vertiport_state and pad_id is not None:
                vertiport.capacity -= 1
                aircraft.schedule_list.append({'t_0':current_epoch, 't_f': current_epoch + landing_occupation_time, 'type':'landing'})
                aircraft.pad_id = pad_id
                aircraft.status = 'landing'
                pad_obj = object_finder(vertiport.pads, {'id_':pad_id})[0]
                pad_obj.status = 'landing'
            if aircraft.status.lower() == 'scheduled':
                aircraft.schedule_list += [{'t_0':current_epoch, 't_f': current_epoch + holding_duration, 
                                                'type':'holding'}]
                aircraft.status = 'holding'
        elif aircraft.status.lower() == 'holding':
            holding_schedule = find_object_schedule_by_type(aircraft, 'holding')
            if current_epoch >= holding_schedule['t_f']:
                aircraft.holding_violation = True
            pad_id = find_empty_pad(vertiport)
            holding_schedule = find_object_schedule_by_type(aircraft, 'holding')
            vertiport_state = check_vertiport_capacity(aircraft, vertiport) 
            if vertiport_state and pad_id is not None:
                vertiport.capacity -= 1
                aircraft.schedule_list.append({'t_0':current_epoch, 't_f': current_epoch + landing_occupation_time, 'type':'landing'})
                aircraft.status = 'landing'
                aircraft.pad_id = pad_id
                holding_schedule['t_f'] = current_epoch
                pad_obj = object_finder(vertiport.pads, {'id_':pad_id})[0]
                pad_obj.status = 'landing'
        elif aircraft.status.lower() == 'landing':
            landing_schedule = find_object_schedule_by_type(aircraft, 'landing')
            if current_epoch >= landing_schedule['t_f']:
                aircraft.schedule_list.append({'t_0':current_epoch, 't_f': current_epoch + time_on_station, 'type':'turnaround'})
                aircraft.status = 'turnaround'
                pad_obj = object_finder(vertiport.pads, {'id_':aircraft.pad_id})[0]
                aircraft.pad_id = None
                pad_obj.status = 'ready'
        elif aircraft.status.lower() == 'turnaround':
            turnaround_schedule = find_object_schedule_by_type(aircraft, 'turnaround')
            if current_epoch >= turnaround_schedule['t_f']:
                pad_id = find_empty_pad(vertiport)
                if pad_id is not None:
                    aircraft.schedule_list.append({'t_0':current_epoch, 't_f': current_epoch + takeoff_occupation_time, 'type':'takeoff'})
                    aircraft.status = 'takeoff'
                    aircraft.pad_id = pad_id
                    pad_obj = object_finder(vertiport.pads, {'id_':pad_id})[0]
                    pad_obj.status = 'takeoff'
                    vertiport.capacity += 1
        elif aircraft.status.lower() == 'takeoff':
            takeoff_schedule = find_object_schedule_by_type(aircraft, 'takeoff')
            if current_epoch >= takeoff_schedule['t_f']:
                 aircraft.status = 'left'
                 pad_obj = object_finder(vertiport.pads, {'id_':aircraft.pad_id})[0]
                 pad_obj.status = 'ready'
    if holding_violations >= 0.1 * len(aircrafts):
        msg_list.append('too much holding violations')
    return vertiport, aircrafts, msg_list
                    

def run_simulation(vertiport: Vertiport, aircrafts: list, landing_occupation_time: int, 
                   takeoff_occupation_time: int, time_on_station: int,
                   holding_duration: int, start_time: int, end_time: int):
    """
    This function runs a simulation for a vertiport between "start_time" and "end_time".
    Having a list of arriving aircraft with a constant time_on_station that their arrival 
    time is between start_time and end_time is necessary for this function to work properly.
    Time step of simulation can be changed in the body of this function.

    Args:
        vertiport (Vertiport): a vertiport object.
        aircrafts (list): list of aircraft objects.
        landing_occupation_time (int): required time for an aircraft to descent, land and to leave a 
                                       landing pad in seconds.
        takeoff_occupation_time (int): required time for an aircraft to finish its takeoff sequences 
                                        and leave the landing pad in seconds.
        time_on_station (int): The amount of time an aircraft will stay on vertiport.
        holding_duration (int): maximum time for holding (before landing) in seconds.
        start_time (int): start time of simulation.
        end_time (int): end time of simulation.

    Returns:
        vertiports (TYPE): list of vertiport objects after simulation.
        aircrafts (TYPE): list of aircraft objects after simulation.
        msg_list (TYPE): list of messages. if there is an error in the simulation, 
                         a message will appear in this list.
        current_epoch (TYPE): last epoch of simulation.

    """
    current_epoch = start_time
    
    while current_epoch <= end_time:
        vertiports, aircrafts, msg_list = physics_module(vertiport, aircrafts, current_epoch, time_on_station, takeoff_occupation_time, landing_occupation_time, \
                                                         holding_duration) 
        if msg_list:
            break
        current_epoch += 1

    return vertiports, aircrafts, msg_list, current_epoch
        