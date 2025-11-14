# functions


import geopandas as gpd
import pygplates
import xarray as xr
import xesmf as xe
import shapely
import numpy as np
import pandas as pd
import rasterio


def create_geodataframe_general(pygplates_recon_geom, reconstruction_time, shapefile_attributes_list=None, flip_geom=False):
    """ This is a general function to convert reconstructed features (e.g. 
    reconstructed coastlines) from pygplates into a GeoDataFrame. This helps
    avoid plotting artefacts.
    It *should* be able to deal with either polygons OR polylines.
    
    TO DO: Make it cycle through shapefile attributes
    
    For polylines only: To make life easier for trenches, there is an additional parameter 'flip_geom'. 
    Use this to invert the order of either the left OR right trenches, so they can be plotted (e.g. using pygmt) with a single command.
    Using this parameter with a polygon won't result in any changes.
    
    Input: 
        - pygplates.ReconstructedFeatureGeometry (i.e., output of pygplates.reconstruct)
    OR 
        - pygplates.Feature
        - recontruction time - this is just for safekeeping in the geodataframe!
    Output: 
        - gpd.GeoDataFrame of the feature"""
    
    # create new and empy geodataframe
    gdf_output = gpd.GeoDataFrame()
    gdf_output['NAME'] = None
    gdf_output['PLATEID1'] = None
    gdf_output['PLATEID2'] = None
    gdf_output['FROMAGE'] = None
    gdf_output['TOAGE'] = None
    gdf_output['reconstruction_time'] = None
    
    date_line_wrapper = pygplates.DateLineWrapper()

    names = []
    plateid1s = []
    plateid2s = []
    fromages = []
    toages = []
    geometrys = []
    reconstruction_times = []
    gpml_types = []
    
    # empty lists for shapefile attributes
    if shapefile_attributes_list is not None:
        shapefile_attrs_list_output = [[] for i in range(len(shapefile_attributes_list))]
    
    for i, seg in enumerate(pygplates_recon_geom):
        
        # if pygplates is a reconstructed feature geometry:
        if isinstance(seg, pygplates.ReconstructedFeatureGeometry):
            wrapped_polygons = date_line_wrapper.wrap(seg.get_reconstructed_geometry())
            for poly in wrapped_polygons:

                # check if it's a polygon or polyline
                if isinstance(poly, pygplates.DateLineWrapper.LatLonPolygon):

                    ring = np.array([(p.get_longitude(), p.get_latitude()) for p in poly.get_exterior_points()])
                    name = seg.get_feature().get_name()
                    plateid = seg.get_feature().get_reconstruction_plate_id()
                    conjid = seg.get_feature().get_conjugate_plate_id()
                    from_age, to_age = seg.get_feature().get_valid_time()

                    # append things
                    names.append(name)
                    plateid1s.append(plateid)
                    plateid2s.append(conjid)
                    fromages.append(from_age)
                    toages.append(to_age)
                    geometrys.append(shapely.geometry.Polygon(ring))
                    reconstruction_times.append(reconstruction_time)
                    gpml_types.append(str(seg.get_feature().get_feature_type()))
                    
                    # If desired shapefile atttributes is known and listed, deal with here
                    if shapefile_attributes_list is not None:
                        # iterate to get through shapfile attributes
                        shapefile_attrs = seg.get_feature().get_shapefile_attributes()
                        if shapefile_attrs:
                            for i in range(len(shapefile_attributes_list)):
                                shapefile_attrs_list_output[i].append(shapefile_attrs.get('%s' % shapefile_attributes_list[i]))
                        else:
                            for i in range(len(shapefile_attributes_list)):
                                shapefile_attrs_list_output[i].append('None')
                
                # otherwise maybe we have a polyline
                elif isinstance(poly, pygplates.DateLineWrapper.LatLonPolyline):
                    # doesn't work with flipping, trying my other way
                    tmp = shapely.geometry.LineString([j.to_lat_lon()[::-1] for j in poly.get_points()])
                    name = seg.get_feature().get_name()
                    plateid = seg.get_feature().get_reconstruction_plate_id()
                    conjid = seg.get_feature().get_conjugate_plate_id()
                    from_age, to_age = seg.get_feature().get_valid_time()
                    
                    names.append(name)
                    plateid1s.append(plateid)
                    plateid2s.append(conjid)
                    fromages.append(from_age)
                    toages.append(to_age)
                    geometrys.append(shapely.geometry.LineString(tmp))
                    reconstruction_times.append(reconstruction_time)
                    gpml_types.append(str(seg.get_feature().get_feature_type()))
                    
                    if shapefile_attributes_list is not None:
                        # iterate to get through shapfile attributes
                        shapefile_attrs = seg.get_shapefile_attributes()
                        if shapefile_attrs:
                            for i in range(len(shapefile_attributes_list)):
                                shapefile_attrs_list_output[i].append(shapefile_attrs.get('%s' % shapefile_attributes_list[i]))
                        else:
                            for i in range(len(shapefile_attributes_list)):
                                shapefile_attrs_list_output[i].append('None')
                                
        elif isinstance(seg, pygplates.Feature):
            wrapped_polygons = date_line_wrapper.wrap(seg.get_geometry(lambda property: True))
            for poly in wrapped_polygons:

                # check if it's a polygon or polyline
                if isinstance(poly, pygplates.DateLineWrapper.LatLonPolygon):

                    ring = np.array([(p.get_longitude(), p.get_latitude()) for p in poly.get_exterior_points()])
                    name = seg.get_name()
                    plateid = seg.get_reconstruction_plate_id()
                    conjid = seg.get_conjugate_plate_id()
                    from_age, to_age = seg.get_valid_time()

                    # append things
                    names.append(name)
                    plateid1s.append(plateid)
                    plateid2s.append(conjid)
                    fromages.append(from_age)
                    toages.append(to_age)
                    geometrys.append(shapely.geometry.Polygon(ring)) 
                    reconstruction_times.append(reconstruction_time)
                    gpml_types.append(str(seg.get_feature_type()))
                    
                    if shapefile_attributes_list is not None:
                        # iterate to get through shapfile attributes
                        shapefile_attrs = seg.get_shapefile_attributes()
                        if shapefile_attrs:
                            for i in range(len(shapefile_attributes_list)):
                                shapefile_attrs_list_output[i].append(shapefile_attrs.get('%s' % shapefile_attributes_list[i]))
                        else:
                            for i in range(len(shapefile_attributes_list)):
                                shapefile_attrs_list_output[i].append('None')
                            
                elif isinstance(poly, pygplates.DateLineWrapper.LatLonPolyline):
                    tmp = shapely.geometry.LineString([j.to_lat_lon()[::-1] for j in poly.get_points()])

                    name = seg.get_name()
                    plateid = seg.get_reconstruction_plate_id()
                    conjid = seg.get_conjugate_plate_id()
                    from_age, to_age = seg.get_valid_time()

                    names.append(name)
                    plateid1s.append(plateid)
                    plateid2s.append(conjid)
                    fromages.append(from_age)
                    toages.append(to_age)
                    geometrys.append(shapely.geometry.LineString(tmp))
                    reconstruction_times.append(reconstruction_time)
                    gpml_types.append(str(seg.get_feature_type()))
                    
                    
                    if shapefile_attributes_list is not None:
                        # iterate to get through shapfile attributes
                        shapefile_attrs = seg.get_shapefile_attributes()
                        if shapefile_attrs:
                            for i in range(len(shapefile_attributes_list)):
                                shapefile_attrs_list_output[i].append(shapefile_attrs.get('%s' % shapefile_attributes_list[i]))
                        else:
                            for i in range(len(shapefile_attributes_list)):
                                shapefile_attrs_list_output[i].append('None')
                    
    # write to geodataframe
    gdf_output['NAME'] = names
    gdf_output['PLATEID1'] = plateid1s
    gdf_output['PLATEID2'] = plateid2s
    gdf_output['FROMAGE'] = fromages
    gdf_output['TOAGE'] = toages
    gdf_output['reconstruction_time'] = reconstruction_times
    gdf_output['gpml_type'] = gpml_types
    gdf_output = gdf_output.set_geometry(geometrys)
    gdf_output = gdf_output.set_crs(epsg=4326)
    
    # add the shapefile attributes
    if shapefile_attributes_list is not None:
        for i in range(len(shapefile_attributes_list)):
            gdf_output['%s' % shapefile_attributes_list[i]] = shapefile_attrs_list_output[i]
    
    return gdf_output



def regrid_to_alternative_resolution(ds_in, output_resolution, lon_min, lon_max, lat_min, lat_max, output_file, output_filename=False, regridding_algorithm="conservative", periodic=False):
    # Function to regrid xarray dataset to a different resolution.
    
    # ---- Set the target resolution.

    # if going from lower to higher resolution, 
    # "conservative and nearest_s2d will preserve the original coarse grid structure (although the data is now defined on a finer grid.)""
    # see https://xesmf.readthedocs.io/en/stable/notebooks/Compare_algorithms.html
    ds_out = xr.Dataset({"lat": (["lat"],
                                 np.arange(lat_min, lat_max + output_resolution, output_resolution), 
                                 {"units": "degrees_north", "standard_name": "latitude"}),
                         "lon": (["lon"], np.arange(lon_min, lon_max + output_resolution, output_resolution), 
                                 {"units": "degrees_east", "standard_name": "longitude"})})

    # create the Regridder
    regridder = xe.Regridder(ds_in, ds_out, regridding_algorithm, periodic=periodic)
    
    # apply the regridder. Results in a xarray.dataset
    ds_out_newres = regridder(ds_in, keep_attrs=True)

    # update the title to reflect the new resolution
    try:
        previous_title = ds_in.attrs['title']
        ds_out_newres.attrs['title'] = '%s, regridded to %sx%s degrees' % (previous_title, output_resolution, output_resolution)
    except KeyError:
        ds_out_newres.attrs['title'] = 'regridded to %sx%s degrees' % (output_resolution, output_resolution)

    # Save file if desired
    if output_filename is True:
        # save file
        comp = dict(zlib=True, complevel=5)
        encoding = {var: comp for var in ds_out_newres.data_vars}
    
        ds_out_newres.to_netcdf(output_file, mode='w', compute=True, encoding=encoding, format="NETCDF4_CLASSIC")
    else:
        pass
    
    return ds_out_newres


def read_rotation_file_pandas(rotation_file_path):
    rotation_file = pd.read_csv(rotation_file_path, names=['PLATEID1', 'age', 'lat', 'lon', 'angle', 'PLATEID2', 'comment'],
                                sep=r'\s+', comment='!')
    
    # get comments. This is hard to do with pandas only, so reading in the file again
    with open(rotation_file_path, 'r') as f:
        lines = f.readlines()
        output = []

        comment = '!'
        for line in lines:
            head, sep, tail = line.partition(comment)
            tail = tail.strip('\n')
            output.append(tail)
        
    rotation_file['comment'] = output
    
    return rotation_file


def convert_gdf_to_raster(gdf, z_column, fill_value=np.nan, grid_spacing=0.1, lon_min=-180, lon_max=180, lat_min=-90, lat_max=90):
    """
    Convert geodataframe into a netcdf using rasterio/rasterize
    Defaults to 0.1° and -180/180/-90/90.
    Then pass the raster to xarray, so we can save the netcdf out nicely.

    """
    # Specify. Otherwise default to 0.1° -180/180/-90/90
    
    # print('...... Defaulting to 0.1° global grid')
    lat_shape = int((180 / grid_spacing) + 1)
    lon_shape = int((360 / grid_spacing) + 1)

    output_shape = (lat_shape, lon_shape)

    output_transform = rasterio.Affine(
        grid_spacing, 0.0, lon_min - (grid_spacing/2), 0.0, grid_spacing, lat_min -(grid_spacing/2))
    # NOTE ref point is bottom left corner)
    lats = np.arange(lat_min, lat_max + grid_spacing, grid_spacing)
    lons = np.arange(lon_min, lon_max + grid_spacing, grid_spacing)

    # convert geometries to raster based on HEIGHT column
    raster = rasterio.features.rasterize([(x.geometry, x[z_column]) for i, x in gdf.iterrows()],
                                         out_shape=output_shape,
                                         transform=output_transform,
                                         fill=fill_value,
                                         all_touched=True)

    # convert to xarray, since that makes saving it out nicely easier
    da_raster = xr.DataArray(raster, coords=[lats, lons], dims=('lat', 'lon'), name='z')

    # convert to dataset and add some attributes
    ds_raster = da_raster.to_dataset()

    # round lats and lons, to ensure we can safely add them
    # because xarray is annoying sometimes
    ds_raster['lat'] = np.round(ds_raster.lat.values, 3)
    ds_raster['lon'] = np.round(ds_raster.lon.values, 3)

    ds_raster['z'].attrs = {
        'actual_range': np.array([np.nanmin(ds_raster.z), np.nanmax(ds_raster.z)], dtype=np.float32)}
    ds_raster['lat'].attrs = {
        'long_name': "latitude", 'standard_name': "latitude", 'units': "degrees_north",
        'actual_range': np.array([np.nanmin(ds_raster.lat), np.nanmax(ds_raster.lat)], dtype=np.float32)}
    ds_raster['lon'].attrs = {
        'long_name': "longitude", 'standard_name': "longitude", 'units': "degrees_east",
        'actual_range': np.array([np.nanmin(ds_raster.lon), np.nanmax(ds_raster.lon)], dtype=np.float32)}
        
    # global attributes
    # ds_raster.attrs['history'] = "created %s" % (
    #     datetime.now().strftime('%Y-%m-%d %H:%M'))
    # compress so it doesn't take a ridiculous amount of space!
    # comp = dict(zlib=True, complevel=5)
    # encoding = {var: comp for var in ds_raster.data_vars}

    # ds_lip_raster.to_netcdf('%s/reconstructed_%s_%sMa.nc' % (path_output_grids, feature_type, time), encoding=encoding)
    return ds_raster


def gplately_raster_to_xarray(raster, raster_name, raster_units):
    
    # check the order of lats
    if raster.lats.min () < raster.lats.max():
        ds_raster = xr.Dataset(data_vars=dict(z=(["lat", "lon"], 
                                                 raster.data, {"long_name": raster_name,
                                                               "units": raster_units,
                                                               "actual_range": np.array([np.nanmin(raster.data), np.nanmax(raster.data)], dtype=np.float32)})),
                               coords=dict(lon=(["lon"], raster.lons.astype('float32'),
                                                {"long_name": "longitude", "units": "degrees_east", "standard_name": "longitude", 
                                                 "actual_range": np.array([raster.lons.min(), raster.lons.max()], dtype=np.float32)}),
                                           lat=(["lat"], (raster.lats).astype('float32'),
                                                {"long_name": "latitude", "units": "degrees_north", "standard_name": "latitude", 
                                                 "actual_range": np.array([raster.lats.min(), raster.lats.max()], dtype=np.float32)})))
    else:
        # otherwise the lats are in DESCENDING order, which means we need to flip the data and lats (otherwise the grid will be upside down later)
        ds_raster = xr.Dataset(data_vars=dict(z=(["lat", "lon"],
                                                 np.flipud(raster.data), {"long_name": raster_name,
                                                                          "units": raster_units,
                                                                          "actual_range": np.array([np.nanmin(raster.data), np.nanmax(raster.data)], dtype=np.float32)})),
                               coords=dict(lon=(["lon"], raster.lons.astype('float32'),
                                                {"long_name": "longitude", "units": "degrees_east", "standard_name": "longitude", 
                                                 "actual_range": np.array([raster.lons.min(), raster.lons.max()], dtype=np.float32)}),
                                           lat=(["lat"], np.flipud(raster.lats).astype('float32'),
                                                {"long_name": "latitude", "units": "degrees_north", "standard_name": "latitude", 
                                                 "actual_range": np.array([raster.lats.min(), raster.lats.max()], dtype=np.float32)})))
        
    return ds_raster



# def convert_shapefile_to_raster(gdf, z_column, fill_value, grid_spacing=0.1, lon_min=-180, lon_max=180, lat_min=-90, lat_max=90):
#     """
#     Convert LIP shapefile (as geodataframe) into a netcdf using rasterio/rasterize
#     Defaults to 0.1° and -180/180/-90/90.
#     Then pass the raster to xarray, so we can save the netcdf out nicely.

#     """
    
#     # lon_min = -180
#     # lon_max = 180
#     # lat_min = -90
#     # lat_max = 90
    
#     lat_shape = int((180 / grid_spacing) + 1)
#     lon_shape = int((360 / grid_spacing) + 1)
    
#     output_shape = (lat_shape, lon_shape)

#     output_transform = rasterio.Affine(
#         grid_spacing, 0.0, lon_min - (grid_spacing/2), 0.0, grid_spacing, lat_min -(grid_spacing/2))
#     # NOTE ref point is bottom left corner)
#     lats = np.arange(lat_min, lat_max + grid_spacing, grid_spacing)
#     lons = np.arange(lon_min, lon_max + grid_spacing, grid_spacing)
    
#     # convert geometries to raster based on z_column
#     raster = rasterio.features.rasterize([(x.geometry, x[z_column]) for i, x in gdf.iterrows()],
#                                              out_shape=output_shape,
#                                              transform=output_transform,
#                                              fill=fill_value,
#                                              all_touched=True)

#     # convert to xarray, since that makes saving it out nicely easier
#     da_raster = xr.DataArray(raster, coords=[lats, lons], dims=('lat', 'lon'), name='z')

#     # convert to dataset and add some attributes
#     ds_raster = da_raster.to_dataset()

#     # round lats and lons, to ensure we can safely add them
#     # because xarray is annoying sometimes
#     ds_raster['lat'] = np.round(ds_raster.lat.values, 2)
#     ds_raster['lon'] = np.round(ds_raster.lon.values, 2)

#     ds_raster['z'].attrs = {'actual_range': np.array([np.nanmin(ds_raster.z), 
#                                                       np.nanmax(ds_raster.z)], dtype=np.float32)}
#     ds_raster['lat'].attrs = {'long_name': "latitude", 'standard_name': "latitude", 
#                               'units': "degrees_north", 'actual_range': 
#                               np.array([np.nanmin(ds_raster.lat), np.nanmax(ds_raster.lat)], dtype=np.float32)}
#     ds_raster['lon'].attrs = {'long_name': "longitude", 'standard_name': "longitude", 'units': "degrees_east",
#         'actual_range': np.array([np.nanmin(ds_raster.lon), np.nanmax(ds_raster.lon)], dtype=np.float32)}

#     return ds_raster