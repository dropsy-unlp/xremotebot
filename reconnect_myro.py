#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import xremotebot.configuration as conf
from glob import glob
from util import run, runbg
import os
import time

class Scribbler:
    @staticmethod
    def release_rfcomm():
        for device in glob('/dev/rfcomm*'):
            run('rfcomm', 'release', device, stdout=None, stderr=None)
            try:
                status, out, err = run('lsof', '-t', device)
            except OSError:
                print('Instale lsof para una mejor gestión de dispositivos')
            else:
                for pid in out.splitlines():
                    os.kill(int(pid), 9)

    @staticmethod
    def bind_rfcomm(macs):
        for n, mac in enumerate(macs):
            status, _, _ = run('rfcomm', 'bind', 'rfcomm{}'.format(n), mac,
                stdout=None, stderr=None)
            if status != 0:
                raise OSError('Error asociando {} '
                              'a un dispositivo rfcomm'.format(mac))

def main():
    Scribbler.release_rfcomm()
    Scribbler.bind_rfcomm(conf.robots.get('scribbler', []))

if __name__ == '__main__':
    main()
