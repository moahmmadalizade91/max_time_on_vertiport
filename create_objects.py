import os
import pandas as pd
import numpy as np
import json
from objects import Vertiport, Pad, Aircraft
from copy import deepcopy


def create_vertiport(file_name: str) -> (list, int):
    """
    This function creates vertiport objects alongside their pads.

    Args:
        file_name (str): vertiport file name that contains its location, pads and number of stands.

    Returns:
        vertiport_objects (list): list of built vertiport objects.
        last_id (int): last objects id, to be used for creating other objects.

    """
    i = 1
    root_path = os.getcwd() + f"\\{file_name}.xlsx"
    excel_data = pd.ExcelFile(root_path)
    sheet_names = excel_data.sheet_names
    excel_data = pd.read_excel(root_path, sheet_name=sheet_names[0])
    data_dict = excel_data.to_dict(orient='dict')
    vertiport_objects = []
    vertiport_created = False
    for index in data_dict['Name']:
        if type(data_dict['Name'][index]) == str:
            if vertiport_created:
                vertiport_obj.pads = pads
                vertiport_objects.append(deepcopy(vertiport_obj))
            vertiport_obj = Vertiport(i, [], [], json.loads(data_dict['Position'][index]), data_dict['Name'][index], data_dict['Capacity'][index])
            vertiport_created = True
            pads = []
            i += 1
            if data_dict['Pad'][index]:
                pad_obj = Pad(i, data_dict['Pad'][index] if type(data_dict['Pad'][index]) == str else 'pad with no name')
                pads.append(pad_obj)
                i += 1
        elif np.isnan(data_dict['Name'][index]):
            if data_dict['Pad'][index]:
                pad_obj = Pad(i, data_dict['Pad'][index] if type(data_dict['Pad'][index]) == str else 'pad with no name')
                pads.append(pad_obj)
                i += 1
    vertiport_obj.pads = pads
    # vertiport_obj.aircrafts = aircrafts
    vertiport_objects.append(deepcopy(vertiport_obj))
    last_id = i
    return vertiport_objects, last_id


def create_aircrafts(aircraft_schedule_data: dict, last_id: int) -> (list, int):
    """
    This function creates aircraft objects demand_schedule_data

    Args:
        aircraft_schedule_data (dict): a dictionary that contains every aircraft's 
                                       arrival time.
        last_id (int): previous last objects id, to be used for creating other objects.

    Returns:
        demands (list): list of built aircraft objects.
        last_id (int): last objects id, to be used for creating other objects.

    """
    aircrafts = []
    for i in range(len(aircraft_schedule_data['aircraft_start_time'])):
        aircrafts.append(Aircraft(last_id, 'scheduled', [], aircraft_schedule_data['aircraft_start_time'][i]))
        last_id += 1
    return aircrafts, last_id