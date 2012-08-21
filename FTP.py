#!/usr/bin/env python

"""
    Copyright (c) 2006, Jason Johnson
    All rights reserved.

    Redistribution and use in source and binary forms, 
    with or without modification, are permitted provided 
    that the following conditions are met:

        * Redistributions of source code must retain 
          the above copyright notice, this list of 
          conditions and the following disclaimer.
        * Redistributions in binary form must reproduce 
          the above copyright notice, this list of conditions 
          and the following disclaimer in the documentation 
          and/or other materials provided with the 
          distribution.
        * Neither the name of the Author nor the names 
          of its contributors may be used to endorse 
          or promote products derived from this software 
          without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS 
    AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED 
    WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR 
    PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT 
    OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, 
    INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES 
    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE 
    GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR 
    BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF 
    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT 
    OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
    POSSIBILITY OF SUCH DAMAGE.
"""

import os.path
import tempfile
import ftplib

class FTPClient:
    def __init__(self, hostname = '', username = '', password = ''):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.ftp = ftplib.FTP()
        self.output = []
        self.store = ''
    
    def setHostname(self, hostname):
        self.hostname = hostname

    def getHostname(self):
        return self.hostname
    
    def setUsername(self, username):
        self.username = username

    def getUsername(self):
        return self.username
    
    def setPassword(self, password):
        self.password = password

    def getPassword(self):
        return self.password
    
    def connect(self):
        try:
            self.ftp.connect(self.hostname)
        except:
            pass
        
    def login(self):
        try:
            self.ftp.login(self.username, self.password)
        except:
            pass
        
    def directoryCallback(self, line):
        new = []
        count = 0
        
        for item in line.split(' '):
            if item != '':
                if count < 9:
                    new.append(item)
                    count = count + 1
                else:
                    new[-1] = new[-1] + ' ' + item
        
        self.output.append(new)
        
    def directory(self, path = ''):
        self.output = []
        
        if path:
            try:
                self.ftp.cwd(path)
            except:
                pass
        
        self.ftp.dir('.', self.directoryCallback)

    def getCurrentDirectory(self):
        return self.ftp.pwd()
    
    def upload(self, local):
        self.ftp.storbinary("STOR " + os.path.basename(local), file(local))

    def downloadCallback(self, data):
        self.store.write(data)
    
    def download(self, remote, local):
        self.store = local
        self.ftp.retrbinary("RETR " + remote, self.downloadCallback)

    def createFile(self, name):
        self.ftp.storbinary("STOR " + name, file(tempfile.mkstemp()[1]))

    def createFolder(self, name):
        self.ftp.mkd(name)

    def deleteFile(self, name):
        try:
            self.ftp.delete(name)
        except:
            pass

    def deleteFolder(self, name):
        try:
            self.ftp.rmd(name)
        except:
            pass
    
    def disconnect(self):
        try:
            self.ftp.quit()
        except:
            pass
