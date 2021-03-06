# Script Name: D8DistanceToStreams
#
# Created By:  David Tarboton
# Date:        9/29/11

# Import ArcPy site-package and os modules
import arcpy
import os
import subprocess

# Inputs
inlyr = arcpy.GetParameterAsText(0)
desc = arcpy.Describe(inlyr)
p = str(desc.catalogPath)
arcpy.AddMessage("\nInput D8 Flow Direction Grid: " + p)

inlyr1 = arcpy.GetParameterAsText(1)
desc = arcpy.Describe(inlyr1)
src = str(desc.catalogPath)
arcpy.AddMessage("Input Stream Raster Grid: " + src)

thresh = arcpy.GetParameterAsText(2)
arcpy.AddMessage("Threshold: " + thresh)

# Input Number of Processes
inputProc = arcpy.GetParameterAsText(3)
arcpy.AddMessage("Number of Processes: " + inputProc)

# Output
dist = arcpy.GetParameterAsText(4)
arcpy.AddMessage("Output Distance To Streams: " + dist)

# Construct command
cmd = 'mpiexec -n ' + inputProc + ' D8HDistToStrm -p ' + '"' + p + '"' + ' -src ' + '"' + src + '"' + \
      ' -dist ' + '"' + dist + '"' + ' -thresh ' + thresh

arcpy.AddMessage("\nCommand Line: "+cmd)

# Submit command to operating system
os.system(cmd)

# Capture the contents of shell command and print it to the arcgis dialog box
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

message = "\n"
for line in process.stdout.readlines():
    if isinstance(line, bytes):	    # true in Python 3
        line = line.decode()
    message = message + line
arcpy.AddMessage(message)

# Calculate statistics on the output so that it displays properly
arcpy.AddMessage('Calculate Statistics\n')
arcpy.CalculateStatistics_management(dist)
