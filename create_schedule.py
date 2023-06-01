import pandas as pd
import numpy as np
from datetime import datetime
def create_schedule(number_of_aircrafts, start_time, end_time):
    duration = end_time-start_time
    aircraft_start_time_list = []
    datetime_list = []
    heading_toward_angle_list = []
    destination_id_list = []
    origin_id_list = []
    # aircraft_id_list = []
    origin_index_main = 0
    destination_index_main = 1
    for aircraft in range(number_of_aircrafts):
        # if trip%2 == 0:
        #     # print('hi')
        #     origin_index = origin_index_main
        #     destination_index = destination_index_main
        # else:
        #     # print('hello')
        #     origin_index = destination_index_main
        #     destination_index = origin_index_main
        aircraft_start_time = int(np.random.rand() * duration + start_time)
        # print(origin_index, destination_index)
        # arrival_time_list.append(arrivial_time)
        # origin_index = int(np.random.rand()*len(airports))
        # destination_index = int(np.random.rand()*len(airports))
        # while destination_index == origin_index:
        #     destination_index = int(np.random.rand()*len(airports))
        # origin_id = airports[origin_index].id_
        # destination_id = airports[destination_index].id_
        # aircraft_id_list.append(aircraft)
        
        aircraft_start_time_list.append(aircraft_start_time)
        # origin_id_list.append(origin_id)
        # destination_id_list.append(destination_id)
    # origin_id_list = [x for _,x in sorted(zip(trip_start_time_list,origin_id_list))]
    # destination_id_list = [x for _,x in sorted(zip(trip_start_time_list,destination_id_list))]
    # aircraft_id_list = [i for i in range(number_of_aircrafts)]
    aircraft_start_time_list.sort()
    datetime_list = [datetime.fromtimestamp(i).strftime('%Y-%m-%d %H:%M:%S') for i in aircraft_start_time_list]
    data = {'aircraft_start_time':aircraft_start_time_list,
            'datetime':datetime_list}
    # df = pd.DataFrame(data)
    # writer=pd.ExcelWriter('{0}.xlsx'.format(str(output_file_name)), engine='xlsxwriter')
    # df.to_excel(writer,sheet_name='arrival_time')
    # writer.save()
    return data


def create_demand(vertiports, demand_number, start_time, end_time):
    duration = end_time-start_time
    demand_start_time_list = []
    origin_id_list = []
    destination_id_list = []
    for demand in range(demand_number):
        origin_index = int(np.random.rand()*len(vertiports))
        destination_index = int(np.random.rand()*len(vertiports))
        while destination_index == origin_index:
            destination_index = int(np.random.rand()*len(vertiports))
        origin_id = vertiports[origin_index].id_
        destination_id = vertiports[destination_index].id_
        demand_time = int(np.random.rand() * duration + start_time)
        demand_start_time_list.append(demand_time)
        origin_id_list.append(origin_id)
        destination_id_list.append(destination_id)
    origin_id_list = [x for _,x in sorted(zip(demand_start_time_list,origin_id_list))]
    destination_id_list = [x for _,x in sorted(zip(demand_start_time_list,destination_id_list))]
    demand_start_time_list.sort()
    datetime_list = [datetime.fromtimestamp(i).strftime('%Y-%m-%d %H:%M:%S') for i in demand_start_time_list]
    data = {'demand_start_time':demand_start_time_list,
            'origin_id': origin_id_list,
            'destination_id': destination_id_list,
            'datetime':datetime_list}
    return data