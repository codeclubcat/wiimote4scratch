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

        self.logo = PhotoImage(file='./res/logo.gif')
        self.red_led = PhotoImage(file='./res/led_red.gif')
        self.green_led = PhotoImage(file='./res/led_green.gif')
        self.btn_up = PhotoImage(file='./res/btn_up.gif')
        self.btn_down = PhotoImage(file='./res/btn_down.gif')

        bg_color = '#464646'
        fg_color = 'white'
        sub_color = '#BDBDBD'
        
        master.wm_title('wiimote4scratch')
        master.resizable(0,0)
        master.configure(background=bg_color)
        master.tk.call('wm', 'iconphoto', master._w, self.logo)
        master.protocol('WM_DELETE_WINDOW', gui_quit)
        
        title_font = tkFont.Font(family='Verdana', size=14, weight='bold')
        subtitle_font = tkFont.Font(family='Verdana', size=11)
        label_font = tkFont.Font(family='Verdana', size=13)

        self.title_frame = Frame(master)
        self.title_frame.configure(background=bg_color)
        Label(self.title_frame, font=title_font, bg=bg_color, fg=fg_color, text='Wiimote for Scratch 1.4').pack()
        self.title_frame.pack(padx=30, pady=10)

	self.body_logo = Frame(master)
	self.body_logo.configure(background=bg_color)
	self.logo_image = Label(self.body_logo, bg=bg_color, image=self.logo)
	self.logo_image.grid(row=0, column=0)
	self.body_logo.pack(pady=3)
	
        self.body_frame = Frame(master)
        self.body_frame.configure(background=bg_color)
        self.leap_status = Label(self.body_frame, bg=bg_color, image=self.red_led)
        self.leap_status.grid(row=0, column=1, sticky=W)
        Label(self.body_frame, text='Wiimote', bg=bg_color, fg=fg_color, font=label_font).grid(row=0, column=0, padx=10, sticky=W)
        self.scratch_status = Label(self.body_frame, bg=bg_color, image=self.red_led)
        self.scratch_status.grid(row=1, column=1, sticky=W)
        Label(self.body_frame, text='Scratch 1.4', bg=bg_color, fg=fg_color, font=label_font).grid(row=1, column=0, padx=10, sticky=W)
        self.body_frame.pack(pady=3)
        
        self.foot_frame = Frame(master)
        self.foot_frame.configure(background=bg_color)
        self.quit_btn = Label(self.foot_frame, bg=bg_color, image=self.btn_up)
        self.quit_btn.bind('<Button-1>', self.quit_toggle)
        self.quit_btn.bind('<ButtonRelease-1>', self.quit)
        self.quit_btn.pack(pady=(10, 2))
        Label(self.foot_frame, font=subtitle_font, bg=bg_color, fg=sub_color, text='Created by Sergi Valverde - Guillaume Lemaitre - 2014').pack(side=LEFT)
        Label(self.foot_frame, font=subtitle_font, bg=bg_color, fg=sub_color, padx=5, text='v'+VERSION).pack(side=RIGHT)
        self.foot_frame.pack(fill=X, padx=5, pady=(0,3))
        
    def quit(self, item):
        gui_quit()
        
    def quit_toggle(self, event):
        self.quit_btn.config(image=self.btn_down)
                
    def set_status(self, dev, connected):
        if dev == 'wiimote':
            if connected:
                self.leap_status.config(image=self.green_led)
            else:
                self.leap_status.config(image=self.red_led)
        elif dev == 'scratch':
            if connected:
                self.scratch_status.config(image=self.green_led)
            else: 
                self.scratch_status.config(image=self.red_led)

def refresh_screen(wiimote):
        gui.set_status('wiimote', wiimote.wii_is_connected)
        gui.set_status('scratch', wiimote.wii_is_linked)

def clear_screen():
    if PLAT == 'Linux' or PLAT == 'Darwin':
        os.system('clear')
    elif PLAT == 'Windows':
        os.system('CLS')

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

