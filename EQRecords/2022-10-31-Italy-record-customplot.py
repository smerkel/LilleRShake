#!/usr/bin/env python3

# 
# This file is part of the LilleRShake distribution (https://github.com/xxxx or http://xxx.github.io).
# Copyright (c) 2022 Sébastien Merkel, Univ. Lille, France
# 
# This program is free software: you can redistribute it and/or modify  
# it under the terms of the GNU General Public License as published by  
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License 
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

from obspy.clients.fdsn import Client
from obspy import UTCDateTime
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Date and time of the event, in UTC
record_start="2022-10-31T21:42:50"
# convert this into UTC Date Time format, and add some extra time before or after the event (in seconds)
starttime = UTCDateTime(record_start) - 100
# The end time for the plot
endtime = starttime + 800
# List of station names
# You can put as many stations as you wish, 1 file will be generated for each station
# find the name of the seismometer from stationview at https://raspberryshake.net/stationview/
stationnames = ["R8C0C","R28DF","RC786"]
# List of station label
stationlabels = ["Lille","Ahrweiler","Scuol"]
# Min frequency for filter
minBP = 0.1
# Min frequency for filter
maxBP = 1.0
# Stem for saving (all files will starting with this, will add the station label after this
stemfilename = "2022-10-31-Italy-Record"
# define which client will be the source of the data, this is the client for the Raspberry Shakes
client = Client(base_url='https://fdsnws.raspberryshakedata.com/')
# See the plots (True or False), save to file is always True
seeplots = False
# Figure width (in inches)
figw = 12
# Figure height (in inches)
figh = 4
# dots per inches
dpi = 120
# Marker every X minutes on horizontal axis
markersepmin = 1


i = -1
for stationname in stationnames:
	i += 1
	stationlabel = stationlabels[i]

	# Get the signal for this station
	# for a station with a short period seismometer EHZ. Some Shakes have an SHZ sensor instead.
	waveform = client.get_waveforms('AM', stationname, '00', 'EHZ', starttime, endtime)
	waveform += client.get_waveforms('AM', stationname, '00', 'EHE', starttime, endtime)
	waveform += client.get_waveforms('AM', stationname, '00', 'EHN', starttime, endtime)
	# place the mean value at zero on the axes
	waveform.detrend(type='demean')
	# To apply a bandpass filter to cut out low-frequency and high-frequency noise
	waveform.filter("bandpass", freqmin=minBP, freqmax=maxBP, corners=4)
	# Old version to create a normal plot in a file for the seismometer. 
	# Not enough customization
	# filename = "2022-10-31-Italy-Record.png"
	# print to file, type = 'relative' for relative times, type = 'normal' for UTC
	# waveform.plot(outfile=filename,size=(1920,800),type='normal', number_of_ticks=12, grid_linewidth=.5, grid_linestyle='--')

	# Getting min and max of ydata (to figure out scales)
	minY = min(min(waveform[0].data),min(waveform[1].data),min(waveform[2].data))
	maxY = max(max(waveform[0].data),max(waveform[1].data),max(waveform[2].data),-minY)

	fig = plt.figure(figsize=(figw, figh), dpi=dpi)
	# these are matplotlib.patch.Patch properties (used for the text boxes with seismometer names)
	props = dict(boxstyle='round', facecolor='white', alpha=0.5)
	xlocator = mdates.MinuteLocator(interval = markersepmin)

	# First plot, EHZ
	ax = fig.add_subplot(3, 1, 1)
	ax.plot(waveform[0].times("matplotlib"), waveform[0].data, "k-", linewidth=0.5)
	ax.set_ylim([-maxY, maxY])
	ax.xaxis_date()
	ax.tick_params(direction="in")
	ax.grid(True, axis='x', linestyle='-.')
	ax.tick_params(labelbottom=False)
	ax.xaxis.set_major_locator(xlocator)
	ax.text(0.05, 0.9, stationlabel+"-EHZ", transform=ax.transAxes, fontsize=12, verticalalignment='top', bbox=props)

	# Second plot, EHE
	ax = fig.add_subplot(3, 1, 2)
	ax.plot(waveform[1].times("matplotlib"), waveform[1].data, "k-", linewidth=0.5)
	ax.set_ylim([-maxY, maxY])
	ax.xaxis_date()
	ax.tick_params(direction="in")
	ax.grid(True, axis='x', linestyle='-.')
	ax.tick_params(labelbottom=False)
	ax.xaxis.set_major_locator(xlocator)
	ax.text(0.05, 0.9, stationlabel+"-EHE", transform=ax.transAxes, fontsize=12, verticalalignment='top', bbox=props)

	# Third plot, EHN
	ax = fig.add_subplot(3, 1, 3)
	ax.plot(waveform[2].times("matplotlib"), waveform[2].data, "k-", linewidth=0.5)
	ax.set_ylim([-maxY, maxY])
	ax.xaxis_date()
	ax.tick_params(direction="in")
	ax.grid(True, axis='x', linestyle='-.')
	ax.xaxis.set_major_locator(xlocator)
	ax.text(0.05, 0.9, stationlabel+"-EHN", transform=ax.transAxes, fontsize=12, verticalalignment='top', bbox=props)

	# Final touches
	ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
	plt.subplots_adjust(wspace=0.0, hspace=0.0, bottom=0.07, top=0.97, left=0.05, right=0.97)
	out = stemfilename+"-"+stationlabel+".png"
	plt.savefig(out)
	print ("Seismometer data saved in " + out)
	if (seeplots):
		plt.show(block=True)
