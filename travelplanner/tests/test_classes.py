"""
Integrated test of initial class structure as outlined in 2.2, including Route, Passenger, and Journey classes.
"""


from travelplanner import Route, Passenger, Journey
import yaml
import os

def test_classes():
	"""Starting example provided in Section 2.2 of the project assignment.

	- Defines sample route and passenger details.
	- Plots route of bus and number of passenger on bus
	- Returns start point of route, and chain code translating to route.
	"""
	
	## Extract test routes and passenger lists
	full_path = os.path.split(os.path.realpath(__file__))
	with open(full_path[0] + '/fixtures.yml') as file:
		testdata = yaml.load(file)
        
	for modelname in testdata.get('models'):
		route = Route(full_path[0] + '/inputdata/' + modelname + '_route.csv')
		route.plot_map(imgname = modelname + '_route')
		startpt, cc = route.generate_cc()
		print("Start point: " + str(startpt))
		print("Chain code: " + str(cc) + '\n')
		
		# Manual input e.g.: john = Passenger(start=(0,2), end=(8,1), speed=15)
		journey = Journey(route, passfname=full_path[0] + '/inputdata/' + modelname + '_pass.csv')
		journey.plot_bus_load(imgname = modelname + '_passplot')
		
	

if __name__== "__main__":
	test_classes()

