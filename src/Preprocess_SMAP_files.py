"""
Script to extract JPEG image file from SMAP HDF5 file

Inputs: SMAP L4 HDF5 files

Outputs: uint8 type soil moisture JPEG image files
         uint8 type precipitation JPEG image files

Author: Archana Kannan (kannana@usc.edu)
"""

# Normalization to 0-255
# NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
# OldMin = 0
# OldMax = 0.9
# NewMin = 255
# NewMax = 0

# Imports
import h5py
import numpy as np
import datetime
from PIL import Image
import pandas as pd

# File paths
path_in = '/Volumes/Seagate/Mixil/SMAP_L4_raw/2021/'
path_out = '/Users/archanakannan/Desktop/Archana/USC/Codes/pythonProject/DSHIELD/SMAP_2021/'

# Dates
start = datetime.datetime(2021,6,30,1,30,0) # START DATETIME
end = datetime.datetime(2021,12,31,22,30,0) # END DATETIME
delta = datetime.timedelta(hours=3) # DELTA T. For SMAP L4 DELTA=3hours

# While loop to extract images for specified dates
while start <= end:
    d = start.strftime("%Y%m%d%H%M%S")
    f = h5py.File(path_in+'SMAP_L4_SM_gph_'+d[0:8]+'T'+d[8:]+'_Vv6030_001.h5','r') # The downloaded file format. If needed include path.
    # Note the file formats, it might change with new SMAP L4 versions
    
    GD_hdf = f.get('Geophysical_Data')
    lat = f.get('cell_lat')
    lon = f.get('cell_lon')
    sm_surface_np = np.array(GD_hdf.get('sm_surface'))
    temp_np = np.array(GD_hdf.get('surface_temp'))
    ppt_np = np.array(GD_hdf.get('precipitation_total_surface_flux'))

    sm_CONUS = sm_surface_np[150:550, 500:1300]
    ppt_CONUS = ppt_np[150:550, 500:1300]
    temp_CONUS = temp_np[150:550, 500:1300]
    lat_CONUS = lat[150:550, 500:1300]
    lon_CONUS = lon[150:550, 500:1300]

    sm_global = sm_surface_np
    ppt_global = ppt_np
    temp_global = temp_np
    lat_global = lat
    lon_global = lon
    
    # Script calculates CONUS images as well, replace "_global" with "_CONUS" for CONUS images
    data_sm = sm_global
    data_PPT = ppt_global
    data_temp = temp_global

    # For PPT range change and converting to uint8
    data_PPT = np.where((data_PPT >= 0) & (data_PPT < 10 ** -20), 255, data_PPT)
    data_PPT = np.where((data_PPT >= 10 ** -20) & (data_PPT < 10 ** -10), 245, data_PPT)
    data_PPT = np.where((data_PPT >= 10 ** -10) & (data_PPT < 10 ** -8), 225, data_PPT)
    data_PPT = np.where((data_PPT >= 10 ** -8) & (data_PPT < 10 ** -6), 205, data_PPT)
    data_PPT = np.where((data_PPT >= 10 ** -6) & (data_PPT < 10 ** -4), 185, data_PPT)
    data_PPT = np.where((data_PPT >= 10 ** -4) & (data_PPT < 10 ** -3), 165, data_PPT)
    data_PPT = np.where((data_PPT >= 0.001) & (data_PPT < 0.001), 145, data_PPT)
    data_PPT = np.where((data_PPT >= 0.002) & (data_PPT < 0.003), 125, data_PPT)
    data_PPT = np.where((data_PPT >= 0.003) & (data_PPT < 0.004), 105, data_PPT)
    data_PPT = np.where((data_PPT >= 0.004) & (data_PPT < 0.005), 95, data_PPT)
    data_PPT = np.where((data_PPT >= 0.005) & (data_PPT < 0.006), 85, data_PPT)
    data_PPT = np.where((data_PPT >= 0.006) & (data_PPT < 0.007), 75, data_PPT)
    data_PPT = np.where((data_PPT >= 0.007) & (data_PPT < 0.008), 65, data_PPT)
    data_PPT = np.where((data_PPT >= 0.008) & (data_PPT < 0.009), 55, data_PPT)
    data_PPT = np.where((data_PPT >= 0.009) & (data_PPT < 0.01), 45, data_PPT)
    data_PPT = np.where((data_PPT >= 0.01) & (data_PPT < 0.02), 35, data_PPT)
    data_PPT = np.where((data_PPT >= 0.02) & (data_PPT < 0.03), 25, data_PPT)
    data_PPT = np.where((data_PPT >= 0.03) & (data_PPT < 0.04), 15, data_PPT)
    data_PPT = np.where((data_PPT >= 0.04) & (data_PPT < 0.05), 5, data_PPT)
    data_PPT = np.where(data_PPT == -9999, 0, data_PPT)
    data_PPT = data_PPT.astype(np.uint8)

    # For SM changing range and converting to uint8
    OldMin = 0
    OldMax = 0.9
    NewMin = 255
    NewMax = 0
    data_sm = np.where(data_sm != -9999, ((((data_sm - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin), data_sm)
    data_sm = np.where(data_sm == -9999, 0, data_sm)
    data_sm = data_sm.astype(np.uint8)

    # Converting numpy array to image and saving the image with extension .jpeg
    im_SM = Image.fromarray(data_sm)
    im_PPT = Image.fromarray(data_PPT)
    im_temp = Image.fromarray(data_temp)
    im_SM.save(path_out + "SMAP_SM_2021/" + d + "_sm" + ".jpeg")
    im_PPT.save(path_out + "SMAP_PPT_2021/" + d + "_ppt" + ".jpeg")
    start += delta
    
