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

# Include the wiiscracth class
from wiiscratch import wiiscractch
import time
import scratch

import sys, threading, socket, os, platform

VERSION = '0.0.1'
PLAT = platform.system()
ARCH = platform.machine()
PATH = os.path.dirname(os.path.realpath(__file__))

if PLAT == 'Linux':
    if ARCH == 'x86_64':
        sys.path.insert(0, PATH+'/lib/Linux/x64')
    else:
        sys.path.insert(0, PATH+'/lib/Linux/x86')
elif PLAT == 'Darwin':
    sys.path.insert(0, PATH+'/lib/Mac')
elif PLAT == 'Windows':
    if ARCH == 'AMD64':
        sys.path.insert(0, PATH+'/lib/Windows/x64')
    else:
        sys.path.insert(0, PATH+'/lib/Windows/x86')

from Tkinter import *
import tkFont

class GUI:

    def __init__(self, master):

	# Read the necessary image
        self.logo = PhotoImage(file='./res/logo.gif')
        self.red_led = PhotoImage(file='./res/led_red.gif')
        self.green_led = PhotoImage(file='./res/led_green.gif')
        self.quit_up = PhotoImage(file='./res/quit_up.gif')
        self.quit_down = PhotoImage(file='./res/quit_down.gif')
        self.con_up = PhotoImage(file='./res/con_up.gif')
        self.con_down = PhotoImage(file='./res/con_down.gif')
	self.dis_up = PhotoImage(file='./res/dis_up.gif')
        self.dis_down = PhotoImage(file='./res/dis_down.gif')

        bg_color = '#464646'
        fg_color = 'white'
        sub_color = '#BDBDBD'
        
	# Whatever information about the title etc.
        master.wm_title('wiimote4scratch')
        master.resizable(0,0)
        master.configure(background=bg_color)
        master.tk.call('wm', 'iconphoto', master._w, self.logo)
        master.protocol('WM_DELETE_WINDOW', gui_quit)
        
        title_font = tkFont.Font(family='Ubuntu', size=14, weight='bold')
        subtitle_font = tkFont.Font(family='Ubuntu', size=8)
        label_font = tkFont.Font(family='Ubuntu', size=10)
	group_font = tkFont.Font(family='Ubuntu', size=8)

        self.title_frame = Frame(master)
        self.title_frame.configure(background=bg_color)
        Label(self.title_frame, font=title_font, bg=bg_color, fg=fg_color, text='Wiimote for Scratch 1.4').pack()
        self.title_frame.pack(padx=30, pady=10)

	# We can put a nice logo of the group
	self.body_logo = Frame(master)
	self.body_logo.configure(background=bg_color)
	self.logo_image = Label(self.body_logo, bg=bg_color, image=self.logo)
	self.logo_image.grid(row=0, column=0)
	self.body_logo.pack(pady=3)

	# Menu to create the desired number of players and establish the connection
	self.optionGroup = LabelFrame(master, text="Options", bg=bg_color, fg=fg_color, padx=4, pady=4, font=group_font)
	self.optionGroup.pack(padx=10, pady=10)
	self.option_frame = Frame(self.optionGroup)
        self.option_frame.configure(background=bg_color)
	self.label_nbplayer = Label(self.option_frame, text='# of players', bg=bg_color, fg=fg_color, font=label_font, padx=3)
	self.label_nbplayer.grid(row=0, column=0)
	self.spinbox_nbplayer = Spinbox(self.option_frame, from_=1, to=4, bg=bg_color, fg=fg_color, font=subtitle_font, width=2)
	self.spinbox_nbplayer.grid(row=0, column=1, padx=5)
	self.con_btn = Label(self.optionGroup, bg=bg_color, image=self.con_up)
        self.con_btn.bind('<Button-1>', self.con_toggle)
        self.con_btn.bind('<ButtonRelease-1>', self.connect)
	self.option_frame.pack(pady=5)
        self.con_btn.pack(pady=5)
	
	# Create a group in order to show the information about the connection
	self.connectionGroup = LabelFrame(master, text="Connection information", bg=bg_color, fg=fg_color, padx=4, pady=4, font=group_font)
	self.connectionGroup.pack(padx=10, pady=10)
        self.body_frame = Frame(self.connectionGroup)
        self.body_frame.configure(background=bg_color)
        self.wiimote_status = Label(self.body_frame, bg=bg_color, image=self.red_led)
        self.wiimote_status.grid(row=0, column=1, sticky=W)
        Label(self.body_frame, text='Wiimote', bg=bg_color, fg=fg_color, font=label_font).grid(row=0, column=0, padx=10, sticky=W)
        self.scratch_status = Label(self.body_frame, bg=bg_color, image=self.red_led)
        self.scratch_status.grid(row=1, column=1, sticky=W)
        Label(self.body_frame, text='Scratch 1.4', bg=bg_color, fg=fg_color, font=label_font).grid(row=1, column=0, padx=10, sticky=W)
        self.body_frame.pack(pady=3)
        
        self.foot_frame = Frame(master)
        self.foot_frame.configure(background=bg_color)
        self.quit_btn = Label(self.foot_frame, bg=bg_color, image=self.quit_up)
        self.quit_btn.bind('<Button-1>', self.quit_toggle)
        self.quit_btn.bind('<ButtonRelease-1>', self.quit)
        self.quit_btn.pack(pady=(10, 2))
        Label(self.foot_frame, font=subtitle_font, bg=bg_color, fg=sub_color, text='Created by Sergi Valverde - Guillaume Lemaitre - 2014').pack(side=LEFT)
        Label(self.foot_frame, font=subtitle_font, bg=bg_color, fg=sub_color, padx=5, text='v'+VERSION).pack(side=RIGHT)
        self.foot_frame.pack(fill=X, padx=5, pady=(0,3))
        
    def quit(self, item):
        gui_quit()
        
    def quit_toggle(self, event):
        self.quit_btn.config(image=self.quit_down)

    def connect(self,item):
	print "connection to scratch"
	s = scratch.Scratch()
	s.broadcast('connected!')

	self.scratch_status.config(image=self.green_led);
	time.sleep(2)

	nPlayer=int(self.spinbox_nbplayer.get())
	print nPlayer

	# Create a for loop to add all the desired player
	wiiList=[]
	for p in range(nPlayer):
		# Create object
		wiiList.append(wiiscractch())
		# Connect a wiimote
		wiiList[p].wiimote_connect(p)
		# Link both wiimote to scratch
		wiiList[p].scratch_connect(s)

	while True:

		for p in range(nPlayer):
			wiiList[p].wiimote_check_scratch_update()

    def con_toggle(self, event):
        self.con_btn.config(image=self.con_down)
                
    def set_status(self, dev, connected):
        if dev == 'wiimote':
            if connected:
                self.wiimote_status.config(image=self.green_led)
            else:
                self.wiimote_status.config(image=self.red_led)
        elif dev == 'scratch':
            if connected:
                self.scratch_status.config(image=self.green_led)
            else: 
                self.scratch_status.config(image=self.red_led)

def gui_quit():
    root.quit()

######################################################################################
## MAIN PROGRAM START HERE
######################################################################################

root = Tk()
gui = GUI(root)

root.mainloop()
root.destroy()

# Here is the main routine to play with scratch
'''
# Connect to scracth
print "connection to scratch"
s = scratch.Scratch()
s.broadcast('connected!')

nPlayer=1

# Create a for loop to add all the desired player
wiiList=[]
for p in range(nPlayer):
	# Create object
	wiiList.append(wiiscractch())
	# Connect a wiimote
	wiiList[p].wiimote_connect(p)
	# Link both wiimote to scratch
	wiiList[p].scratch_connect(s)

while True:

	for p in range(nPlayer):
		wiiList[p].wiimote_check_scratch_update()
'''

