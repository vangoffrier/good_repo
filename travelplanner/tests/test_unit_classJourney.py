"""
Unit tests of Journey class in tpclasses.py
"""


from travelplanner import Route, Passenger, Journey
import yaml
import os
import pytest

xfail = pytest.mark.xfail

def test_journey_init():
	"""
	Extracts route and passenger data from file and confirms correct processing.
	"""
	
	## Extract test routes and passenger lists  
	full_path = os.path.split(os.path.realpath(__file__))    
	modelname = 'initial'
	routeobj = Route(full_path[0] + '/inputdata/' + modelname + '_route.csv')
	journeyobj = Journey(routeobj, passfname=full_path[0] + '/inputdata/' + modelname + '_pass.csv')
	
	comproute = [((2, 1), 'A'), ((3, 1), ''), ((4, 1), ''), ((5, 1), ''), \
				 ((6, 1), 'B'), ((7, 1), ''), ((7, 2), ''), ((8, 2), ''), \
				 ((9, 2), ''), ((10, 2), ''), ((11, 2), 'C'), ((11, 1), ''), \
				 ((12, 1), ''), ((13, 1), ''), ((14, 1), ''), ((14, 2), 'D'), \
				 ((14, 3), ''), ((14, 4), ''), ((13, 4), ''), ((12, 4), ''), \
				 ((11, 4), ''), ((10, 4), ''), ((9, 4), ''), ((9, 5), 'E'), \
				 ((9, 6), ''), ((10, 6), ''), ((11, 6), 'F'), ((12, 6), ''), \
				 ((13, 6), ''), ((14, 6), ''), ((15, 6), ''), ((16, 6), 'G')]
				 
	comppassinfo = [((0, 2), (8, 1), 15), ((0, 0), (6, 2), 12), ((5, 2), (15, 4), 16), ((4, 5), (9, 7), 20)]


	assert journeyobj.routeobj.route == comproute
	
	passlist = journeyobj.passlist
	passinfo = []
	for passenger in passlist:
		passinfo.append( (passenger.startpt, passenger.endpt, passenger.speed) )
	assert passinfo == comppassinfo
	
def test_journey_traveltime():
	"""
	Calculates optimal travel times on model file "rand6", which has multiple cases of passenger destinations
	equidistant between two stops.
	"""
	
	## Extract test routes and passenger lists  
	full_path = os.path.split(os.path.realpath(__file__))    
	modelname = 'rand6'
	routeobj = Route(full_path[0] + '/inputdata/' + modelname + '_route.csv',bus_speed=2)
	journeyobj = Journey(routeobj, passfname=full_path[0] + '/inputdata/' + modelname + '_pass.csv')
	
	traveltimes = []
	for i in range(len(journeyobj.passlist)):
		traveltimes.append(journeyobj.travel_time(i))
	
	comptraveltimes = [{'bus': 34, 'walk': 906.2257748298549}, {'bus': 0, 'walk': 30.0},
					   {'bus': 32, 'walk': 102.46211251235322}, {'bus': 0, 'walk': 432.9260906898544},
					   {'bus': 0, 'walk': 0.0}, {'bus': 0, 'walk': 132.81566172707193},
					   {'bus': 0, 'walk': 216.0}, {'bus': 0, 'walk': 373.2264728017025},
					   {'bus': 0, 'walk': 570.087712549569}, {'bus': 0, 'walk': 202.82997806044352}]
					   
	assert traveltimes == comptraveltimes

	
def test_journey_printtraveltime():
	"""
	Calculates optimal travel times for all passengers on journey, and returns average bus and walking
	times in the specified format.
	"""
	
	## Extract test routes and passenger lists  
	full_path = os.path.split(os.path.realpath(__file__))    
	modelname = 'rand4'
	routeobj = Route(full_path[0] + '/inputdata/' + modelname + '_route.csv',bus_speed=2)
	journeyobj = Journey(routeobj, passfname=full_path[0] + '/inputdata/' + modelname + '_pass.csv')
	
	## Pull stdout to wrapper where we can check its content
	import sys
	import io
	old_stdout = sys.stdout
	sys.stdout = buffer = io.StringIO()

	journeyobj.print_time_stats()

	sys.stdout = old_stdout 
	whatWasPrinted = buffer.getvalue()
	desiredPrint = "Average time on bus: 11 min\nAverage walking time: 184 min\n\n"
	assert whatWasPrinted == desiredPrint

	

@xfail
def testneg_journey_init():
	"""
	Attempts to extract route and passenger data from same file and checks for error.
	"""
	
	## Extract test routes and passenger lists  
	full_path = os.path.split(os.path.realpath(__file__))    
	modelname = 'initial'
	routeobj = Route(full_path[0] + '/inputdata/' + modelname + '_route.csv')
	journeyobj = Journey(routeobj, passfname=full_path[0] + '/inputdata/' + modelname + '_route.csv')
	

if __name__== "__main__":
	test_journey_init()
	test_journey_traveltime()
	test_journey_printtraveltime()
	testneg_journey_init()

