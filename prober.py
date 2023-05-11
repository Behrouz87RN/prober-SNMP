#!/usr/bin/python3

import sys, time, math
from easysnmp import *
from pip._vendor.requests.sessions import Session

# Parse command-line arguments
agentIP, agentPort, agentCommunity = sys.argv[1].split(':')
smplFrequency =  float(sys.argv[2])
smplCount = int(sys.argv[3])
smplTime = 1 / smplFrequency
# Initialize variables
objects, object_1, object_2, timer = [], [], [], ''

objects = ['1.3.6.1.2.1.1.3.0'] + [sys.argv[i] for i in range(4, len(sys.argv))]

#Set up SNMP session

session_args = {'hostname': agentIP, 'remote_port': agentPort, 'community': agentCommunity, 'version': 2, 'timeout': 1, 'retries': 3}
session = Session(**session_args)

#def print_values(value, diff, timer):
	#  if timer == str(t2):
		#print(round(value / diff), end="|")
	#  else:
		#print(t2, "|", round(value / diff), end="|")
		#  timer = str(t2)
	# except:
		# print(t2, "|", round(value / diff), end="|")
		# timer = str(t2)
#Define function for fetching SNMP values and calculating rates

def sid():
	global object_1, t1, t2
	outcome = session.get(objects)
	TimerSys= int(outcome[0].value)/100
	object_2 = []

	for th in range(1, len(outcome)):
		if outcome[th].value not in ('NOSUCHOBJECT', 'NOSUCHINSTANCE'):
			value = outcome[th].value
			snmp_type = outcome[th].snmp_type
# if the SNMP data is a counter, calculate the rate of change
			if snmp_type in ('COUNTER64', 'COUNTER32', 'COUNTER'):
				value = int(value)

			object_2.append(value)

			if count != 0 and len(object_1) > 0:
				if TimerSys > t1:
					if snmp_type in ('COUNTER', 'COUNTER32', 'COUNTER64'):
						oiddiff = int(object_2[th - 1]) - int(object_1[th - 1])
						time_diff = (TimerSys - t1)
						rate = int(oiddiff / time_diff)
						if rate < 0:
							if TimerSys > t1:
								if snmp_type == 'COUNTER32':
									oiddiff += (2 ** 32)
									#print_values(oiddiff, time_diff, t2)
									try:
										if timer==str(t2):
											#print(round(oiddiff/(time_diff)),end="|")
											print(oiddiff/(time_diff),end="|")
										else:
											print(round(t2),"|",round(oiddiff/(time_diff)), end="|");timer=str(t2)

									except:
										print(round(t2),"|", round(oiddiff/(time_diff)), end= "|");timer=str(t2)

								elif snmp_type == 'COUNTER64':
									oiddiff += (2 ** 64)
									#print_values(oiddiff, time_diff, t2)
									try:
										if timer==str(t2):
											#print(oiddiff/(time_diff))
											print(round(oiddiff/(time_diff)), end ="|")
										else:
											print(t2, "|", round(oiddiff/(time_diff)), end="|");timer=str(t2)

									except:
										#print(oiddiff/time_diff)
										print(t2,"|",round(oiddiff/(time_diff)),end= "|");timer=str(t2)
								#else:
									#break
							else:
								print("system was restarted ")
								break

						else:
							#print_values(rate, 1, t2)
							try:
								if timer==str(t2):
									print( round(rate) ,end= "|")
									#print("first")
								else:
									print(t2,"|", round(rate), end="|")
									timer=str(t2)
									#print("second")
							except:
								print(t2 ,"|", round(rate), end="|")
								timer=str(t2)
#handle non-responsive SNMP agents 
					elif outcome[th].snmp_type=='GAUGE':
						oiddiff = int(object_2[th-1]) - int(object_1[th-1])
						#if oiddiff>0: oiddiff="+"+str(oiddiff)
						try:
							if timer==str(t2):
								print(object_2[len(object_2)-1],"(",+oiddiff,")", end="|")
								#print("4")
							else:
								print(t2,"|",object_2[len(object_2)-1],"(",+oiddiff,")", end="|")
								timer=str(t2)
								#print("5")
						except:
							print(t2,"|",object_2[len(object_2)-1],"(",+oiddiff,")", end="|")
							timer=str(t2)
							#print("6")	
		
					#else:
						#break

				else:
					print("system was restarted ")
					break

	object_1 = object_2
	t1 = TimerSys

	#print("new time {}".format(t1))
if smplCount==-1:
	count = 0
	object_1 = []
	while True:
		t2 = time.time()
		sid()
		if count!=0:
			print(end="\n")
		ResponseTime = time.time()
		count = count+1
		if smplTime >= ResponseTime - t2:
			time.sleep((smplTime- ResponseTime + t2))
		else:
			#n=math.ceil((ResponseTime-t2)/smplTime)
			n=((ResponseTime-t2)/smplTime)
			print(n,"n",((n*smplTime)- ResponseTime + t2))
			time.sleep(((n*smplTime)- ResponseTime + t2))
else:
	object_1 = []
	a=smplCount
	for count in range(0,smplCount+1):
		t2 = time.time()

		sid()
		if count!=0:
			print(end="\n")
		ResponseTime = time.time()
		if smplTime >= ResponseTime - t2:
			time.sleep((smplTime- ResponseTime + t2))
		else:
			#n=math.ceil((ResponseTime-t2)/smplTime)
			n=((ResponseTime-t2)/smplTime)
			print(n,"n",((n*smplTime)- ResponseTime + t2))
			time.sleep(((n*smplTime)- ResponseTime + t2))
