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

from Tkinter import *
import time
import threading
import random
import Queue
import tkFont 

from wiiscratch import wiiscractch
import scratch


import platform, os, sys, socket

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

class GuiPart:
    def __init__(self, master, queue_wiimote, endCommand):
        self.queue_wiimote = queue_wiimote
        # Set up the GUI
        #console = Button(master, text='Done', command=endCommand)
        #console.pack()
        # Add more GUI stuff here
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
        self.quit_btn.bind('<ButtonRelease-1>', endCommand)
        self.quit_btn.pack(pady=(10, 2))
        Label(self.foot_frame, font=subtitle_font, bg=bg_color, fg=sub_color, text='Created by Sergi Valverde - Guillaume Lemaitre - 2014').pack(side=LEFT)
        Label(self.foot_frame, font=subtitle_font, bg=bg_color, fg=sub_color, padx=5, text='v'+VERSION).pack(side=RIGHT)
        self.foot_frame.pack(fill=X, padx=5, pady=(0,3))

        self.isWiimoteConnected = False
        self.isScratchConnected = False

    def processIncoming(self):
        """
        Handle all the messages currently in the queue (if any).
        """
        while self.queue_wiimote.qsize():
            try:
                msg = self.queue_wiimote.get(0)
                print msg
            except Queue.Empty:
                pass


    def connect(self,item):

        if not self.isWiimoteConnected:
            print "connection to scratch"
            s = scratch.Scratch()
            s.broadcast('scratch connected!')

            self.isScratchConnected = True

            nPlayer=int(self.spinbox_nbplayer.get())

            # Create a for loop to add all the desired player
            self.wiiList=[]
            self.number_wiimote = 0
            for p in range(nPlayer):
                # Create object                                                                                                                                    
                self.wiiList.append(wiiscractch())
                # Connect a wiimote                                                                                                                                
                self.wiiList[p].wiimote_connect(p)
                # Link both wiimote to scratch                                                                                                                     
                self.wiiList[p].scratch_connect(s)
                # Number of wiimote
                self.number_wiimote += 1
            
            self.isWiimoteConnected = True
        else:
            print "The wiimote(s) are already connected"

    def con_toggle(self, event):
        self.con_btn.config(image=self.con_down)


    def quit_toggle(self, event):
        self.quit_btn.config(image=self.quit_down)

    def quit(self, item):
        gui_quit()

class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """
    def __init__(self, master):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI. We spawn a new thread for the worker.
        """
        self.master = master

        # Create the queue
        self.queue_wiimote = Queue.Queue()

        # Set up the GUI part
        self.gui = GuiPart(master, self.queue_wiimote, self.endApplication)

        # Set that we are running the software
        self.running = 1
        self.thread_wiimote = threading.Thread(target = self.workerThreadConnectedWiimote)
        self.thread_wiimote.start()

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall()

    def periodicCall(self):
        """
        Check every 100 ms if there is something new in the queue.
        """
        self.gui.processIncoming()
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
        self.master.after(100, self.periodicCall)
    
    # Thread for the update of the wiimote connecte
    def workerThreadConnectedWiimote(self):
        while self.running:
            print self.gui.isWiimoteConnected
            if self.gui.isWiimoteConnected:
                for p in range(self.gui.number_wiimote):
                    self.gui.wiiList[p].wiimote_check_scratch_update()
                self.gui.wiimote_status.config(image=self.gui.green_led)
            else:
                self.gui.wiimote_status.config(image=self.gui.red_led)
            if self.gui.isScratchConnected:
                self.gui.scratch_status.config(image=self.gui.green_led)
            else:
                self.gui.scratch_status.config(image=self.gui.red_led)
            self.queue_wiimote.put(self.gui.isWiimoteConnected)

    def endApplication(self, item):
        self.running = 0

def gui_quit():
    import sys
    sys.exit(1)
    root.quit()

root = Tk()

client = ThreadedClient(root)
root.mainloop()
