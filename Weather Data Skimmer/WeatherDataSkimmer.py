import urllib3 as u
import csv

def clean(content):
  # Clean it up
  start_index = content.find('[Trace]\\n')
  content = content[start_index + 9:] # get rid of html header garbage
  end_index = content.rfind('\\n[$]')# get rid of junk at the end of the file
  content = content[: end_index]
  data = content.replace('\\n', ', ') # remove the newline characters
  data = data.split(', ') # split into individual data points
  return data

def format(data):
  # format for csv writing
  row_start = 0
  csv_data = []
  while row_start < len(data):
    if row_start != 6:
      csv_data.append(data[row_start: row_start + 6])
    row_start += 6
  return csv_data

def writeCSV(filename, csv_data):
  # Write it to a csv
  with open('data/{}'.format(filename), 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(csv_data)
  csv_file.close()

def getData(location, time, file_name):
  # Get the data from the page
  http = u.PoolManager()
  # URL for the data from Australian Atmospheric Soundings
  url = 'http://slash.dotat.org/cgi-bin/atmos?raw=1&loc={}&time={}'.format(location, time)
  response = http.request('GET', url)
  content = str(response.data)
  data = clean(content)
  csv_data = format(data)
  writeCSV(file_name, csv_data)

# RUN THE SCRIPT
if __name__ == '__main__':
  location = 95527 # MOREE
  # date_list = ['20190111', '20190110', '20190107', '20190106',
  #               '20190104', '20190103', '20190101', '20181230',
  #               '20181228', '20181221', '20181217', '20181216',
  #               '20181215', '20181214', '20181213', '20181212',
  #               '20181209', '20181207', '20181205', '20181202']
  #
  # comp_date_list = ['20180401', '20180403', '20180406', '20180408',
  #                   '20180413', '20180414', '20180415', '20180420',
  #                   '20180422', '20180423', '20180424', '20180427']

  month_str = '04'

  for year in range(2002, 2019):
    for day in range(1, 31):
      if day < 10:
        day = '0' + str(day)
      date = str(year) + month_str + str(day)
      time = date + '000000'
      file_name = '{}-{}.csv'.format(location, date)
      getData(location, time, file_name)
