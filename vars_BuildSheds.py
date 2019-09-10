## Build Sheds
## Define variables
## Jon Skaggs
## intiated 10 September 2019

## REQUIRED USER VARIABLES ----------------------------------------------------

# Define a path string that describes the location of your geodatabase
# (use double back slashes!).
path = "D:\\users_data\\jskaggs\\watershed\\test.gdb"

# Define a projection in ESPG format (www.spatialreference.org). 
proj = 102003

# Input a snapping distance; this is the distance you allow your pour points
# to move to find the highest value accumulation cell. Units are in the units
# of the projection you specified above.
snap_distance = 50

## REQUIRED USER DATA ---------------------------------------------------------

aoi = "aoi"
dem = "dem"
pourpoint = "pourpoint"