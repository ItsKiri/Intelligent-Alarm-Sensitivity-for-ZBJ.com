import numpy as np
import scipy.signal


file = open('hostname.csv', 'r')
hostname_list = file.readline().split(",")
file.close()
result = open('time_result.csv', 'w')
lines = 'hostname'+','+'cpu_idle'+','+'mem'+','+'disk'+','+'diskio' + \
        ','+'diskior'+','+'diskiow'+','+'netss'+'\n'
result.write(lines)
threshold = open('result.csv', 'r')
threshold_list = []
while 1:
    line = threshold.readline()
    if not line:
        break
    pass
    threshold_list.append(line)
threshold.close()
cpu_threshold = []
mem_threshold = []
disk_threshold = []
diskio_threshold = []
diskior_threshold = []
diskiow_threshold = []
netss_threshold = []
for i in threshold_list:
    cpu = float(i.split(',')[1])
    cpu_threshold.append(cpu)
    mem = float(i.split(',')[2])
    mem_threshold.append(mem)
    disk = float(i.split(',')[3])
    disk_threshold.append(disk)
    diskio = float(i.split(',')[4])
    diskio_threshold.append(diskio)
    diskior = float(i.split(',')[5])
    diskior_threshold.append(diskior)
    diskiow = float(i.split(',')[6])
    diskiow_threshold.append(diskiow)
    netss = float(i.split(',')[7])
    netss_threshold.append(netss)
minValue = 5
maxValue = 30
for i in range(len(hostname_list)):
    filename = hostname_list[i] + '_full.csv'
    file = open(filename, 'r')
    information_list = []
    while 1:
        line = file.readline()
        if not line:
            break
        pass
        information_list.append(line)
    file.close()
    x_list = []
    cpu_list = []
    mem_list = []
    disk_list = []
    diskio_list = []
    diskior_list = []
    diskiow_list = []
    netss_list = []
    cpu_duration = []
    mem_duration = []
    disk_duration = []
    diskio_duration = []
    diskior_duration = []
    diskiow_duration = []
    netss_duration = []
    for information in information_list:
        x = int(information.split(',')[0])
        x_list.append(x)
        cpu = float(information.split(',')[3])
        cpu_list.append(cpu)
        mem = float(information.split(',')[4])
        mem_list.append(mem)
        disk = float(information.split(',')[5])
        disk_list.append(disk)
        diskio = float(information.split(',')[6])
        diskio_list.append(diskio)
        diskior = float(information.split(',')[7])
        diskior_list.append(diskior)
        diskiow = float(information.split(',')[8])
        diskiow_list.append(diskiow)
        netss = float(information.split(',')[9])
        netss_list.append(netss)
    j = 0
    while j < len(cpu_list):
        count = 0
        while cpu_list[j+count] < cpu_threshold[i]:
            count += 1
            if j + count >= len(cpu_list):
                break
        if count > minValue and count < maxValue:
            cpu_duration.append(count)
        elif count >= maxValue:
            cpu_duration.append(minValue)
        elif count == 0:
            count = 1
        j += count
    j = 0
    while j < len(mem_list):
        count = 0
        while mem_list[j+count] > mem_threshold[i]:
            count += 1
            if j + count >= len(mem_list):
                break
        if count > minValue and count < maxValue:
            mem_duration.append(count)
        elif count >= maxValue:
            mem_duration.append(minValue)
        elif count == 0:
            count = 1
        j += count
    j = 0
    while j < len(disk_list):
        count = 0
        while disk_list[j+count] > disk_threshold[i]:
            count += 1
            if j + count >= len(disk_list):
                break
        if count > minValue and count < maxValue:
            disk_duration.append(count)
        elif count >= maxValue:
            disk_duration.append(minValue)
        elif count == 0:
            count = 1
        j += count
    j = 0
    while j < len(diskio_list):
        count = 0
        while diskio_list[j+count] > diskio_threshold[i]:
            count += 1
            if j + count >= len(diskio_list):
                break
        if count > minValue and count < maxValue:
            diskio_duration.append(count)
        elif count >= maxValue:
            diskio_duration.append(minValue)
        elif count == 0:
            count = 1
        j += count
    j = 0
    while j < len(diskior_list):
        count = 0
        while diskior_list[j+count] > diskior_threshold[i]:
            count += 1
            if j + count >= len(diskior_list):
                break
        if count > minValue and count < maxValue:
            diskior_duration.append(count)
        elif count >= maxValue:
            diskior_duration.append(minValue)
        elif count == 0:
            count = 1
        j += count
    j = 0
    while j < len(diskiow_list):
        count = 0
        while diskiow_list[j+count] > diskiow_threshold[i]:
            count += 1
            if j + count >= len(diskiow_list):
                break
        if count > minValue and count < maxValue:
            diskiow_duration.append(count)
        elif count >= maxValue:
            diskiow_duration.append(minValue)
        elif count == 0:
            count = 1
        j += count
    j = 0
    while j < len(netss_list):
        count = 0
        while netss_list[j+count] > netss_threshold[i]:
            count += 1
            if j + count >= len(netss_list):
                break
        if count > minValue and count < maxValue:
            netss_duration.append(count)
        elif count >= maxValue:
            netss_duration.append(minValue)
        elif count == 0:
            count = 1
        j += count
    if len(cpu_duration) > 0:
        cpu_avg = np.min(cpu_duration)
    else:
        cpu_avg = minValue
    if len(mem_duration) > 0:
        mem_avg = np.min(mem_duration)
    else:
        mem_avg = minValue
    if len(disk_duration) > 0:
        disk_avg = np.min(disk_duration)
    else:
        disk_avg = minValue
    if len(diskio_duration) > 0:
        diskio_avg = np.min(diskio_duration)
    else:
        diskio_avg = minValue
    if len(diskior_duration) > 0:
        diskior_avg = np.min(diskior_duration)
    else:
        diskior_avg = minValue
    if len(diskiow_duration) > 0:
        diskiow_avg = np.min(diskiow_duration)
    else:
        diskiow_avg = minValue
    if len(netss_duration) > 0:
        netss_avg = np.min(netss_duration)
    else:
        netss_avg = minValue
    lines = hostname_list[i]+','+str(cpu_avg)+','+str(mem_avg)+','+str(disk_avg)+','+str(
        diskio_avg) + ','+str(diskior_avg)+','+str(diskiow_avg) + ','+str(netss_avg)+'\n'
    result.write(lines)
result.close()
print("task finished")
