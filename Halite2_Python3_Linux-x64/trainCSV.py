import subprocess
import sys
import json
import time
import numpy as np
import hlt
import random
import math
#json loads the output from the subprocess

if sys.argv[1] == "-h":
	print("python3 trainCSV.py -duration -amount (how many halite runs 2 and 4) -adjust(float on how much to change for neighbor) -startingTemp -tempDecrease")
	exit()

duration = int(sys.argv[1])
amount = int(sys.argv[2])
adjust = float(sys.argv[3])
print("Running training for {} seconds".format(duration)) 

haliteTwo = ["./halite", "-d", "240 160", "-t", "python3 MyBot.py", "python3 ../controlBot/MyBot.py", "-q", "-r"]
# haliteTwo = "./halite -d '240 160' 'python3 MyBot.py' 'python3 ../controlBot/MyBot.py' -q -r -t"
haliteFour = ["./halite", "-d", "288 192", "-t", "python3 MyBot.py", "python3 ../controlBot/MyBot.py", "python3 ../controlBot/MyBot.py", "python3 ../controlBot/MyBot.py", "-q", "-r"]
# haliteFour = "./halite -d '288 192' 'python3 MyBot.py' 'python3 ../controlBot/MyBot.py' 'python3 ../controlBot/MyBot.py' 'python3 ../controlBot/MyBot.py' -q -r -t"

def runTwo(num):
	#runs num trials and returns winrate  
	totalWin = 0
	# processList = [subprocess.Popen(haliteTwo, stdout = subprocess.PIPE) for i in range(num)]
	# i = 1
	# for process in processList:
	# 	process.wait()
	# 	output, __ = process.communicate()
	# 	process.kill()
	# 	result = json.loads(output.decode("utf-8"))
	# 	rank = result["stats"]["0"]["rank"]
	# 	if rank == 1:
	# 		totalWin += 1
	# 	print("runTwo: {} / {}".format(i, num))
	# 	i += 1
	for i in range(num):
		result = json.loads(subprocess.check_output(haliteTwo).decode("utf-8"))
		rank = result["stats"]["0"]["rank"]
		if rank == 1:
			totalWin += 1
		print("runTwo: {} / {}".format(i+1, num))
	print("winrate = {}".format(float(totalWin / num)))
	return float(totalWin / num)

def runFour(num):
	totalWin = 0
	# processList = [subprocess.Popen(haliteFour, stdout = subprocess.PIPE) for i in range(num)]
	# i = 1
	# for process in processList:
	# 	process.wait()
	# 	output, __ = process.communicate()
	# 	process.kill()
	# 	result = json.loads(output.decode("utf-8"))
	# 	rank = result["stats"]["0"]["rank"]
	# 	if rank == 1:
	# 		totalWin += 1
	# 	print("runFour: {} / {}".format(i, num))
	# 	i += 1
	for i in range(num):
		result = json.loads(subprocess.check_output(haliteFour).decode("utf-8"))
		rank = result["stats"]["0"]["rank"]
		if rank == 1:
			totalWin += 1
		print("runFour: {} / {}".format(i+1, num))
	print("winrate = {}".format(float(totalWin / num)))
	return float(totalWin / num)

def getNeighbor(node):
	print("currNode: {}".format(node))
	choices = ["Gu", "Ge", "Gf", "Ges", "Gfs"]
	# choice = random.choice(choices)
	for choice in choices:
		node[choice] = round(random.expovariate(1.5),4)
	print("newNode: {}".format(node))
	return node

temperature = int(sys.argv[4])
tempDecrease = int(sys.argv[5])
i = 0
startTime = time.time()
# print("Running iteration {} with temperature {} and time {} / {}".format(i, temperature, time.time() - startTime, duration))
currNode = hlt.gVals.parseGVals()
# winrate = runTwo(amount)
# winrate2 = runFour(amount)
# currH = (winrate + winrate2) / 2
# currH = winrate
# print("Ran with winrate {}".format(currH))
i += 1
bestNode = hlt.gVals.parseGVals()
while (time.time() - startTime < duration and temperature > 0):
	print("Running iteration {} with temperature {} and time {} / {}".format(i, temperature, time.time() - startTime, duration))
	#do training
	#pick a single neighbor and write to CSV
	newNode = getNeighbor(currNode)
	hlt.gVals.appendGVals(newNode)


	winrate = runTwo(amount) # default to 50
	winrate2 = runFour(amount)
	# newH = (winrate + winrate2) / 2
	# newH = winrate
	# score = newH - 50
	# deltaH = newH - currH
	deltaH = ((winrate - 0.7) + ((winrate2 - 0.35)* 2))
	print("Ran with delta winrate {}".format(deltaH))
	if deltaH >= 0:
		currNode = newNode
		bestNode = newNode
		# currH = newH
		hlt.gVals.appendControlVals(newNode)
		print("Delta H > 0, accepted move")
	else: 
		randVal = random.random()
		threshold = math.exp(deltaH*20 / temperature)
		print("randval: {}, threshold: {}".format(randVal, threshold))
		if randVal < threshold:
			currNode = newNode
			# currH = newH
			#reduce temperature
			hlt.gVals.appendControlVals(newNode)
			temperature -= tempDecrease
			print("Accepted move due to probability")
		else:
			print("Didn't accept move due to probablity")
		#current = next with probablity e^(deltah/T) or loop
	i += 1
		
if temperature == 0:
	print("terminated simulated annealing bc of temperature")
else:
	print("terminated due to time")

print("Best node: {}".format(bestNode))
hlt.gVals.appendGVals(bestNode)
