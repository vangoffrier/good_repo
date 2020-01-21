"""
Doctest for generate_cc function of Route class in tpclasses.py file.
"""


from travelplanner import Route, Passenger, Journey
import yaml
import os
	
def test_route_cc_fromfile(modelname):
	"""
	Generates route Freeman chain code (and initial point) and compares with known result.
	
	An appropriately defined route has only even chain code entries.
    >>> test_route_cc_fromfile('rand1')
    (((5, 10), 'A'), '000000000006660006646600222')
    
    An inappropriately defined route mdray have an odd chain code entry, representing diagonal movement.
    >>> test_route_cc_fromfile('diag')
    Traceback (most recent call last):
    ...
    AssertionError: Improper input, diagonal movement detected.
	"""
	
	## Extract test route
	full_path = os.path.split(os.path.realpath(__file__))
    
    ## Construct Route object
	routeobj = Route(full_path[0] + '/inputdata/' + modelname + '_route.csv')
	
	## Calculate Freeman chain codefor Route
	testcc = routeobj.generate_cc()
	return testcc



if __name__== "__main__":
	import doctest
	doctest.testmod()

