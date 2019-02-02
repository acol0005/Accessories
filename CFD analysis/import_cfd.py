import csv
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt

filename = './results/results.csv'

def restoreNumericList(list_str):
  lst = list_str.replace('[', '').replace(']', '').split(', ')
  lst = [float(element) for element in lst]
  return lst

def restore2DList(arr_str):
  arr = [restoreNumericList(vector_str) for vector_str in arr_str]
  return arr

def restore3DList(arr_str):
  # for lst in arr_str:
  #   print(lst)
  arr = [list2d for list2d in arr_str]
  new_arr = []
  for i in range(0,len(arr)):
    arr[i] = arr[i].replace('[[','[').replace(']]',']')
    # will not work if 'xx' is in an array
    sublists = [restoreNumericList(lst) for lst in arr[i].replace(', [','xx[').split('xx')]
    new_arr.append(sublists)
  return new_arr

def readCFDData(file_name):
  # READ THE CSV
  with open(file_name, 'r') as csv_file:
    reader  = csv.reader(csv_file, delimiter=',')
    data = np.array([row for row in reader])
  csv_file.close()
  # EXTRACT DATA
  headers = data[0, :]
  data = data[1:, 2:] # ignore header, rocket, and launch location
  restore3DList(data[:, 8])
  data_dict = {
    'mach numbers': data[:, 0].astype(float),
    'pitches': data[:, 1].astype(float),
    'rolls': data[:, 2].astype(float),
    'drag vectors': np.array(restore2DList(data[:, 3])),
    'total drags': data[:, 4].astype(float),
    'c_d vectors': np.array(restore2DList(data[:, 5])),
    'total coeffs': data[:, 6].astype(float),
    'moment x locations': np.array(restore2DList(data[:, 7])),
    'moments': np.array(restore3DList(data[:, 8])),
    'c_m array': np.array(restore3DList(data[:, 9]))
    }
  return data_dict

data_obj = readCFDData(filename)
# print(data_obj['c_m array'].shape)

# # INTERPOLATE
# x = np.empty((len(mach_num),3))
# x[:, 0] = mach_num
# x[:, 1] = pitch
# x[:, 2] = roll
# drag_interp_fun = interpolate.NearestNDInterpolator(x, cd_vecs)
#
#
# # TESTING
# num_samples = 10
# pitches = np.linspace(0,15, num_samples)
# mach_nums = 0.3 * np.ones(num_samples)
# rolls = 0 * np.ones(num_samples)
#
# x_t = np.empty((num_samples,3))
# x_t[:, 0] = mach_nums
# x_t[:, 1] = pitches
# x_t[:, 2] = rolls
#
# cds = drag_interp_fun(x_t)
# # plt.plot(pitches, drags)
# # plt.xlabel('Angle of attack (deg)')
# # plt.ylabel('Drag (N)')
# # plt.show()
# print(cds)
