import requests
import time
import datetime
import json
import sys
import heapq


now = int(time.time())
apiurl = "please ask for permission"
url = apiurl + "/api/v1/grafana/render"
day = 14
t = now - day * 24 * 60 * 60
factor = day * 40
gethostnameurl = apiurl + "/api/v1/grafana/metrics/find?query="


def get_hostname(ip):
    hostname = ""
    query = ip + "]"
    url = gethostnameurl + query
    response = requests.request("GET", url)
    r = json.loads(response.text)
    for t in r:
        hostname = t['text']
    return hostname


def get_cpu(hostname):
    target = '{' + hostname + '}#cpu#idle'
    payload = {'target': target,
               'from': t,
               'until': now,
               }
    files = []
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request(
        "POST", url, headers=headers, data=payload, files=files)
    cpu_list = []
    da = json.loads(response.text)
    for d in da:
        for i in d['Values']:
            if i['value'] is not None:
                cpu_list.append(i['value'])
    cpu_warninglist = heapq.nsmallest(factor, cpu_list)
    for i in cpu_warninglist:
        i = float('%.2f' % i)
    return cpu_warninglist


def get_mem(hostname):
    target = '{' + hostname + '}#mem#memused#percent'
    payload = {'target': target,
               'from': t,
               'until': now,
               }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request(
        "POST", url, headers=headers, data=payload, files=[])
    mem_list = []
    da = json.loads(response.text)
    for d in da:
        for i in d['Values']:
            if i['value'] is not None:
                mem_list.append(i['value'])
    mem_warninglist = heapq.nlargest(factor, mem_list)
    for i in mem_warninglist:
        i = float('%.2f' % i)
    return mem_warninglist


def get_disk(hostname):
    target = '{' + hostname + '}#df#bytes#used#percent'
    payload = {'target': target,
               'from': t,
               'until': now,
               }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request(
        "POST", url, headers=headers, data=payload, files=[])
    da = json.loads(response.text)
    disk_list = []
    for d in da:
        for i in d['Values']:
            if i['value'] is not None:
                disk_list.append(i['value'])
    disk_warninglist = heapq.nlargest(factor, disk_list)
    for i in disk_warninglist:
        i = float('%.2f' % i)
    return disk_warninglist


def get_diskio(hostname):
    target = '{' + hostname + '}#disk#io#util'
    payload = {'target': target,
               'from': t,
               'until': now,
               }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request(
        "POST", url, headers=headers, data=payload, files=[])
    da = json.loads(response.text)
    diskio_list = []
    for d in da:
        for i in d['Values']:
            if i['value'] is not None:
                diskio_list.append(i['value'])
    diskio_warninglist = heapq.nlargest(factor, diskio_list)
    for i in diskio_warninglist:
        i = float('%.2f' % i)
    return diskio_warninglist


def get_diskior(hostname):
    target = '{' + hostname + '}#disk#io#read_bytes'
    payload = {'target': target,
               'from': t,
               'until': now,
               }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request(
        "POST", url, headers=headers, data=payload, files=[])
    da = json.loads(response.text)
    diskior_list = []
    for d in da:
        for i in d['Values']:
            if i['value'] is not None:
                diskior_list.append(i['value']/1024/1024)
    diskior_warninglist = heapq.nlargest(factor, diskior_list)
    return diskior_warninglist


def get_diskiow(hostname):
    target = '{' + hostname + '}#disk#io#write_bytes'
    payload = {'target': target,
               'from': t,
               'until': now,
               }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request(
        "POST", url, headers=headers, data=payload, files=[])
    da = json.loads(response.text)
    diskiow_list = []
    for d in da:
        for i in d['Values']:
            if i['value'] is not None:
                diskiow_list.append(i['value']/1024/1024)
    diskiow_warninglist = heapq.nlargest(factor, diskiow_list)
    return diskiow_warninglist


def get_ss(hostname):
    target = '{' + hostname + '}#ss#estab'
    payload = {'target': target,
               'from': t,
               'until': now,
               }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request(
        "POST", url, headers=headers, data=payload, files=[])
    da = json.loads(response.text)
    ss_list = []
    for d in da:
        for i in d['Values']:
            if i['value'] is not None:
                ss_list.append(i['value'])
    ss_warninglist = heapq.nlargest(factor, ss_list)
    return ss_warninglist


file = open('hostname.csv', 'r')
hostname_list = file.readline().split(",")
file.close()
for hostname in hostname_list:
    filename = hostname + '.csv'
    with open(filename, 'w') as files:
        # lines = 'x' + ',' + 'hostname' + ',' + "ip" + ',' + "cpu" + ',' + "mem" + ',' + "disk" + \
        #     ',' + "diskio" + ',' + "diskior" + ',' + "diskiow" + ',' + "netss"
        # files.write(lines + '\n')
        x = 1
        ip = hostname.split("[")[1].split("]")[0]
        cpu = get_cpu(hostname)
        cpu.sort()
        mem = get_mem(hostname)
        mem.sort(reverse=True)
        disk = get_disk(hostname)
        disk.sort(reverse=True)
        diskio = get_diskio(hostname)
        diskio.sort(reverse=True)
        diskior = get_diskior(hostname)
        diskior.sort(reverse=True)
        diskiow = get_diskiow(hostname)
        diskiow.sort(reverse=True)
        netss = get_ss(hostname)
        netss.sort(reverse=True)
        for i in range(factor):
            lines = str(x) + ',' + hostname + ',' + ip + ',' + str(cpu[i]) + ',' + str(mem[i]) + ',' + str(disk[i]) + ',' + str(
                diskio[i]) + ',' + str(diskior[i]) + ',' + str(diskiow[i]) + ',' + str(netss[i])
            files.write(lines + '\n')
            x += 1
    files.close()
print("task finished")
