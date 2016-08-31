import os
import sys
import datetime
import time
import subprocess, threading
import shlex
import traceback
import signal
import argparse
import json

class Command(object):

    cmd = None
    process = None
    status = None
    output, error = '', ''

    def __init__(self, cmd):
        # if isinstance(cmd, basestring):
        #     cmd = shlex.split(cmd)
        self.cmd = cmd
        #self.process = None

    def run(self, timeout, outputfile, errfile):
        def target():
            print('Thread started')
            try:
                print(self.cmd)
                open(outputfile, 'w').close()
                open(errfile, 'w').close()
                self.process = subprocess.Popen(self.cmd, shell=True, stdout = file(outputfile, 'w+'), stderr = file(errfile, 'w+')) #
                (self.output, self.error) = self.process.communicate() #
                self.status = self.process.returncode
                print(self.output) #"Out:'%s'" %
                print(self.error) #"Err:'%s'" %
                print('Thread finished')
            except:
                self.error = traceback.format_exc()
                self.status = -1
                print(self.error)

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.isAlive():
            print('Terminating process')
            os.kill(self.process.pid,signal.SIGTERM) #terminate
            thread.join()
        print(self.status)



parser = argparse.ArgumentParser(description='MyIntelliDroid!')
parser.add_argument('apksDir', metavar='apksDir', help='Directory of Input APK Files')
parser.add_argument('outDir', metavar='outDir', help='Directory of Output Files')
args = parser.parse_args()
currentdir = os.getcwd()

num = 0
#APK DIR
rootdir = args.apksDir
libdir = os.path.join(currentdir,"libs")
for path, subdirs, files in os.walk(rootdir):
    for name in files:
        if name.endswith(".apk"):
            num = num +1
            appfile = os.path.join(path, name)
            appName = name[:-4]

            #print filepath
            saveout = sys.stdout
            p, filename = os.path.split(appfile)
            #print filename
            a, dir = os.path.split(p)

            extracted_apk_dir = os.path.join(args.outDir, "Decomplied", appName)

            #if not os.path.exists(extracted_apk_dir):
             #   os.makedirs(extracted_apk_dir)
            cmd = 'apktool d -f -o ' + extracted_apk_dir + ' -s ' + appfile
            fp = os.popen(cmd)
            res = fp.read()
            print(res)

            os.chdir(extracted_apk_dir)

            # Use dex2jar to convert dex to class
            cmd = 'C:/Users/hao/Downloads/dex2jar-2.0/d2j-dex2jar.bat ' + extracted_apk_dir + '/classes.dex'
            fp = os.popen(cmd)
            res = fp.read()
            print(res)

            print('finish '+ filename)
print("number of APK: ", str(num));

