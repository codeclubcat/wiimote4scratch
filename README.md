wiimote4scratch
===============

<p>This project attend to use the wiimote to control sprite character in the scratch editor 1.4</p>

# Content

## Installation

The installation has been tested on:
* Lubuntu 14.04 distibution for an ARM architecture
* Ubuntu 14.04 distribution for 64 bits architecture

This project needs the following dependencies:
* cwiid
* scratchpy

### CWWID

Some dependencies are needed in order to compile the cwiid library:

```
apt-get install bison flex libbluetooth-dev libgtk2.0-dev python-dev libtool automake1.10 autoconf quilt patchutils python-all-dev cdbs poppler-data autogen automake gcc bluetooth libbluetooth3-dev libgtk2.0-dev pkg-config python2.7-dev flex bison git-core libbluetooth-dev python-pygame python-tk
```

Then, clone the github repository:

```
git clone https://github.com/bogado/cwiid.git
```

You need to compile the code:
```
cd cwiid
aclocal
autoconf
./configure
make
make install
```

It is possible that the `/usr/local` is not included in the python path. To do so, you can add the following line to your `.bashrc`:

```
export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python2.7/site-packages
```

### SCRATCHPY

Some dependencies are needed in order to compile the scratchpy library:

```
apt-get install python-setuptools
```

The scratchpy library can be cloned such as:

```
git clone https://github.com/pilliq/scratchpy.git
```

You need to install the library with:

```
make install
```

## Usage

Once all the dependencies install, the application wiimotescratch can be launched. The application allowing the bridging between the wiimote(s) and scratch can be found. To execute the application execute the following command line:

```
python wiimote4scratch.py
```

Then, you need to start Scratch and open an example (File->Open). You are ready to establish a connection with the different component (i.e., wiimote and Scratch). Select the number of wiimote to connect and click on the button Connect. Once that the connections to Scratch and the wiimotes are established, you should see two green ticks as status.

You can quit the application at any moment using the Quit button.

A python class is available in `python/wiiscratch.py`

## Scratch

In `scratch/`, several examples of possible applications of the wiimote in scratch are presented.
