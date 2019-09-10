## Build more watersheds
## Jon Skaggs
## 5 September 2019

## ----------------------------------------------------------------------------

## DEFINE USER VARIABLES IN "vars_BuildSheds.py"

## ----------------------------------------------------------------------------

## Import modules
print "## Importing modules"
# This bad boy has the ESRI tools we want to use.
import arcpy
# These are the expensive ESRI tools.
from arcpy.sa import *
# This bad boy helps keep track of how long things are taking.
import timeit

## Set the start time
print "## Starting timer"
start_master = timeit.default_timer()

# Set user defined variables.
print "## Setting user defined variables"
from vars_BuildSheds import *

## Set global variables
print "## Setting global variables"
# The workspace is where our data are.
arcpy.env.workspace = path
# This is the projection we are going to use as defined by the user.
proj = arcpy.SpatialReference(proj)
# Set overwrite to True for debugging.
arcpy.env.overwriteOutput = True
# Get the SA license.
arcpy.CheckOutExtension("Spatial")

print ""
## Print notes for the user.
print "Start time:",
print int(start_master/60)
print "The workspace is:",
print arcpy.env.workspace
print "The projection you have provided is:",
print proj.name
# Print license confirmation to console. If it is not initialized,
# print a warning message to the console and exist the script.
if arcpy.CheckExtension("Spatial") == "Available":
    print "The Spatial Analyst license is loaded."
else:
    message = "The Spatial Analyst license was not loaded correctly."
    print message
    sys.exit(message)
print ""

## Is the data in the workspace?
print "Checking for the input data in the workspace."
# Here is the list of inputs we need to generate watersheds.
# Loop through each input and check if they exist in our workspace.

OurFiles = [aoi, dem, pourpoint]
for i in range(len(OurFiles)):
    if arcpy.Exists(OurFiles[i]):
        print OurFiles[i],
        print "is present."
    else:
        print OurFiles[i] 
        notpresent_message = "is not present."
        print notpresent_message
        sys.exit (notpresent_message)
count = arcpy.GetCount_management(pourpoint)
print "pourpoint count is:",
print (count)
stop = timeit.default_timer()
elapsed = stop - start_master
print "Time elapsed:", 
print int(elapsed/60)
print ""

# Project data.
print "Projecting the vector data."
if not arcpy.Exists("pourpoint_p"):
    arcpy.Project_management(
        in_dataset = pourpoint, 
        out_dataset = pourpoint + "_p", 
        out_coor_system = proj)
print "Projecting the raster data."
if not arcpy.Exists("dem_p"):
    arcpy.ProjectRaster_management(
        in_raster = dem,
        out_raster = dem + "_p",
        out_coor_system = proj,
        resampling_type = "BILINEAR")
stop = timeit.default_timer()
elapsed = stop - start_master
print "Time elapsed:", 
print int(elapsed/60)
print ""

# ADD A CHECK HERE AND RETURN VALUE TO CONSOLE

# Fill sinks in the raster.
print "Filling raster sinks."
dem_fill = Fill(in_surface_raster = dem)
stop = timeit.default_timer()
elapsed = stop - start_master
print "Time elapsed:", 
print int(elapsed/60)
print ""

# Calculate flow direction.
print "Calculating flow direction."
dem_dir = FlowDirection(in_surface_raster = dem_fill)
stop = timeit.default_timer()
elapsed = stop - start_master
print "Time elapsed:", 
print int(elapsed/60)
print ""

# Calculate flow accumulation.
print "Calculating flow accumulation."
dem_acc = FlowAccumulation(
    in_flow_direction_raster = dem_dir,
    data_type = "INTEGER")
stop = timeit.default_timer()
elapsed = stop - start_master
print "Time elapsed:", 
print int(elapsed/60)
print ""

# Snap pour points
print "Snapping pour points to high accumulation cells."
if check_snap == 1:
    pourpoint_snap = SnapPourPoint(
        in_pour_point_data = pourpoint,
        in_accumulation_raster = dem_acc,
        snap_distance = snap_distance)
    arcpy.FeatureClassToShapefile_conversion(
        in_features = pourpoint_snap,
        output_folder = "D:\\users_data\\jskaggs\\watershed\\")
    checksnap_message = "Shapefile of snapped points written to parent folder."
    print checksnap_message
    stop = timeit.default_timer()
    elapsed = stop - start_master
    print "Time elapsed:", 
    print int(elapsed/60)
    print ""
    sys.exit(checksnap_messsage)
else:
    pourpoint_snap = SnapPourPoint(
        in_pour_point_data = pourpoint,
        in_accumulation_raster = dem_acc,
        snap_distance = snap_distance)
    stop = timeit.default_timer()
    elapsed = stop - start_master
    print "Time elapsed:", 
    print int(elapsed/60)
    print ""

# ADD AN AUTOMATIC SITE ID GENERATOR
# ADD FUNCTION TO RECORD SNAPPED DISTANCE

# Draw watersheds
print "Drawing watersheds."
wshed = Watershed(
    in_flow_direction_raster = dem_dir,
    in_pour_point_data = pourpoint_snap)
    
# Save watersheds to disk.
print "Saving watersheds."
arcpy.CopyFeatures_management(
    input_features = wshed,
    out_feature_class = wshed_f)
stop = timeit.default_timer()
elapsed = stop - start_master
print "Time elapsed:", 
print int(elapsed/60)
print ""