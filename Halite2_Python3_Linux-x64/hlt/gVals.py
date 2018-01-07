import csv

def parseGVals():
	parameters = open('hlt/parameters.csv', 'r')
	parameterReader = csv.reader(parameters)
	for row in parameterReader:
		#Gu, Ge, Gf, Ges, Gfs
		parameterDict = {"Gu":float(row[0]),"Ge":float(row[1]),"Gf":float(row[2]),"Ges":float(row[3]),"Gfs":float(row[4])}
	parameters.close()
	return parameterDict

def writeGVals(parameterDict):
	parameters = open('hlt/parameters.csv', 'w')
	parameterWriter = csv.writer(parameters)
	parameterVals = [parameterDict["Gu"],parameterDict["Ge"],parameterDict["Gf"],parameterDict["Ges"],parameterDict["Gfs"]]
	parameterWriter.writerow(parameterVals)
	parameters.close()

def appendGVals(parameterDict):
	parameters = open('hlt/parameters.csv', 'a')
	parameterWriter = csv.writer(parameters)
	parameterVals = [parameterDict["Gu"],parameterDict["Ge"],parameterDict["Gf"],parameterDict["Ges"],parameterDict["Gfs"]]
	parameterWriter.writerow(parameterVals)
	parameters.close()

def appendControlVals(parameterDict):
	parameters = open('../controlBot/hlt/parameters.csv', 'a')
	parameterWriter = csv.writer(parameters)
	parameterVals = [parameterDict["Gu"],parameterDict["Ge"],parameterDict["Gf"],parameterDict["Ges"],parameterDict["Gfs"]]
	parameterWriter.writerow(parameterVals)
	parameters.close()

# parameterDict = {"Gu":1,"Ge":2,"Gf":3,"Ges":4,"Gfs":5}
# appendGVals(parameterDict)