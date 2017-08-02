#!/usr/bin/env python2.6
#-*- coding:utf-8 -*-

import csv
import datetime

class saformat(object):
    def __init__(self, ip, type, date=None):
        if date is None:
            self.date = (datetime.datetime.now() + datetime.timedelta(days = -1)).strftime("%Y-%m-%d")
        else:
            self.date = date
        self.type = type
        self.ip = ip
        self.sadir = "/data/perdir/%s/%s" % (self.ip, self.date)
        self.name = "%sfile" % self.type
    def makeitems(self):
        with open("%s/%s" % (self.sadir, self.name), 'rb') as f:
            reader = csv.reader(f, delimiter=' ', quoting=csv.QUOTE_NONE)
            self.rowlist = [row for row in reader]
        if len(self.rowlist) < 143:
            self.salist = [(line[0],line[1:]) for line in self.rowlist]
        else:
            self.salist = [line[1:] for line in self.rowlist]
        return [[(self.type,saline)] for saline in self.salist]
    def timestamp(self):
        try:
            self.tslist = ["%s %s" % (self.date, tsline) for tsline in self.rowlist]
        except ValueError:
            self.ts = self.date
        finally:
            return self.ts


def makejson(ip):
        timestap = saformat(ip, "cpu").timestamp()
        iolist = saformat(ip, "io").makeitems()
        cpulist = saformat(ip, "cpu").makeitems()
        swaplist = saformat(ip, "swap").makeitems()
        memlist = saformat(ip, "mem").makeitems()
        loadlist = saformat(ip, "load").makeitems()
        netlist = saformat(ip, "net").makeitems()
        res = []
        for i in range(len(iolist)):
                res.append([timestap[i], ip, dict(iolist[i] + cpulist[i] + swaplist[i] + memlist[i] + loadlist[i] + netlist[i])])
        return res



if __name__ == '__main__':
    with open('/root/ansible/shen/sar_ip_20150721') as hosts:
        for h in hosts.readlines():
            sajson = makejson(h)
            print(sajson)



