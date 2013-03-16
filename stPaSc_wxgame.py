import wx, socket

class SecondaryFrame(wx.Frame):
	def __init__(self, parent, id, user_name1, user_name2, server, s, conn, client):
		wx.Frame.__init__(self, parent, id, "Steen, papier, schaar - Play a game", pos=(150, 150), size=(400, 300))

		self.playPanel = wx.Panel(self)

		self.clientscore = 0
		self.serverscore = 0

		self.steenBtn = wx.Button(self.playPanel, -1, "steen", pos=(10, 100), size=(100 , -1))
		self.papierBtn = wx.Button(self.playPanel, -1, "papier", pos=(142.5, 100), size=(100 , -1))
		self.schaarBtn = wx.Button(self.playPanel, -1, "schaar", pos=(275, 100), size=(100 , -1))

		self.Bind(wx.EVT_BUTTON, self.choseSteen, self.steenBtn)
		self.Bind(wx.EVT_BUTTON, self.chosePapier, self.papierBtn)
		self.Bind(wx.EVT_BUTTON, self.choseSchaar, self.schaarBtn)

		#######################Output##########################################

		self.OutputText = wx.StaticText(self.playPanel, -1, "                                                    ", size=(300, 100), pos=(55, 150))
		self.OutputText.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))

		self.OutputScore1 = wx.StaticText(self.playPanel, -1,"                                           ")

		self.server = server
		self.user_name1 = user_name1
		self.user_name2 = user_name2
		self.s = s
		self.conn = conn
		self.client = client

	def choseSteen(self,event):
		self.choice1 = "steen"
		self.givescores()

	def chosePapier(self, event):
		self.choice1 = "papier"
		self.givescores()

	def choseSchaar(self, event):
		self.choice1 = "schaar"
		self.givescores()

	def givescores(self):
		self.steenBtn.Hide()
		self.papierBtn.Hide()
		self.schaarBtn.Hide()

		if self.server:
			self.conn.sendall(self.choice1)
		if self.client:
			self.s.sendall(self.choice1)

		self.OutputText.SetLabel("You chose %s" % self.choice1)

		if self.server:
			self.OutputText.SetLabel("waiting for %s to finish..." % self.user_name2)
			self.choice2 = self.conn.recv(1024)
			self.OutputText.SetLabel("%s choose %s" % (self.user_name2, self.choice2))

		elif self.client:
			self.OutputText.SetLabel("waiting for %s to finish..." % self.user_name2)
			self.choice2 = self.s.recv(1024)
			self.OutputText.SetLabel("%s choose %s" % (self.user_name2, self.choice2))

	def getWinner(self):
		if self.server:
			if self.choice1 in ["1","steen"]:
				self.choice1_n = 1
			elif self.choice1 in ["2","papier"]:
				self.choice1_n = 2
			elif self.choice1 in ["3","schaar"]:
				self.choice1_n = 3

			if self.choice2 in ["1","steen"]:
				self.choice2_n = 1
			elif self.choice2 in ["2","papier"]:
				
				self.choice2_n = 2
			elif self.choice2 in ["3","schaar"]:
				self.choice2_n = 3
			
			if self.choice1_n - self.choice2_n in [1,-2]:
				self.winner = self.user_name1
				self.serverscore = self.serverscore + 1
			elif self.choice1_n - self.choice2_n in [-1,2]:
				self.winner = self.user_name2
				self.clientscore = self.clientscore + 1
			elif self.choice1_n - self.choice2_n == 0:
				self.winner = "no one"

			self.sendItem = self.winner+';'+str(self.clientscore)+';'+str(self.serverscore)
			sleep(0.1)
			self.conn.send(self.sendItem)
			self.OutputText.SetLabel( "the winner is %s" % self.winner)
			self.OutputText.SetLabel( "%s has %d and %s has %d as score.\n" % (self.user_name1, self.serverscore, self.user_name2, self.clientscore))

		elif self.client:
			self.winner = self.s.recv(1024)
			self.winner = self.winner.split(';',2)
			self.OutputText.SetLabel( "the winner is %s" % self.winner[0])
			self.clientscore = int(self.winner[1])
			self.serverscore = int(self.winner[2])
			self.OutputText.SetLabel( "%s has %d and %s has %d as score.\n" % (self.user_name1, self.clientscore, self.user_name2, self.serverscore))


	self.steenBtn.Show()
	self.papierBtn.Show()
	self.schaarBtn.Show()






class MainFrame(wx.Frame):
	conn = ""
	def __init__(self, parent, id):
		wx.Frame.__init__(self, parent, id, "Steen, papier, schaar - Connect to Player", pos=(150, 150), size=(400, 300))

		self.connectPanel = wx.Panel(self)

		###############################SERVER-CLIENT########################
		serverBtn = wx.Button(self.connectPanel, -1, "server", (50, 20), (100, -1))
		clientBtn = wx.Button(self.connectPanel, -1, "client", (200, 20), (100, -1))

		self.Bind(wx.EVT_BUTTON, self.choseServer, serverBtn)
		self.Bind(wx.EVT_BUTTON, self.choseClient, clientBtn)

		self.PORT = 1234
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		#############################Username#################################

		self.user_nameTxt = wx.TextCtrl(self.connectPanel, -1, "Username", size=(125, -1), pos=(50, 90))

		self.Bind(wx.EVT_TEXT, self.Un, self.user_nameTxt)

		#############################Test###############################

		changeScreenBtn = wx.Button(self.connectPanel, -1, "change Frame", pos=(50, 280), size=(100, -1))
		self.Bind(wx.EVT_BUTTON, self.loadSecondaryFrameEvent, changeScreenBtn)

		#############################Output###############################

		self.OutputText = wx.StaticText(self.connectPanel, -1, "                                                    ", size=(300, 100), pos=(55, 150))
		self.OutputText.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))


		

	def choseServer(self, event):
		self.server = True
		self.client = False
		#self.OutputText.SetLabel("server")

		self.HOST = ""

		self.openServerBtn = wx.Button(self.connectPanel, -1, "Open Server", size=(100, -1), pos=(50, 60))

		self.Bind(wx.EVT_BUTTON, self.connectToPlayer, self.openServerBtn)

		try:
			self.ipTxt.Hide()
			self.connectBtn.Hide()
		except:
			print ""

	def choseClient(self, event):
		self.client = True
		self.server = False
		self.ip = "IP HERE"

		self.ipTxt = wx.TextCtrl(self.connectPanel, -1, self.ip, size=(125, -1), pos=(50, 60))
		self.connectBtn = wx.Button(self.connectPanel, -1, "connect to server", size=(100, -1), pos=(200, 60))

		self.Bind(wx.EVT_TEXT, self.setIp, self.ipTxt)
		self.Bind(wx.EVT_BUTTON, self.connectToPlayer, self.connectBtn)

		#self.OutputText.SetLabel("client")

		try:
			self.openServerBtn.Hide()
		except:
			print ""

	def setIp(self, event):
		self.HOST = event.GetString()

	def connectToPlayer(self, event):
		if self.server:
			self.OutputText.SetLabel("waiting for client to connect...")
			self.s.bind((self.HOST, self.PORT))
			self.s.listen(1)
			self.conn, self.addr = self.s.accept()
			self.user_name2 = self.conn.recv(1024)
			self.OutputText.SetLabel(self.user_name2 + " connected to your server. \n")
			self.conn.sendall(self.user_name1)

		elif self.client:
			self.OutputText.SetLabel("connecting to server...")
			try:
				self.s.connect((self.HOST, self.PORT))
			except:
				self.OutputText.SetLabel("server is not online")

			self.s.send(self.user_name1)
			self.user_name2 = self.s.recv(1024)
			self.OutputText.SetLabel("You connected to %s's server on ip: %s \n" %(self.user_name2, self.HOST))

		self.loadSecondaryFrame()

	def loadSecondaryFrame(self):
		frame = SecondaryFrame(None, -1, self.user_name1, self.user_name2, self.server, self.s, self.conn, self.client)
		frame.Show()
		self.Hide()

	def loadSecondaryFrameEvent(self, event):
		frame = SecondaryFrame(None, -1)
		frame.Show()
		self.Hide()


	def Un(self,event):
		self.user_name1 = event.GetString()



if __name__ == "__main__":
	app = wx.PySimpleApp()
	frame = MainFrame(None, -1)
	frame.Show()
	app.MainLoop()
