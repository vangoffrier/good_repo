import math
import numpy as np
import matplotlib.pyplot as plt
import csv

def timetable(route):
	'''
	Generates a timetable for a route as minutes from its first stop.
	'''
	time = 0
	stops = {}
	for step in route:
		if step[1]:
			stops[step[1]] = time
		time += 10
	return stops
	
	
def passenger_trip(passenger, route):
	'''
	Calculates passenger's walking distance to the closest starting and ending stops,
	as an ordered pair.
	'''
	start, end, pace = passenger
	stops = [value for value in route if value[1]]	# calculate closer stops
	
	## to start
	distances = [(math.sqrt((coordstop[0] - start[0])**2 +
	(coordstop[1] - start[1])**2), stop) for coordstop,stop in stops]
	closer_start = min(distances)
	
	## to end
	distances = [(math.sqrt((coordstop[0] - end[0])**2 +
	(coordstop[1] - end[1])**2), stop) for coordstop,stop in stops]
	closer_end = min(distances)
	
	return (closer_start, closer_end)
	

def passenger_trip_time(passenger, route):
	'''
	Calculates the total travel time for a particular passenger.
	'''
	walk_distance_stops = passenger_trip(passenger, route)
	bus_times = timetable(route)
	bus_travel = bus_times[walk_distance_stops[1][1]] - \
				 bus_times[walk_distance_stops[0][1]]
	walk_travel = walk_distance_stops[0][0] * passenger[2] + \
				  walk_distance_stops[1][0] * passenger[2]
	return bus_travel + walk_travel


def plot_map(route, imgname):
	'''
	Displays route and stops on a grid for visualisation purposes.
	'''
	max_x = max([n[0][0] for n in route]) + 5 # adds padding
	max_y = max([n[0][1] for n in route]) + 5
	grid = np.zeros((max_y, max_x))
	for coordstop,stop in route:
		grid[coordstop[1], coordstop[0]] = 1
		if stop:
			grid[coordstop[1], coordstop[0]] += 1
	fig, ax = plt.subplots(1, 1)
	ax.pcolor(grid)
	ax.invert_yaxis()
	ax.set_aspect('equal', 'datalim')
	#plt.show(block=False)
	plt.savefig(imgname + '_route.png')
	plt.close()


def plot_bus_load(route, passengers, imgname):
	'''
	Displays number of people on the bus between stops.
	'''
	stops = {step[1]:0 for step in route if step[1]}
	for passenger in passengers:
		trip = passenger_trip(passenger, route)
		stops[trip[0][1]] += 1
		stops[trip[1][1]] -= 1
	for i, stop in enumerate(stops):
		if i > 0:
			stops[stop] += stops[prev]
		prev = stop
	fig, ax = plt.subplots()
	ax.step(range(len(stops)), list(stops.values()), where='post')
	ax.set_xticks(range(len(stops)))
	ax.set_xticklabels(list(stops.keys()))
	#plt.show(block=False)
	plt.savefig(imgname + '_busload.png')
	plt.close()
	
	
def read_passengers(filen):
	'''
	Extract passenger data from file according to perline format:
	origin_x, origin_y, destination_x, destination_y, walkspeed
	'''
	with open(filen) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		passlist = []
		for row in csv_reader:
			assert (len(row) == 5), "Input error, improper csv dimensions."
			thispass = ((int(row[0]),int(row[1])), (int(row[2]),int(row[3])), int(row[4]))
			passlist.append(thispass)
	return passlist
	
def read_route(filen):
	'''
	Extract route data from file according to perline format:
	coord_x, coord_y, stop
	'''
	with open(filen) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		route = []
		for row in csv_reader:
			assert (len(row) == 3), "Input error, improper csv dimensions."
			thisstep = ((int(row[0]),int(row[1])), row[2].strip())
			route.append(thisstep)
	return route
	
	
	
	
