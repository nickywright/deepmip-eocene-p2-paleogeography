# Readme for ETOPO1

This is a version of the bedrock grid-registered ETOPO1 (present-day bathymetry/topography), that has been regridded to 0.1° (6m) (to prevent aliasing) using the generic mapping tools (GMT) command:
gmt grdfilter ETOPO1_Bed_g_gmt4.grd -D1 -Fg11.2 -I6m -GETOPO1_Bed_g_gmt4_6m.nc

Given the 

The original ETOPO1 dataset can be downloaded from: https://www.ncei.noaa.gov/products/etopo-global-relief-model

Reference for ETOPO1:
Amante, C. and B.W. Eakins, 2009. ETOPO1 1 Arc-Minute Global Relief Model: Procedures, Data Sources and Analysis. NOAA Technical Memorandum NESDIS NGDC-24. National Geophysical Data Center, NOAA. doi:10.7289/V5C8276M [access date]