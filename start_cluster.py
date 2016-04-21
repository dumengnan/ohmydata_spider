#!/usr/bin/python
# -*- coding:utf-8 -*-
import multiprocessing
import argparse
import pexpect
import sys

class sshProcess(multiprocessing.Process):
    def __init__(self, workerid, hostname, password, crawlername):
        multiprocessing.Process.__init__(self)
        self.workerid = workerid
        self.hostname = hostname
        self.password = password
        self.crawlername = crawlername

    def run(self):
        server = pexpect.spawn('ssh %s cd ~/cpython/ohmydata_spider;scrapy crawl %s'%(self.hostname, self.crawlername))
        fout = file(self.workerid+'.log', 'w')
        server.logfile = fout
        server.expect('.*ssword:')
        server.sendline(self.password)
        server.expect(pexpect.EOF)

def main():
    parse = argparse.ArgumentParser()
    parse.add_argument('--worker', help='input the number of you want run in the worker', type=int,default=1)
    parse.add_argument('--crawlername', help='input the cralwer name that you want running', type=str,default="")
    args = parse.parse_args()
    worker = args.worker
    crawlername = args.crawlername

    
    config = open('cluster.config', 'r')
    for line in config:
        info = line.split(' ')
        if len(info) == 3:
            workerid = info[0]
            hostname = info[1]
            password = info[2]
            
            i = 0 
            while i < worker:
                p = sshProcess(workerid, hostname, password, crawlername)
                p.start()
                i = i + 1

if __name__ == '__main__':
    main()
