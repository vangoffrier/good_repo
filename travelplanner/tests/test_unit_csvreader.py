"""
Unit test of csv reader functions read_passengers and read_route in tpools.py
"""


from travelplanner.tptools import read_passengers, read_route
import yaml
import os
import pytest

xfail = pytest.mark.xfail

def test_csvreader():
	"""
	Extracts route and passenger data from sample "initial" model file and compares with known results.
	"""
	
	## Extract test routes and passenger lists
	full_path = os.path.split(os.path.realpath(__file__))
	modelname = 'initial'
	route = read_route(full_path[0] + '/inputdata/' + modelname + '_route.csv')
	passengers = read_passengers(full_path[0] + '/inputdata/' + modelname + '_pass.csv')
	
	comproute = [((2, 1), 'A'), ((3, 1), ''), ((4, 1), ''), ((5, 1), ''), \
				 ((6, 1), 'B'), ((7, 1), ''), ((7, 2), ''), ((8, 2), ''), \
				 ((9, 2), ''), ((10, 2), ''), ((11, 2), 'C'), ((11, 1), ''), \
				 ((12, 1), ''), ((13, 1), ''), ((14, 1), ''), ((14, 2), 'D'), \
				 ((14, 3), ''), ((14, 4), ''), ((13, 4), ''), ((12, 4), ''), \
				 ((11, 4), ''), ((10, 4), ''), ((9, 4), ''), ((9, 5), 'E'), \
				 ((9, 6), ''), ((10, 6), ''), ((11, 6), 'F'), ((12, 6), ''), \
				 ((13, 6), ''), ((14, 6), ''), ((15, 6), ''), ((16, 6), 'G')]
				 
	comppassengers = [((0, 2), (8, 1), 15), ((0, 0), (6, 2), 12), \
					  ((5, 2), (15, 4), 16), ((4, 5), (9, 7), 20)]

	assert route == comproute
	assert passengers == comppassengers


@xfail
def testneg_csvreader():
	"""
	Extracts route and passenger data from wrong files and checks for expected failure.
	"""
	
	## Extract test routes and passenger lists
	full_path = os.path.split(os.path.realpath(__file__))        
	modelname = 'initial'
	route = read_route(full_path[0] + '/inputdata/' + modelname + '_pass.csv')
	passengers = read_passengers(full_path[0] + '/inputdata/' + modelname + '_route.csv')
	
	comproute = [((2, 1), 'A'), ((3, 1), ''), ((4, 1), ''), ((5, 1), ''), \
				 ((6, 1), 'B'), ((7, 2), ''), ((8, 2), ''), ((9, 2), ''), \
				 ((10, 2), ''), ((11, 2), 'C'), ((11, 1), ''), ((12, 1), ''), \
				 ((13, 1), ''), ((14, 1), ''), ((14, 2), 'D'), ((14, 3), ''), \
				 ((14, 4), ''), ((13, 4), ''), ((12, 4), ''), ((11, 4), ''), \
				 ((10, 4), ''), ((9, 4), ''), ((9, 5), 'E'), ((9, 6), ''), \
				 ((10, 6), ''), ((11, 6), 'F'), ((12, 6), ''), ((13, 6), ''), \
				 ((14, 6), ''), ((15, 6), ''), ((16, 6), 'G')]
				 
	comppassengers = [((0, 2), (8, 1), 15), ((0, 0), (6, 2), 12), \
					  ((5, 2), (15, 4), 16), ((4, 5), (9, 7), 20)]


if __name__== "__main__":
	test_csvreader()
	testneg_csvreader()

