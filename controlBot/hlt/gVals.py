from . import entity, collision, game_map
import csv

def parseGVals():
	parameters = open('hlt/parameters.csv', 'r')
	parameterReader = csv.reader(parameters)
	for row in parameterReader:
		#Gu, Ge, Gf, Ges, Gfs
		parameterDict = {"Gu":float(row[0]),"Ge":float(row[1]),"Gf":float(row[2]),"Ges":float(row[3]),"Gfs":float(row[4])}
		continue
	parameters.close()
	return parameterDict