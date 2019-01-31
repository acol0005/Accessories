import csv
import os
import matplotlib.pyplot as plt
import numpy as np

METRES_TO_FEET = 3.28084

def readFile(file_name):
  global METRES_TO_FEET
  if os.path.exists('data/{}'.format(file_name)):
    with open('data/{}'.format(file_name), 'r') as csv_file:
      reader = csv.reader(csv_file)
      pressure = []
      alt = []
      temp = []
      dew_point = []
      wind_dir = []
      wind_speed = []
      for row in reader:
        if '-9999' in row: # fix rows with bad data
          # for index in range(0, len(row)):
          #   item = row[index]
          #   if item == '-9999':
          #     row[index] = 'NaN' # I don't know what to replace the bad entries with tbh
          print('bad boi')
          os.remove('./data/{}'.format(file_name))
          break
        if reader.line_num > 1: # don't include the headers
          pressure.append(float(row[0]))
          alt.append(float(row[1]))
          temp.append(float(row[2]))
          dew_point.append(float(row[3]))
          wind_dir.append(float(row[4]))
          wind_speed.append(float(row[5]))
      csv_file.close()
    data_dict = {'pressure': pressure,
              'altitude': alt, #metres
              'temperature': temp, #degC
              'dew point': dew_point, #degC
              'wind direction': wind_dir, #degrees
              'wind speed': wind_speed #knots
              }
    # check for empty datasets
    for key, val in data_dict.items():
      is_empty = True
      if val != []:
        is_empty = False
    if is_empty:
      os.remove('data/' + file_name) # get rid of empty data
      return -1 # data was empty
    else:
      return data_dict
  else:
    return -1 # couldn't find the file


# RUN THE FILE
if __name__ == '__main__':
  # date_list = ['20190111', '20190110', '20190107', '20190106',
  #               '20190104', '20190103', '20190101', '20181230',
  #               '20181228', '20181221', '20181217', '20181216',
  #               '20181215', '20181214', '20181213', '20181212',
  #               '20181209', '20181207', '20181205', '20181202']
  #
  # comp_date_list = ['20180401', '20180403', '20180406', '20180408',
  #                   '20180413', '20180414', '20180415', '20180420',
  #                   '20180422', '20180423', '20180424', '20180427']

  # fig = plt.figure()
  # plt.suptitle('Moree Weather Data - for April in 2002 - 2018')
  # plt.tight_layout()

  # CREATE MATRICES TO STORE THE DATA WE WANT TO AVERAGE (interpolated at pre-determined altitudes)
  # Initially only going up to 40k feet to save computation and read-in time
  # Increments of 100 feet (? not sure what else to pick)
  alt_max_ft = 100000
  alt_inc_ft = 50
  alt_max = alt_max_ft / METRES_TO_FEET
  alt_inc = alt_inc_ft / METRES_TO_FEET
  alt_std = np.arange(0, alt_max, alt_inc)
  num_files = len([name for name in os.listdir('./data/') if name.endswith('.csv')])

  big_alt = np.zeros((len(alt_std),num_files))
  big_temp = np.zeros((len(alt_std),num_files))
  big_pressure = np.zeros((len(alt_std),num_files))
  big_dew_pt = np.zeros((len(alt_std),num_files))
  big_wind_dir = np.zeros((len(alt_std),num_files))
  big_wind_spd = np.zeros((len(alt_std),num_files))

  count = 0

  for file in [name for name in os.listdir('./data/') if name.endswith('.csv')]:
  # file = '95527-20180420.csv'
    data = readFile(file)
    if data == -1: # don't analyse empty data
      # continue
      pass
    else:
      # PLOTTING TO SEE WHAT WE'RE DEALING WITH
      # plt.subplot(221)
      # plt.plot(data['wind speed'], np.array(data['altitude']) * METRES_TO_FEET, '.')
      # plt.subplot(222)
      # plt.plot(data['wind direction'], np.array(data['altitude']) * METRES_TO_FEET, '.')
      # plt.subplot(223)
      # plt.plot(data['temperature'], np.array(data['altitude']) * METRES_TO_FEET, '.')
      # plt.subplot(224)
      # plt.plot(data['pressure'], np.array(data['altitude']) * METRES_TO_FEET, '.')

      # INTERPOLATE
      interp_wind_spd = np.interp(alt_std, data['altitude'], data['wind speed'])
      interp_wind_dir = np.interp(alt_std, data['altitude'], data['wind direction'])
      interp_temp = np.interp(alt_std, data['altitude'], data['temperature'])
      interp_pressure = np.interp(alt_std, data['altitude'], data['pressure'])
      interp_dew_point = np.interp(alt_std, data['altitude'], data['dew point'])

      big_wind_spd[:, count] = interp_wind_spd
      big_wind_dir[:, count] = interp_wind_dir
      big_temp[:, count] = interp_temp
      big_pressure[:, count] = interp_pressure
      big_dew_pt[:, count] = interp_dew_point

      count += 1

  avg_wind_spd = np.around(np.mean(big_wind_spd, axis=1, dtype=np.float64), 2)
  avg_wind_dir = np.around(np.mean(big_wind_dir, axis=1, dtype=np.float64), 2)
  avg_temp = np.around(np.mean(big_temp, axis=1, dtype=np.float64), 2)
  avg_pressure = np.around(np.mean(big_pressure, axis=1, dtype=np.float64), 2)
  avg_dew_pt = np.around(np.mean(big_dew_pt, axis=1, dtype=np.float64), 2)

  alt_std = np.around(alt_std, 1)

  # # ISA temp/pressure for comparison
  # p0 = 101325
  # T0 = 288.15
  # h = alt_std
  # p = p0 * np.power((1 - 0.0065 * h / T0), 5.2561) / 100
  # h_trop = np.arange(0, 11000, 50)
  # T_trop = T0 - h_trop/1000 * 6.5
  # h_pause = np.arange(11000, 20000, 50)
  # T_pause = h_pause * 0 + 216.65
  # h_strat = np.arange(20000, 32000, 50)
  # T_strat = 216.65 + (h_strat-20000)/1000 * 1.0
  #
  # T = np.concatenate((T_trop, T_pause, T_strat), axis=None)
  # h_temp = np.concatenate((h_trop, h_pause, h_strat), axis = None)
  # T = T - 273.15

  plt.subplot(221)
  # plt.axis([0, 70, 0, 35000])
  plt.plot(avg_wind_spd, alt_std * METRES_TO_FEET, 'r-')
  plt.xlabel('Wind Speed (knots)')
  plt.ylabel('Altitude (ft)')

  plt.subplot(222)
  # plt.axis([0, 360, 0, 35000])
  plt.plot(avg_wind_dir, alt_std * METRES_TO_FEET, 'r-')
  plt.xlabel('Wind direction (deg)')
  plt.ylabel('Altitude (ft)')

  plt.subplot(223)
  plt.plot(avg_temp, alt_std * METRES_TO_FEET, 'r-')
  # plt.plot(T, h_temp * METRES_TO_FEET, 'b-')
  plt.xlabel('Temperature (degC)')
  plt.ylabel('Altitude (ft)')

  plt.subplot(224)
  plt.plot(avg_pressure, alt_std * METRES_TO_FEET, 'r-')
  # plt.plot(p, alt_std * METRES_TO_FEET, 'b-')
  plt.xlabel('Pressure (hPa)')
  plt.ylabel('Altitude (ft)')

  plt.tight_layout()
  plt.show()

  # WRITE TO A CSV
  # csv_data = [['Pressure (hPa)', 'ICAO Height (m)', 'Temperature (C)', 'Dew Point (C)', 'Wind Direction (degree)', 'Wind Speed (knots)']]
  # row_num = 0
  #
  # while row_num < len(alt_std):
  #   csv_data.append([avg_pressure[row_num], alt_std[row_num], avg_temp[row_num], avg_dew_pt[row_num], avg_wind_dir[row_num], avg_wind_spd[row_num]])
  #   row_num += 1
  #
  # with open('april_avg_profile.csv', 'w') as csv_file:
  #   writer = csv.writer(csv_file)
  #   writer.writerows(csv_data)
  # csv_file.close()
