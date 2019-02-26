from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import os
import csv
# os.environ['PROJ_LIB'] = 'anaconda3/envs/HPR_py3/share/proj'
from mpl_toolkits.basemap import Basemap


file_name = 'james.nc' #NETCDF3_CLASSIC FILE
file_path = os.path.join(os.getcwd(), file_name)

dataset = Dataset(file_path)
dimensions = dataset.dimensions
variables = dataset.variables

# longitude and latitude of the location to average around (Westmar)
WM_LONG = 149.6498806
WM_LAT = -28.1767682

lat = np.array(variables['lat'][:])
long = np.array(variables['lon'][:])
ncl0 = dimensions['ncl0']
vel_u = np.array(variables['U'][:,:,:]) # ordering: ncl0, lat, long
vel_v = np.array(variables['V'][:,:,:])
vel_w = np.array(variables['W'][:,:,:])

vel_mag_sq = vel_u**2 + vel_v**2 + vel_w**2
vel_mag = np.power(vel_mag_sq, 0.5) # velocity magnitudes

# find the indices of the nearest data points to Westmar's location
WM_LAT_INDEX = np.abs(lat - WM_LAT).argmin()
WM_LONG_INDEX = np.abs(long - WM_LONG).argmin()

METRES_TO_FEET = 3.28084

# print('actual location: ({},{})'.format(WM_LAT, WM_LONG))
# print('nearest data point: ({},{})'.format(lat[WM_LAT_INDEX], long[WM_LONG_INDEX]))

header_row = ['altitude (m)', 'wind speed (m/s)', 'u component (m/s)', 'v component (m/s)', 'w component (m/s)', 'wind direction (degrees clockwise from true north)']

# get the indices of the 5x5 square of data points centered on Westmar
row_filter = np.array([-2, -1, 0, 1, 2])
lat_inds = WM_LAT_INDEX + row_filter
lon_inds = WM_LONG_INDEX + row_filter

total_latlon_pts = len(lat_inds) * len(lon_inds)
avg_vel_mags = np.zeros(ncl0.size)
avg_vel_u = np.zeros(ncl0.size)
avg_vel_v = np.zeros(ncl0.size)
avg_vel_w = np.zeros(ncl0.size)
alts = np.zeros(ncl0.size)
directions = np.zeros(ncl0.size)

for height_index in range(0,ncl0.size):
  vel_mag_sum = 0
  vel_u_sum = 0
  vel_v_sum = 0
  vel_w_sum = 0
  for lat_index in lat_inds:
    for lon_index in lon_inds:
      vel_mag_sum += vel_mag[height_index, lat_index, lon_index]
      vel_u_sum += vel_u[height_index, lat_index, lon_index]
      vel_v_sum += vel_v[height_index, lat_index, lon_index]
      vel_w_sum += vel_w[height_index, lat_index, lon_index]

  vel_mag_avg = vel_mag_sum / total_latlon_pts
  vel_u_avg = vel_u_sum / total_latlon_pts
  vel_v_avg = vel_v_sum / total_latlon_pts
  vel_w_avg = vel_w_sum / total_latlon_pts


  direction = np.rad2deg(np.arctan2(vel_v_avg, vel_u_avg)) # using convention of (-pi, pi]
  # convert to [0deg, 360deg)
  direction = (270- direction) % 360
  # print('direction: {:6.2f}deg, vector: ({:3.1f},{:3.1f})'.format(np.round(direction,2), np.round(vel_u_avg,0), np.round(vel_v_avg,0)))

  directions[height_index] = direction
  avg_vel_mags[height_index] = vel_mag_avg
  avg_vel_u[height_index] = vel_u_avg
  avg_vel_v[height_index] = vel_v_avg
  avg_vel_w[height_index] = vel_w_avg
  alts[height_index] = (2000 * height_index) / METRES_TO_FEET

data = np.stack((np.around(alts,1), np.around(avg_vel_mags,2),
                np.around(avg_vel_u,2), np.around(avg_vel_v,2), np.around(avg_vel_w,2),
                np.around(directions, 1)))

# write to csv
file_name = 'wind_model.csv'
with open(file_name, 'w') as csv_file:
  writer = csv.writer(csv_file)
  writer.writerow(header_row)
  for row_ind in range(0,ncl0.size):
    writer.writerow(data.T[row_ind, :])


# PLOTTING FOR INVESTIGATION
# print('magnitudes')
# print(avg_vel_mags)
# print('u')
# print(avg_vel_u)
# print('v')
# print(avg_vel_v)
# print('w')
# print(avg_vel_w)

# lat_mean = lat.mean()
# lon_mean = long.mean()
# low_left_corner_lat = lat.max()
# low_left_corner_long = long.min()
# up_right_corner_lat = lat.min()
# up_right_corner_long = long.max()

# map = Basemap(resolution='l',projection='ortho',lat_ts=40,
#             lat_0=lat_mean,lon_0=lon_mean)#,
#             # llcrnrlat=low_left_corner_lat,llcrnrlon=low_left_corner_long,
#             # urcrnrlat=up_right_corner_lat,urcrnrlon=up_right_corner_long)
#
# map.drawcoastlines(linewidth=0.25)
# # Because our lon and lat variables are 1D,
# # use meshgrid to create 2D arrays
# # Not necessary if coordinates are already in 2D arrays.
# lon, lat = np.meshgrid(long, lat)
# xi, yi = map(lon, lat)
# # Plot Data
# cs = map.pcolormesh(xi,yi,vel_u[0,:,:])
# map.plot(WM_LONG, WM_LAT, 'ro', latlon=True) # draw a point for westmar
# plt.show()
