import time
import calendar
from calendar import monthrange
import csv

# user defined variables
c_wday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
head_line = 'Day\tDate\tCheck In\tCheck Out\tExtra pause [min.]\tHours\tNote\n'

# create an empty table for the curent month
# in the case table alredy exists it will be overwritten !!!
def make_empty_table(c_month = time.localtime(time.time()).tm_mon):
    c_year = time.localtime(time.time()) .tm_year
    days_in_month = monthrange(c_year, c_month)[1]
    table = head_line

    for i in range(0, days_in_month):
        c_date = '{:02d}.{:02d}.{}.'.format(i+1, c_month, c_year) # date format
        week_day = calendar.weekday(c_year,c_month,i+1)
        cur_line ='{0}. \t{1} \t\t\t\t\t\n'.format(c_wday[week_day][0:2], c_date)
        table += cur_line

    #DataFile = '/home/SmartSensor/PyCode/WorkEvidence/work_statistics_2020_{:02d}.csv'.format(c_month)
    DataFile = 'work_statistics_2020_{:02d}.csv'.format(c_month)
    f = open(DataFile, "w")
    f.write(table)
    f.close()
    table, table_name = write_checkin_time()
    write_table(table, table_name)
    print('Table ', table_name, ' is created')

def read_work_table(month = time.localtime(time.time()).tm_mon):
    #DataFile = '/home/SmartSensor/PyCode/WorkEvidence/work_statistics_2020_{:02d}.csv'.format(month)
    DataFile = 'work_statistics_2020_{:02d}.csv'.format(month)
    table=[]
    with open(DataFile) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            tmp = row[0].split('\t')
            table.append(tmp)
    return table, DataFile


def write_checkin_time():
    table, table_name = read_work_table()
    c_mday = time.localtime(time.time()).tm_mday
    c_hour = time.localtime(time.time()).tm_hour
    c_min = time.localtime(time.time()).tm_min
    c_sec = time.localtime(time.time()).tm_sec
    if table[c_mday][2] == '':
        table[c_mday][2] = '{:02d}:{:02d}:{:02d}'.format(c_hour,c_min,c_sec)
    return table, table_name

def write_checkout_time():
    table, table_name = read_work_table()
    # write check out time
    c_mday = time.localtime(time.time()).tm_mday
    c_hour = time.localtime(time.time()).tm_hour
    c_min = time.localtime(time.time()).tm_min
    c_sec = time.localtime(time.time()).tm_sec
    table[c_mday][3] = '{:02d}:{:02d}:{:02d}'.format(c_hour,c_min,c_sec)

    #write total time at work for current date
    ck_in = table[c_mday][2].split(':')
    work_time = (c_hour - int(ck_in[0]))*3600 + (c_min - int(ck_in[1]))*60 + c_sec - int(ck_in[2]) - int(table[c_mday][4])*60
    w_hour = work_time // 3600
    work_time = work_time-w_hour*3600
    w_min = work_time // 60
    w_sec = work_time-w_min*60
    table[c_mday][5] = '{:02d}:{:02d}:{:02d}'.format(w_hour,w_min,w_sec)

    write_table(table, table_name)


def write_pause():
    table, table_name = read_work_table()
    c_mday = time.localtime(time.time()).tm_mday
    # write pause
    pause = int(input('Enter pause duration in minutes\n\n'))
    table[c_mday][4] = '{:02d}'.format(pause)
    write_table(table, table_name)

def write_table(table, table_name):
    with open(table_name, 'w', newline='\n') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter='\t',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in table:
            spamwriter.writerow(row)


try:
    # check in time alredy writed
    table, table_name = read_work_table()
    c_mday = time.localtime(time.time()).tm_mday
    if len(table[c_mday][2]) > 2:
        operation = int(input('Insert:\n    0 \t for create work table\n    1 \t for check in\n    2 \t for check out\n    3 \t for pause in minutes\n\n'))
        #print('step 1')
    else:
        operation = 1
        #print('step 2, duzina polja je {}'.format(len(table[c_mday][2])))
except Exception as e:
        print('File for current month is not created, it will be created now.\n ')
        operation = 0



if operation == 0:
    make_empty_table()
elif operation == 1:
    table, table_name = write_checkin_time()
    write_table(table, table_name)
elif operation == 2:
    write_checkout_time()
elif operation == 3:
    write_pause()
    write_checkout_time()
