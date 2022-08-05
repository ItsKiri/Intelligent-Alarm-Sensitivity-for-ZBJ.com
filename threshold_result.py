import numpy as np
import scipy.signal


file = open('hostname.csv', 'r')
hostname_list = file.readline().split(",")
file.close()
result = open('result.csv', 'w')
# lines = 'hostname'+','+'cpu_idle'+','+'mem'+','+'disk'+','+'diskio' + \
#         ','+'diskior'+','+'diskiow'+','+'netss'+'\n'
# result.write(lines)
for hostname in hostname_list:
    filename = hostname + '.csv'
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
    factor = len(x_list)-1
    polyorder = 7
    cpu_list = scipy.signal.savgol_filter(cpu_list, factor, polyorder)
    mem_list = scipy.signal.savgol_filter(mem_list, factor, polyorder)
    disk_list = scipy.signal.savgol_filter(disk_list, factor, polyorder)
    diskio_list = scipy.signal.savgol_filter(diskio_list, factor, polyorder)
    diskior_list = scipy.signal.savgol_filter(diskior_list, factor, polyorder)
    diskiow_list = scipy.signal.savgol_filter(diskiow_list, factor, polyorder)
    netss_list = scipy.signal.savgol_filter(netss_list, factor, polyorder)
    cpu_coeffs = np.polyfit(x_list, cpu_list, polyorder)
    cpu_func = np.poly1d(cpu_coeffs).deriv().deriv()
    cpu_warninglist = np.roots(cpu_func)
    if len(cpu_warninglist) == 0:
        cpu_result = 1
    else:
        cpu_result = 1
        cpu_warninglist = np.sort(cpu_warninglist)
        for i in cpu_warninglist:
            if not isinstance(i, complex):
                if i > 0:
                    cpu_result = i
                    break
    mem_coeffs = np.polyfit(x_list, mem_list, polyorder)
    mem_func = np.poly1d(mem_coeffs).deriv().deriv()
    mem_warninglist = np.roots(mem_func)
    if len(mem_warninglist) == 0:
        mem_result = 1
    else:
        mem_result = 1
        mem_warninglist = np.sort(mem_warninglist)
        for i in mem_warninglist:
            if not isinstance(i, complex):
                if i > 0:
                    mem_result = i
                    break
    disk_coeffs = np.polyfit(x_list, disk_list, polyorder)
    disk_func = np.poly1d(disk_coeffs).deriv().deriv()
    disk_warninglist = np.roots(disk_func)
    if len(disk_warninglist) == 0:
        disk_result = 1
    else:
        disk_result = 1
        disk_warninglist = np.sort(disk_warninglist)
        for i in disk_warninglist:
            if not isinstance(i, complex):
                if i > 0:
                    disk_result = i
                    break
    diskio_coeffs = np.polyfit(x_list, diskio_list, polyorder)
    diskio_func = np.poly1d(diskio_coeffs).deriv().deriv()
    diskio_warninglist = np.roots(diskio_func)
    if len(diskio_warninglist) == 0:
        diskio_result = 1
    else:
        diskio_result = 1
        diskio_warninglist = np.sort(diskio_warninglist)
        for i in diskio_warninglist:
            if not isinstance(i, complex):
                if i > 0:
                    diskio_result = i
                    break
    diskior_coeffs = np.polyfit(x_list, diskior_list, polyorder)
    diskior_func = np.poly1d(diskior_coeffs).deriv().deriv()
    diskior_warninglist = np.roots(diskior_func)
    if len(diskior_warninglist) == 0:
        diskior_result = 1
    else:
        diskior_result = 1
        diskior_warninglist = np.sort(diskior_warninglist)
        for i in diskior_warninglist:
            if not isinstance(i, complex):
                if i > 0:
                    diskior_result = i
                    break
    diskiow_coeffs = np.polyfit(x_list, diskiow_list, polyorder)
    diskiow_func = np.poly1d(diskiow_coeffs).deriv().deriv()
    diskiow_warninglist = np.roots(diskiow_func)
    if len(diskiow_warninglist) == 0:
        diskiow_result = 1
    else:
        diskiow_result = 1
        diskiow_warninglist = np.sort(diskiow_warninglist)
        for i in diskiow_warninglist:
            if not isinstance(i, complex):
                if i > 0:
                    diskiow_result = i
                    break
    netss_coeffs = np.polyfit(x_list, netss_list, polyorder)
    netss_func = np.poly1d(netss_coeffs).deriv().deriv()
    netss_warninglist = np.roots(netss_func)
    if len(netss_warninglist) == 0:
        netss_result = 1
    else:
        netss_result = 1
        netss_warninglist = np.sort(netss_warninglist)
        for i in netss_warninglist:
            if not isinstance(i, complex):
                if i > 0:
                    netss_result = i
                    break
    cpu_result = np.poly1d(cpu_coeffs)(cpu_result)
    if cpu_result < 0:
        cpu_result = 0
    if cpu_result > 100:
        cpu_result = 100
    mem_result = np.poly1d(mem_coeffs)(mem_result)
    if mem_result < 0:
        mem_result = 0
    if mem_result > 100:
        mem_result = 100
    disk_result = np.poly1d(disk_coeffs)(disk_result)
    if disk_result < 0:
        disk_result = 0
    if disk_result > 100:
        disk_result = 100
    diskio_result = np.poly1d(diskio_coeffs)(diskio_result)
    if diskio_result < 0:
        diskio_result = 0
    if diskio_result > 100:
        diskio_result = 100
    diskior_result = np.poly1d(diskior_coeffs)(diskior_result)
    if diskior_result < 0:
        diskior_result = 0
    if diskior_result > 100:
        diskior_result = 100
    diskiow_result = np.poly1d(diskiow_coeffs)(diskiow_result)
    if diskiow_result < 0:
        diskiow_result = 0
    if diskiow_result > 100:
        diskiow_result = 100
    netss_result = np.poly1d(netss_coeffs)(netss_result)
    if netss_result < 0:
        netss_result = 0
    if netss_result > 100:
        netss_result = 100
    lines = hostname+','+str(cpu_result)+','+str(mem_result)+','+str(disk_result)+','+str(diskio_result) + \
        ','+str(diskior_result)+','+str(diskiow_result) + \
        ','+str(netss_result)+'\n'
    result.write(lines)
result.close()
print("task finished")
