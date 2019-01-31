import csv
import numpy as np
import os

data_dir = './data/'
results_dir = './results/'
results_file_name = 'results.csv'
#angles: 0-5, 7, 11, 15, 20
density = 1.225 # kg/m^3
temp = 300 # K
radius = 0.0655 # m
a_ref = np.pi * (radius ** 2)

#file_name: <rocket>_<launch>_M<number (e.g. 0.15 is 0-15)>_PH<number (deg)>_TH<number (deg)>.csv
# file_name = '{}_{}_M{}-{}_PH{}_TH{}.csv'.format(rocket_name, launch_name, mach_int, mach_dec, pitch, roll)
# e.g. Athena_Westmar_drag_M0-15_PH0_TH0.csv

def convertMachNumber(mach_str):
  # converts mach number from format used in filenames into a string
  # e.g. from M0-15 to 0.15
  num_str = mach_str[1:]
  num_str = '.'.join(num_str.split('-'))
  return float(num_str)

def convertFileName(file_name):
  # converts the csv file's name (as set up in the journal generator script)
  # to information about the flight conditions
  file_name_no_csv = file_name[:file_name.find('.csv')]
  rocket, launch, mach_str, pitch_str, roll_str = file_name_no_csv.split('_')
  data = {
    'rocket': rocket,
    'launch': launch,
    'mach number': convertMachNumber(mach_str),
    'pitch': pitch_str[2:],
    'roll': roll_str[2:]
    }
  return data

def getSoundSpeed(temp):
  # calculates the sound speed of air at a given temperature
  R_ideal = 287.058 # J/kg-K
  gamma = 1.4
  sound_speed = np.sqrt(gamma * R_ideal * temp)
  return sound_speed

def getForceCoefficient(force, density, mach_num, temp, ref_area):
  # Return the force coefficient for a given flight condition and force
  sound_speed = getSoundSpeed(temp)
  vel = mach_num + sound_speed
  q = 0.5 * density * (vel ** 2)
  force_coeff = force/(q * ref_area)
  return force_coeff




# RUN THE SCRIPT
if __name__ == '__main__':
  # header for the results file
  results = [['Rocket', 'Launch', 'Mach Number', 'Pitch (deg)', 'Roll (deg)',
              'drag_x (N)',       'drag_y (N)',  'drag_z (N)',  'Total Drag (N)',
              'C_D_x',            'C_D_y',       'C_D_z',       'Total C_D']]

  for file_name in [name for name in os.listdir(data_dir) if name.endswith('.csv')]:
    with open(data_dir + file_name, 'r') as data_file:
      reader = csv.reader(data_file)
      data = [row for row in reader]
      # flatten rows into a single list
      flat_data = [sublist[0] for sublist in data if sublist != []]
      # extract info from file name
      info = convertFileName(file_name)
      mach_num = info['mach number']
      # remove all the data except drag vector
      drag = ['(' + item for item in ''.join(flat_data).replace('  ', '').split('(')][4]
      drag_vec = drag.replace('(', '').replace(')', '').split(' ')[0:3]
      # calculate drag coefficients in x,y,z
      coeff_vec = [np.round(getForceCoefficient(float(component), density, mach_num, temp, a_ref),3) for component in drag_vec]
      # calculate total drag and drag coefficient
      total_drag = np.round(np.linalg.norm(drag_vec), 3)
      total_coeff = np.round(np.linalg.norm(coeff_vec), 3)
      # add to results, ready to write to csv
      file_data = [info['rocket'], info['launch'], mach_num, info['pitch'], info['roll'],
                  drag_vec[0], drag_vec[1], drag_vec[2], total_drag,
                  coeff_vec[0], coeff_vec[1], coeff_vec[2], total_coeff]
      results.append(file_data)
    data_file.close()

  with open(results_dir + results_file_name, 'w') as results_file:
    writer = csv.writer(results_file)
    writer.writerows(results)
  results_file.close()
