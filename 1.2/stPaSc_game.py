#!/usr/bin/env python
import random, os, sys, socket
from time import sleep

print("Do you want to be client or server?")
mode = raw_input(">>> ")

client = False
server = False

if mode == "server":
	server = True

elif mode == "client":
	client = True

else:
	print "You didn't choose an available option."
	print "Options are:"
	print "1.Server"
	print "2.Client"
	sys.exit()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if client:
	print("What server do you want to connect to?")
	HOST = raw_input(">>> ")
elif server:
	HOST = ''

PORT = 1234

user_name1 = raw_input("What is your username? ")
print ("You choose %s as username.") % user_name1

if server:
	print("Waiting for a client to connect...")
	s.bind((HOST, PORT))
	s.listen(1)
	conn, addr = s.accept()
	user_name2 = conn.recv(1024)
	print user_name2 + " connected to your server. \n"
	conn.sendall(user_name1)

elif client:
	print ("connecting to server...")
	try:
		s.connect((HOST, PORT))
	except:
		print ("server is not online")
		sys.exit()

	s.send(user_name1)
	user_name2 = s.recv(1024)
	print "You connected to %s's server on ip: %s \n" %(user_name2, HOST)

############################################# GAME BEGINS ###########################################

clientscore = 0
serverscore = 0
while max(int(clientscore),int(serverscore)) < 3:

	while True:
		print "The game begins"
		choice1 = raw_input("rock (1), paper (2) of scissors (3)? ")
		if choice1 in ["rock", "1", "paper", "2", "scissors", "3"]:
			break

		print "You have to chose rock, paper or scissors!!"

	#print choice1
 
	if server:
		conn.sendall(choice1)
	if client:
		s.sendall(choice1)

	print "You chose %s" % choice1

	if server:
		print ("waiting for %s to finish..." % (user_name2))
		choice2 = conn.recv(1024)
		print "%s choose %s" % (user_name2, choice2)
		#conn.send(choice1)
		#print conn.recv(1024)

	elif client:
		print ("waiting for %s to finish..." % (user_name2))
		choice2 = s.recv(1024)
		print "%s choose %s" % (user_name2, choice2)
		#s.send(choice1)
		#s.recv(1024)

	if server:
		if choice1 in ["1","rock"]:
			choice1_n = 1
		elif choice1 in ["2","paper"]:
			choice1_n = 2
		elif choice1 in ["3","scissors"]:
			choice1_n = 3

		if choice2 in ["1","rock"]:
			choice2_n = 1
		elif choice2 in ["2","paper"]:
			
			choice2_n = 2
		elif choice2 in ["3","scissors"]:
			choice2_n = 3
		
		if choice1_n - choice2_n in [1,-2]:
			winner = user_name1
			serverscore = serverscore + 1
		elif choice1_n - choice2_n in [-1,2]:
			winner = user_name2
			clientscore = clientscore + 1
		elif choice1_n - choice2_n == 0:
			winner = "no one"

		sendItem = winner+';'+str(clientscore)+';'+str(serverscore)
		sleep(0.1)
		conn.send(sendItem)
		print "the winner is %s" % winner
	#	print sendItem
		
	#	conn.send(str(clientscore))
	#	conn.send(str(serverscore))
		print "%s has %d and %s has %d as score.\n" % (user_name1, serverscore, user_name2, clientscore)

	elif client:
	#	sleep(1)
		winner = s.recv(1024)
		winner = winner.split(';',2)
		print "the winner is %s" % winner[0]

		clientscore = int(winner[1])
	#	print clientscore
		serverscore = int(winner[2])
	#	print serverscore
		print "%s has %d and %s has %d as score.\n" % (user_name1, clientscore, user_name2, serverscore)
