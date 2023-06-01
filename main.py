from create_objects import create_vertiport, create_aircrafts
from create_schedule import create_schedule
from run_simulation import run_simulation
import pickle as pk

file_name = 'vertiport_info'
landing_occupation_time = 180 #seconds
takeoff_occupation_time = 120 #seconds
holding_duration = 600 #seconds
start_time = 1668832200
end_time = 1668832200 + 3600 # 1 hour of operation will be simulated (end_time = start_time + 3600)
time_on_station_step = 10 # increment in time on station step in seconds
out_data = {}
msg_list = []
aircraft_step = 2 # aircraft increment step
# vertiport capacities
for capacity in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]:
    out_data[capacity] = {}
    for i in range(30):
        aircraft_number = (i+1) * aircraft_step
        if aircraft_number <= capacity:
            continue
        time_on_station = 0
        out_data[capacity][aircraft_number] = None
        msg_list = []
        while not msg_list and time_on_station < 3600:
            # creating vertiport
            vertiports, last_id = create_vertiport(file_name)
            vertiport = vertiports[0]
            vertiport.capacity = capacity
            # creating aircraft scehdule data
            aircraft_schedule_data = create_schedule(aircraft_number, start_time, end_time)
            # creating aircrafts
            aircrafts, last_id = create_aircrafts(aircraft_schedule_data, last_id)
            # running simulation
            vertiport, aircrafts, msg_list, current_epoch = run_simulation(vertiport, aircrafts, 
                                                                           landing_occupation_time, 
                                                                           takeoff_occupation_time, 
                                                                           time_on_station,
                                                                           holding_duration, 
                                                                           start_time, end_time + 3600)
            if not msg_list:
                # if there is no error, we will raise time on station value.
                out_data[capacity][aircraft_number] = time_on_station
                time_on_station += time_on_station_step
                
        pk.dump(out_data,open('out_data.p','wb'))
        # Data will be in this form: 
        # out_data = {vertiport_capacity:{'number_of_arriving_aircraft_per_hour':max_time_on_station}}