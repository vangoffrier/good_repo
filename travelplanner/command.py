"""
Sets up argument parsing for command entry into package. Should allow command of the form:
bussimula routefile passfile --speed 5 [--saveplots]
"""

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from travelplanner import Route, Passenger, Journey

def tp_interface(routefile, passfile, speed, saveplots):
	"""Starting route provided in Section 1 of the project assignment.

	- Defines sample route and passenger details.
	- Plots route of bus and number of passenger on bus (if saveplot == True)
	- Returns start point of route, and chain code translating to route.
	"""
	
	## Extract test routes and passenger lists, generate objects
	routeobj = Route(routefile, bus_speed = speed)
	journeyobj = Journey(routeobj, passfname = passfile)
				 
	print("Stops: minutes from start\n", journeyobj.routeobj.timetable())
	for pid in range(len(journeyobj.passlist)):
		print(f"Trip for passenger: {pid}")
		start, end = journeyobj.trip(pid)
		total_time = journeyobj.trip_time(pid)
		print((f" Walk {start[0]:3.2f} units to stop {start[1]}, \n"
			   f" get on the bus and alite at stop {end[1]} and \n"
			   f" walk {end[0]:3.2f} units to your destination."))
		print(f" Total time of travel: {total_time:03.2f} minutes")
			
	if saveplots:
		journeyobj.routeobj.plot_map("map")			# Plots route of bus
		journeyobj.plot_bus_load("load")			# Plots num. pass. on bus

def process():
    parser = ArgumentParser(description="Test description.",
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('routefile', nargs='?', default="",
                        help="Input CSV file with route of bus.")
    parser.add_argument('passfile', nargs='?', default="",
                        help="Input CSV file with passenger details.")
    parser.add_argument('--speed', default=10,
                        help="Speed of the bus.")
    parser.add_argument('--saveplots', help="Save plots map.png and load.png to file.",
    					action="store_true")
    args = parser.parse_args()

	## Run travelplanner simulation according to arguments
    tp_interface(args.routefile, args.passfile, int(args.speed), args.saveplots)
    
