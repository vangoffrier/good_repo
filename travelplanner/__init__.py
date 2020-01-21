import math
import numpy as np
import matplotlib.pyplot as plt
import csv


class Passenger:
	'''
	Holds route and speed information about an individual passenger.
	'''
	def __init__(self, start, end, speed):
		'''
		Collects individual passenger data and instantiates Passenger class.
		'''
		assert (type(start) == tuple), "Input error, improper start coordinate."
		assert (type(end) == tuple), "Input error, improper end coordinate."
		assert (type(speed) == int or type(speed) == float), "Input error, improper speed."
		self.startpt = start
		self.endpt = end
		self.speed = speed

	def walk_time(self):
		'''
		Calculates walking time for passenger between start and end point at their given speed.
		'''
		dist = math.sqrt((self.endpt[0] - self.startpt[0])**2 + (self.endpt[1] - self.startpt[1])**2)
		return dist * self.speed

		    
class Route:
	'''
	Holds grid-path of bus journey, providing tools for representation of the route in timetable and chain-code
	forms.
	'''
	def __init__(self, filen,  bus_speed=10):
		'''
		Constructs route from CSV file and instantiates Route class.
		'''
		assert (type(bus_speed) == int or type(bus_speed) == float), "Input error, improper bus speed."
		assert (bus_speed>=0), "Input error, negative bus speed."
		self.bus_speed = bus_speed
		with open(filen) as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			self.route = []
			for row in csv_reader:
				assert (len(row) == 3), "Input error, improper csv dimensions."
				thisstep = ((int(row[0]),int(row[1])), row[2].strip())
				self.route.append(thisstep)
		self.cc = self.generate_cc()
		for elem in self.cc[1]:
			assert(int(elem)%2 == 0), "Improper input, diagonal movement detected."

	def plot_map(self, imgname=0):
		'''
		Displays route and stops on a grid for visualisation purposes.
		'''
		max_x = max([n[0][0] for n in self.route]) + 5 # adds padding
		max_y = max([n[0][1] for n in self.route]) + 5
		grid = np.zeros((max_y, max_x))
		for coordstop,stop in self.route:
			grid[coordstop[1], coordstop[0]] = 1
			if stop:
				grid[coordstop[1], coordstop[0]] += 1
		fig, ax = plt.subplots(1, 1)
		ax.pcolor(grid)
		ax.invert_yaxis()
		ax.set_aspect('equal', 'datalim')
		#plt.show(block=False)
		if imgname:
			plt.savefig(imgname + '.png')
		plt.close()
        
	def timetable(self):
		'''
		Generates a timetable for a route as minutes from its first stop.
		'''
		time = 0
		stops = {}
		for step in self.route:
			if step[1]:
				stops[step[1]] = time
			time += self.bus_speed
		return stops
    
	def generate_cc(self):
		'''
		Converts a set of route into a Freeman chain code, returning tuple (startpt, chaincode)
		3   2   1
		  ` | `
		4 - C - 0
		  ` | `
		5   6   7
		'''
		start = self.route[0][:2]
		cc = []
		freeman_cc2coord = {0: (1, 0),
							1: (1, -1),
							2: (0, -1),
							3: (-1, -1),
							4: (-1, 0),
							5: (-1, 1),
							6: (0, 1),
							7: (1, 1)}
		freeman_coord2cc = {val: key for key,val in freeman_cc2coord.items()}
		for b, a in zip(self.route[1:], self.route):
			x_step = b[0][0] - a[0][0]
			y_step = b[0][1] - a[0][1]
			cc.append(str(freeman_coord2cc[(x_step, y_step)]))
		return start, ''.join(cc)
		
		
class Journey:
	'''
	Holds route of bus journey and collection of passengers on that journey, providing tools for analysing the
	journey of each individual passenger and of the busload as a whole.
	'''
	def __init__(self, myroute, mypasslist=[], passfname=0):
		'''
		Collects route and passenger information and instantiates Journey class. If filename for passlist is provided, 			instantiates with that information superceding explicit mypasslist input.
		'''
		self.routeobj = myroute
			
		if passfname:
			# Extract passenger data from file according to perline format:
			# origin_x, origin_y, destination_x, destination_y, walkspeed
			
			with open(passfname) as csv_file:
				csv_reader = csv.reader(csv_file, delimiter=',')
				self.passlist = []
				for row in csv_reader:
					assert (len(row) == 5), "Input error, improper passlist csv dimensions."
					thispass = Passenger((int(row[0]),int(row[1])), (int(row[2]),int(row[3])), int(row[4]))
					self.passlist.append(thispass)
		else:
			self.passlist = mypasslist
		
	def trip(self, passenger_id):
		'''
		Calculates passenger's walking distance to the closest starting and ending stops,
		as an ordered pair.
		'''
		stops = [value for value in self.routeobj.route if value[1]]	# calculate closer stops
		
		passenger = self.passlist[passenger_id]
		
		## to start
		distances = [(math.sqrt((coordstop[0] - passenger.startpt[0])**2 +
		(coordstop[1] - passenger.startpt[1])**2), stop) for coordstop,stop in stops]
		closer_start = min(distances)
		
		## to end
		distances = [(math.sqrt((coordstop[0] - passenger.endpt[0])**2 +
		(coordstop[1] - passenger.endpt[1])**2), stop) for coordstop,stop in stops]
		closer_end = min(distances)
		
		return (closer_start, closer_end)
		
	def trip_time(self, passenger_id):
		'''
		Calculates passenger's total travel time and returns as a single value.
		'''
		passenger = self.passlist[passenger_id]
		
		walk_distance_stops = self.trip(passenger_id)
		bus_times = self.routeobj.timetable()
		bus_travel = abs(bus_times[walk_distance_stops[1][1]] - \
					 bus_times[walk_distance_stops[0][1]])
		walk_travel = walk_distance_stops[0][0] * passenger.speed + \
					  walk_distance_stops[1][0] * passenger.speed
		return bus_travel + walk_travel
		
	def travel_time(self, passenger_id):
		'''
		Calculates passenger's optimal travel time and returns as a dictionary of the form
		{'bus': bustime, 'walk': walktime}.
		'''
		stops = [value for value in self.routeobj.route if value[1]]	# calculate closer stops
		passenger = self.passlist[passenger_id]
		
		## to start
		distances = [math.sqrt((coordstop[0] - passenger.startpt[0])**2 +
		(coordstop[1] - passenger.startpt[1])**2) for coordstop,stop in stops]
		minstartdist = min(distances)
		closer_starts = [stops[i] for i, x in enumerate(distances) if x == minstartdist]
		
		## to end
		distances = [math.sqrt((coordstop[0] - passenger.endpt[0])**2 +
		(coordstop[1] - passenger.endpt[1])**2) for coordstop,stop in stops]
		minenddist = min(distances)
		closer_ends = [stops[i] for i, x in enumerate(distances) if x == minenddist]
		
		best_travel = (0,passenger.walk_time())
		
		for cand_start in closer_starts:
			for cand_end in closer_ends:
				bus_times = self.routeobj.timetable()
				bus_travel = bus_times[cand_end[1]] - bus_times[cand_start[1]]
				if bus_travel<=0: break		# eliminate case where later stop comes before earlier stop
				walk_travel = minstartdist * passenger.speed + minenddist * passenger.speed
				cand_travel = (bus_travel,walk_travel)
				if sum(cand_travel) < sum(best_travel): best_travel = cand_travel
		
		return {'bus': best_travel[0], 'walk': best_travel[1]}
		
	def print_time_stats(self):
		'''
		Prints walking time and bus time statistics, averaging over all passengers.
		'''
		total_bustime = 0
		total_walktime = 0
		for passenger_id in range(len(self.passlist)):
			total_bustime += self.travel_time(passenger_id)['bus']
			total_walktime += self.travel_time(passenger_id)['walk']
			
		print("Average time on bus: " + str(int(total_bustime/len(self.passlist))) + " min")
		print("Average walking time: " + str(int(total_walktime/len(self.passlist))) + " min\n")
				
	def plot_bus_load(self, imgname=0):
		'''
		Plots and displays graph of number of passengers on bus, as it travels along its route.
		'''
		stops = {step[1]:0 for step in self.routeobj.route if step[1]}
		for passenger_id in range(len(self.passlist)):
			ptrip = self.trip(passenger_id)
			stops[ptrip[0][1]] += 1
			stops[ptrip[1][1]] -= 1
		for i, stop in enumerate(stops):
			if i > 0:
				stops[stop] += stops[prev]
			prev = stop
		fig, ax = plt.subplots()
		ax.step(range(len(stops)), list(stops.values()), where='post')
		ax.set_xticks(range(len(stops)))
		ax.set_xticklabels(list(stops.keys()))
		#plt.show(block=False)
		if imgname:
			plt.savefig(imgname + '.png')
		plt.close()
		
		
