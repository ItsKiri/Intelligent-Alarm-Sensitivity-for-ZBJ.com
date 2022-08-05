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
factor = day * 24 * 60
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
    for i in cpu_list:
        i = float('%.2f' % i)
    return cpu_list


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
    for i in mem_list:
        i = float('%.2f' % i)
    return mem_list


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
    for i in disk_list:
        i = float('%.2f' % i)
    return disk_list


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
    for i in diskio_list:
        i = float('%.2f' % i)
    return diskio_list


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
    return diskior_list


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
    return diskiow_list


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
    return ss_list


file = open('hostname.csv', 'r')
hostname_list = file.readline().split(",")
file.close()
for hostname in hostname_list:
    filename = hostname + '_full.csv'
    with open(filename, 'w') as files:
        # lines = 'x' + ',' + 'hostname' + ',' + "ip" + ',' + "cpu" + ',' + "mem" + ',' + "disk" + \
        #     ',' + "diskio" + ',' + "diskior" + ',' + "diskiow" + ',' + "netss"
        # files.write(lines + '\n')
        x = 1
        ip = hostname.split("[")[1].split("]")[0]
        cpu = get_cpu(hostname)
        length = len(cpu)
        mem = get_mem(hostname)
        if len(mem) < length:
            length = len(mem)
        disk = get_disk(hostname)
        if len(disk) < length:
            length = len(disk)
        diskio = get_diskio(hostname)
        if len(diskio) < length:
            length = len(diskio)
        diskior = get_diskior(hostname)
        if len(diskior) < length:
            length = len(diskior)
        diskiow = get_diskiow(hostname)
        if len(diskiow) < length:
            length = len(diskiow)
        netss = get_ss(hostname)
        if len(netss) < length:
            length = len(netss)
        for i in range(length):
            lines = str(x) + ',' + hostname + ',' + ip + ',' + str(cpu[i]) + ',' + str(mem[i]) + ',' + str(disk[i]) + ',' + str(
                diskio[i]) + ',' + str(diskior[i]) + ',' + str(diskiow[i]) + ',' + str(netss[i])
            files.write(lines + '\n')
            x += 1
    files.close()
print("task finished")
