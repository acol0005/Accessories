import csv
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt

filename = './results/results.csv'

def readCFDData(file_name):
  # READ THE CSV
  with open(file_name, 'r') as csv_file:
    reader  = csv.reader(csv_file)
    data = np.array([row for row in reader])
  csv_file.close()
  # EXTRACT DATA
  data = data[1:, 2:]
  data_dict = {
    'mach numbers': data[:, 0],
    'pitches': data[:, 1],
    'rolls': data[:, 2],
    'drag vectors': data[:, 3:6],
    'total drags': data[:, 6],
    'coeff vectors': data[:, 7:10],
    'total coeffs': data[:, 10]
    }
  return data_dict

data_obj = readCFDData(filename)

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
