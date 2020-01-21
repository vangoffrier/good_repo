"""
Prints contents of fixture_data.yaml in a readable way, for pre-testing purposes.
"""

import yaml


with open('fixture_data.yaml') as file:
	testdata = yaml.load(file)

print(testdata)
