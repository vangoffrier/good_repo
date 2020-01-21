"""
Unit tests of Route class in tpclasses.py
"""


from travelplanner import Route, Passenger, Journey
import yaml
import os
import pytest

xfail = pytest.mark.xfail

def test_route_init():
	"""
	Extracts route data from sample "initial" model file and compares with known results.
	"""
	
	## Extract test route
	full_path = os.path.split(os.path.realpath(__file__))
	modelname = 'initial'
	routeobj = Route(full_path[0] + '/inputdata/' + modelname + '_route.csv')
	
	comproute = [((2, 1), 'A'), ((3, 1), ''), ((4, 1), ''), ((5, 1), ''), \
				 ((6, 1), 'B'), ((7, 1), ''), ((7, 2), ''), ((8, 2), ''), \
				 ((9, 2), ''), ((10, 2), ''), ((11, 2), 'C'), ((11, 1), ''), \
				 ((12, 1), ''), ((13, 1), ''), ((14, 1), ''), ((14, 2), 'D'), \
				 ((14, 3), ''), ((14, 4), ''), ((13, 4), ''), ((12, 4), ''), \
				 ((11, 4), ''), ((10, 4), ''), ((9, 4), ''), ((9, 5), 'E'), \
				 ((9, 6), ''), ((10, 6), ''), ((11, 6), 'F'), ((12, 6), ''), \
				 ((13, 6), ''), ((14, 6), ''), ((15, 6), ''), ((16, 6), 'G')]

	assert routeobj.route == comproute
	
def test_route_timetable():
	"""
	Generates route timetable and compares with known result.
	"""
	
	## Extract test route
	full_path = os.path.split(os.path.realpath(__file__))
	modelname = 'initial'
	routeobj = Route(full_path[0] + '/inputdata/' + modelname + '_route.csv')
	
	## Calculate timetable
	testtt = routeobj.timetable()
	comptt = {'A': 0, 'B': 40, 'C': 100, 'D': 150, 'E': 230, 'F': 260, 'G': 310}
	assert testtt == comptt
	
def test_route_timetable_halfspeed():
	"""
	Generates route timetable with halved speed and compares with known result.
	"""
	
	## Extract test route
	full_path = os.path.split(os.path.realpath(__file__))
	modelname = 'initial'
	routeobj = Route(full_path[0] + '/inputdata/' + modelname + '_route.csv', bus_speed=5)
	
	## Calculate timetable
	testtt = routeobj.timetable()
	comptt = {'A': 0, 'B': 20, 'C': 50, 'D': 75, 'E': 115, 'F': 130, 'G': 155}
	assert testtt == comptt
	
def test_route_cc():
	"""
	Generates route Freeman chain code (and initial point) and compares with known result.
	"""
	
	## Extract test route
	full_path = os.path.split(os.path.realpath(__file__))
	with open(full_path[0] + '/fixtures.yml') as file:
		testdata = yaml.load(file)
        
	modelname = 'initial'
	routeobj = Route(full_path[0] + '/inputdata/' + modelname + '_route.csv')
	
	## Calculate Freeman chain code
	testcc = routeobj.generate_cc()
	print(testcc)
	compcc = (((2, 1), 'A'), '0000060000200066644444660000000')
	assert testcc == compcc


@xfail
def testneg_route_init():
	"""
	Attempts to extract route data from an int filename and checks for expected failure.
	"""
	
	## Extract test routes and passenger lists
	full_path = os.path.split(os.path.realpath(__file__))        
	modelname = 'initial'
	routeobj = Route(420)
	
@xfail
def testneg_route_speed():
	"""
	Attempts to construct a route with negative bus speed and throws an error.
	"""
	
	## Extract test routes and passenger lists
	full_path = os.path.split(os.path.realpath(__file__))        
	modelname = 'initial'
	routeobj = Route(full_path[0] + '/inputdata/' + modelname + '_route.csv','abc')
	
@xfail
def testneg_route_diag():
	"""
	Attempts to extract a route with diagonal movement and throws an error.
	"""
	
	## Extract test routes and passenger lists
	full_path = os.path.split(os.path.realpath(__file__))        
	modelname = 'diag'
	routeobj = Route(full_path[0] + '/inputdata/' + modelname + '_route.csv','abc')
	


if __name__== "__main__":
	test_route_init()
	test_route_timetable()
	test_route_timetable_halfspeed()
	test_route_cc()
	testneg_route_init()
	testneg_route_speed()

