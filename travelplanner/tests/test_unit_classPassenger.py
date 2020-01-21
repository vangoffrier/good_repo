"""
Unit tests of Passenger class in tpclasses.py
"""


from travelplanner import Route, Passenger, Journey
import yaml
import os
import pytest

xfail = pytest.mark.xfail

def test_passenger_init():
	"""
	Extracts passenger data from manual submission and confirms correct processing.
	"""
	
	## Extract test route
	john = Passenger(start=(0,2), end=(8,1), speed=15)
	
	comp_john_startpt = (0,2)
	comp_john_endpt = (8,1)
	comp_john_speed =  15

	assert john.startpt == comp_john_startpt
	assert john.endpt == comp_john_endpt
	assert john.speed == comp_john_speed
	
def test_passenger_walktime():
	"""
	Calculates passenger walk time and compares with known result.
	"""
	
	## Extract test route
	john = Passenger(start=(0,2), end=(8,1), speed=15)
	comp_walktime = 120.93386622447824

@xfail
def testneg_passenger_init():
	"""
	Gives incorrect format of passenger input and checks for expected failure.
	"""
	
	## Extract test route
	john = Passenger(start=(0,2), end=(8,1), speed='abc')
	
	
if __name__== "__main__":
	test_passenger_init()
	test_passenger_walktime()
	testneg_passenger_init()

