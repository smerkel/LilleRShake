# EQRecords

## Presentation

These scripts plot the record for
 * Individual events
 * Multiple stations
 * Saves the plot into a PNG image

## Requirements

Requires
 * matplotlib
 * pyQT5 GUI interface (you can change this at the very top of the script)
 * obspy from https://docs.obspy.org/

## Howto

### Edit settings

Edit the settings at the top of your file with
 * when you want the record to start, typically the date / time of the Earthquake which you can find using the IRIS Earthquake Browser at http://www.iris.washington.edu/ieb/
 * The time window over which to plot the data (300 s if you are somewhat close, 2500 s for something on the otherside of the Earth, maybe)
 * The list of stations you want to plot data for
 * The frequency filter settings. The RaspberryShake app uses 0.1 to 0.8 Hz for global signals, 0.7 to 2.0 Hz for regional, 3 to 8.0 Hz for local stuff. I find that anything above 3 to 4 Hz is quite noisy and affected by local stuff (not earthquakes) based on a quick test on the ULille device.
 * Figure and file name settings

### Run the script!


Simply type 
```
  python3 the-name-of-my-script.py
```

It will save an image of the record for each station you requested and, if you did ask for it, plot the records on screen.

## Example

This is what you will get for the RaspberryShake at ULille if you run the script for the EQ in Italy on 2022-10-31, which is in this folder:

![2022-10-31-Italy-Record-Lille](https://user-images.githubusercontent.com/12073828/199465515-f2346789-275e-4a59-8d1e-949c23a0c007.png)
