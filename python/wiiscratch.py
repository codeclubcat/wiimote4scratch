#********************************************************************************
# wiimote4scrath 1.4
# sergi valverde
# guillaume Lemaitre
#********************************************************************************

############################################################################
#  This program is free software: you can redistribute it and/or modify    #
#  it under the terms of the GNU General Public License as published by    #
#  the Free Software Foundation, either version 3 of the License, or       #
#  (at your option) any later version.                                     #
#                                                                          #
#  This program is distributed in the hope that it will be useful,         #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of          #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
#  GNU General Public License for more details.                            #
#                                                                          #
#  You should have received a copy of the GNU General Public License       #
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.   #
############################################################################

# Import the needed module
import cwiid
import time
import scratch

# delay between p
button_delay = 0.1

# Create the wiiscratch class
class wiiscractch:
	# Initialisation
	def __init__(self):
		# Initialisation of scratch object
		self.s = None;
		# Initialisation of the button status
		self.b_left_pressed = False
		self.b_right_pressed = False
		self.b_up_pressed = False
		self.b_down_pressed = False
		self.b_one_pressed = False
		self.b_two_pressed = False
		self.b_A_pressed = False
		self.b_B_pressed = False
		self.b_HOME_pressed = False
		self.b_MINUS_pressed = False
		self.b_PLUS_pressed = False
		# Initialisation of the cwiid object
		self.wiimote = None;
		# Initialisation of the id
		self.wiimoteID = ''
		# Initialisation of the wiimote status connection
		self.wii_is_connected = False
		# Initialisation of the scract status
		self.wii_is_linked = False

	# Connect to scratch
	def scratch_connect(self,scracth_object):
		self.s = scracth_object
		print "The wiimote is linked to scratch"

		self.wii_is_linked = True

		# Initialise all the sensors values in scratch
		self.s.sensorupdate({self.wiimoteID+'button_left' : 0})
		self.s.sensorupdate({self.wiimoteID+'button_right' : 0})
		self.s.sensorupdate({self.wiimoteID+'button_up' : 0})
		self.s.sensorupdate({self.wiimoteID+'button_down' : 0})
		self.s.sensorupdate({self.wiimoteID+'button_one' : 0})
		self.s.sensorupdate({self.wiimoteID+'button_two' : 0})
		self.s.sensorupdate({self.wiimoteID+'button_A' : 0})
		self.s.sensorupdate({self.wiimoteID+'button_B' : 0})
		self.s.sensorupdate({self.wiimoteID+'button_HOME' : 0})
		self.s.sensorupdate({self.wiimoteID+'button_MINUS' : 0})
		self.s.sensorupdate({self.wiimoteID+'button_PLUS' : 0})
		time.sleep(button_delay)
			

	# Connect a wiimote 
	def wiimote_connect(self,identifier):
		print "Instanciate connection to a wiimote"		
		i = 2
		while not self.wiimote:
			try:
				self.wiimote=cwiid.Wiimote()
			except RuntimeError:
				if (i>5):
				    print("cannot create connection")
		print "WIIMOTE CONNECTED!"
		
		#set wiimote to report button presses and accelerometer state
		self.wiimote.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC

		#turn on led to show connected
		self.wiimote.led = identifier+1

		#give an id
		self.wiimoteID = 'Player_' + str(identifier+1) + '_'

		#the remote is connected
		self.wii_is_connected = True

	# Check buttons status and send messages to scractch
	def wiimote_check_scratch_update(self):
		
		buttons = self.wiimote.state['buttons']
		accel = self.wiimote.state['acc']

		# -------------------------------------------
		# button information
		# -------------------------------------------
		# button left
		if buttons & cwiid.BTN_LEFT & ~self.b_left_pressed:
			self.s.sensorupdate({self.wiimoteID+'button_left' : 1})
			self.b_left_pressed = True
			time.sleep(button_delay)
		elif self.b_left_pressed:
			self.s.sensorupdate({self.wiimoteID+'button_left' : 0})
			self.b_left_pressed = False
			time.sleep(button_delay)
		# button right
		if buttons & cwiid.BTN_RIGHT & ~self.b_right_pressed:
			self.s.sensorupdate({self.wiimoteID+'button_right' : 1})
			self.b_right_pressed = True
			time.sleep(button_delay)
		elif self.b_right_pressed:
			self.s.sensorupdate({self.wiimoteID+'button_right' : 0})
			self.b_right_pressed = False
			time.sleep(button_delay)
		# button up
		if buttons & cwiid.BTN_UP & ~self.b_up_pressed:
			self.s.sensorupdate({self.wiimoteID+'button_up' : 1})
			self.b_up_pressed = True
			time.sleep(button_delay)
		elif self.b_up_pressed:
			self.s.sensorupdate({self.wiimoteID+'button_up' : 0})
			self.b_up_pressed = False
			time.sleep(button_delay)
		# button down
		if buttons & cwiid.BTN_DOWN & ~self.b_down_pressed:
			self.s.sensorupdate({self.wiimoteID+'button_down' : 1})
			self.b_down_pressed = True
			time.sleep(button_delay)
		elif self.b_down_pressed:
			self.s.sensorupdate({self.wiimoteID+'button_down' : 0})
			self.b_down_pressed = False
			time.sleep(button_delay)
		# button 1
		if buttons & cwiid.BTN_1 & ~self.b_one_pressed:
			self.s.sensorupdate({self.wiimoteID+'button_one' : 1})
			self.b_one_pressed = True
			time.sleep(button_delay)
		elif self.b_one_pressed:
			self.s.sensorupdate({self.wiimoteID+'button_one' : 0})
			self.b_one_pressed = False
			time.sleep(button_delay)
		# button 2
		if buttons & cwiid.BTN_2 & ~self.b_two_pressed:
			self.s.sensorupdate({self.wiimoteID+'button_two' : 1})
			self.b_two_pressed = True
			time.sleep(button_delay)
		elif self.b_two_pressed:
			self.s.sensorupdate({self.wiimoteID+'button_two' : 0})
			self.b_two_pressed = False
			time.sleep(button_delay)
		# button A
		if buttons & cwiid.BTN_A & ~self.b_A_pressed:
			self.s.sensorupdate({self.wiimoteID+'button_A' : 1})
			self.b_A_pressed = True
			time.sleep(button_delay)
		elif self.b_A_pressed:
			self.s.sensorupdate({self.wiimoteID+'button_A' : 0})
			self.b_A_pressed = False
			time.sleep(button_delay)
		# button B
		if buttons & cwiid.BTN_B & ~self.b_B_pressed:
			self.s.sensorupdate({self.wiimoteID+'button_B' : 1})
			self.b_B_pressed = True
			time.sleep(button_delay)
		elif self.b_B_pressed:
			self.s.sensorupdate({self.wiimoteID+'button_B' : 0})
			self.b_B_pressed = False
			time.sleep(button_delay)
		# button HOME
		if buttons & cwiid.BTN_HOME & ~self.b_HOME_pressed:
			self.s.sensorupdate({self.wiimoteID+'button_HOME' : 1})
			self.b_HOME_pressed = True
			time.sleep(button_delay)
		elif self.b_HOME_pressed:
			self.s.sensorupdate({self.wiimoteID+'button_HOME' : 0})
			self.b_HOME_pressed = False
			time.sleep(button_delay)
		# button MINUS
		if buttons & cwiid.BTN_MINUS & ~self.b_MINUS_pressed:
			self.s.sensorupdate({self.wiimoteID+'button_MINUS' : 1})
			self.b_MINUS_pressed = True
			time.sleep(button_delay)
		elif self.b_MINUS_pressed:
			self.s.sensorupdate({self.wiimoteID+'button_MINUS' : 0})
			self.b_MINUS_pressed = False
			time.sleep(button_delay)
		# button PLUS
		if buttons & cwiid.BTN_PLUS & ~self.b_PLUS_pressed:
			self.s.sensorupdate({self.wiimoteID+'button_PLUS' : 1})
			self.b_PLUS_pressed = True
			time.sleep(button_delay)
		elif self.b_PLUS_pressed:
			self.s.sensorupdate({self.wiimoteID+'button_PLUS' : 0})
			self.b_PLUS_pressed = False
			time.sleep(button_delay)
