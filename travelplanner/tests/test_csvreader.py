"""
Integrated test of csv reader structure and travelplanner functionality, using two specified and six random model datasets.
"""


from travelplanner.tptools import timetable, passenger_trip, passenger_trip_time, plot_map, plot_bus_load, read_passengers, read_route
import yaml
import os

def test_models():
	"""Starting route provided in Section 1 of the project assignment.

	- Defines sample route and passenger details.
	- Plots route of bus and number of passengers on bus
	"""
	
	## Extract test routes and passenger lists
	full_path = os.path.split(os.path.realpath(__file__))
	with open(full_path[0] + '/fixtures.yml') as file:
		testdata = yaml.load(file)
        
	for modelname in testdata.get('models'):
		route = read_route(full_path[0] + '/inputdata/' + modelname + '_route.csv')
		passengers = read_passengers(full_path[0] + '/inputdata/' + modelname + '_pass.csv')
		
		print(passengers)
    
				 
		print(" Stops: minutes from start\n", timetable(route))
		pid = 0
		for passenger in passengers:
			pid += 1
			print(f"Trip for passenger: {pid}")
			start, end = passenger_trip(passenger, route)
			total_time = passenger_trip_time(passenger, route)
			print((f" Walk {start[0]:3.2f} units to stop {start[1]}, \n"
				   f" get on the bus and alite at stop {end[1]} and \n"
				   f" walk {end[0]:3.2f} units to your destination."))
			print(f" Total time of travel: {total_time:03.2f} minutes")
			
		plot_map(route, modelname)					# Plots route of bus
		plot_bus_load(route, passengers, modelname)	# Plots num. pass. on bus
	

if __name__== "__main__":
	test_models()

