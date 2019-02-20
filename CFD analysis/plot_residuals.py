import numpy as np
import csv, os
import matplotlib.pyplot as plt

#file_name: <rocket>_<launch>_M<number (e.g. 0.15 is 0-15)>_PH<number (deg)>_TH<number (deg)>.csv
# file_name = '{}_{}_M{}-{}_PH{}_TH{}.csv'.format(rocket_name, launch_name, mach_int, mach_dec, pitch, roll)

# Written by: Hamish Self
# Date modified: 20/2/2019

# OPTIONS
#===============================================================================
residual_dir = './residuals/' # location of .out files
plots_dir = './residual plots/' # location to save plots
axes = ['x', 'y', 'z'] # axes to plot
img_format = '.png' # plot file type
#===============================================================================

def getData(file_loc):
  with open(file_loc, 'r') as res_file:
    reader = csv.reader(res_file, delimiter=' ')
    raw_data = [row for row in reader]
  # remove headers
  clean_data = np.array(raw_data[3:])
  iters = clean_data[:, 0].astype(int)
  residuals = clean_data[:, 1].astype(float)
  return iters, residuals


# RUN THE SCIPT
#===============================================================================
if __name__ == '__main__':
  # files' names without '-x','-y','-z', or '.out' at the end
  files = [file[:-6] for file in os.listdir(residual_dir)]
  # remove repeat entries by converting to a set and back to a list
  files_set= set(files)
  files = list(files_set)
  # loop
  for f in files:
    legend = []
    for ax in axes:
      file_loc = '{}{}-{}.out'.format(residual_dir, f, ax)
      if os.path.exists(file_loc): # only access files that exist
        iters, residuals = getData(file_loc)
        legend.append(ax)
        plt.plot(iters, residuals)
      else:
        pass
    plt.xlabel('iterations')
    plt.ylabel('C_d')
    plt.title(f)
    plt.tight_layout()
    plt.legend(legend)
    # plt.show()
    plt.savefig(plots_dir + f + img_format, bbox_inches='tight')
    plt.clf()
