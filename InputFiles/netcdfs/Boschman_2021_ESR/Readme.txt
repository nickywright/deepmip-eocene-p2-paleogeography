# Readme for Boschman_2021_ESR

This is a processed copy of Boschman's (2021) South America paleotopography. This is from her preferred reconstruction, and can be obtained from the Supplementary data associated with her paper: 
Boschman, L.M., 2021, Andean mountain building since the Late Cretaceous: A paleoelevation reconstruction, Earth-Science Reviews, v220, https://doi.org/10.1016/j.earscirev.2021.103640

I (Nicky Wright) converted this to a netcdf using:

The following commands (in R):
# ---- 
# import libraries, otherwise it doesn't work
library(rgdal)
library(raster)
library(ncdf4)


# for a single file:
# import file
# raster_grd = raster("4.rasters\ reconstruction\ PREFERRED/0_Ma.grd")
# save the raster, specify 'nc' for the ending
# writeRaster(raster_grd, "4.rasters\ reconstruction\ PREFERRED/0_Ma.nc", varname="z", overwrite=TRUE)

# make a folder to write the final grids to
system('mkdir "4.rasters\ reconstruction\ PREFERRED/netcdfs"')
system('mkdir "4.rasters\ reconstruction\ PREFERRED/netcdfs/original_region"')

# make a grid of nans
system('echo "0 -90" | gmt grdmask -Rd -I0.1d -Gmask.nc -S0 -fg')
system('gmt grdmath  mask.nc 0 NAN = mask_nans.nc')

# to loop through:
for (i in 0:80) {
	# import file: need to use 'paste0', otherwise R gets confused!
	raster_grd <- raster(paste0("4.rasters\ reconstruction\ PREFERRED/",i,"_Ma.grd"))
	writeRaster(raster_grd, paste0("4.rasters\ reconstruction\ PREFERRED/netcdfs/original_region/",i,"_Ma.nc"), varname="z", overwrite=TRUE)
		
	# a bunch of code to convert them to the same region
	# modify using GMT
	system(sprintf('echo "Working on %s Ma"', i))
	system(sprintf('gmt grdinfo "4.rasters\ reconstruction\ PREFERRED/netcdfs/original_region/%s_Ma.nc"', i))
	
	# convert to gridline registration
	system(sprintf('gmt grdedit "4.rasters\ reconstruction\ PREFERRED/netcdfs/original_region/%s_Ma.nc" -G%s_Ma-gl.nc -T', i, i))
	
	# use grdblend to make a global grid
	system(sprintf('gmt grdblend %s_Ma-gl.nc mask_nans.nc -G"4.rasters\ reconstruction\ PREFERRED/netcdfs/%s_Ma.nc" -Cf', i, i))
	
	# delete the gridline grid
	system(sprintf('rm %s_Ma-gl.nc', i))
}
# ---- 
