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

import wx
import csv

class Login(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, "The FTP Client")

        self.staticBoxConnect = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Connection"))
        self.staticBoxFavorites = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Favorites"))

        self.staticTextHost = wx.StaticText(self, -1, "Hostname")
        self.staticTextUser = wx.StaticText(self, -1, "Username")
        self.staticTextPass = wx.StaticText(self, -1, "Password")
        self.textCtrlHost = wx.TextCtrl(self, -1, size = (150, -1))
        self.textCtrlUser = wx.TextCtrl(self, -1, size = (125, -1))
        self.textCtrlPass = wx.TextCtrl(self, -1, size = (125, -1), style = wx.PASSWORD)
        self.choiceFavorites = wx.Choice(self, -1, size = (200, -1))
        self.buttonConnect = wx.Button(self, wx.ID_OK, "Connect", size = (70, -1))
        self.buttonConnect.SetDefault()
        
        self.flexBox = wx.FlexGridSizer(3, 1)
        self.flexFields = wx.FlexGridSizer(3, 2)

        self.initFavorites()
        self.loadFavorites()
        self.doBind()
        self.doLayout()

    def disable(self):
        self.textCtrlHost.SetEditable(False)
        self.textCtrlUser.SetEditable(False)
        self.textCtrlPass.SetEditable(False)
        self.buttonConnect.SetLabel("Connecting...")
        
    def getHostname(self):
        return self.textCtrlHost.GetValue()

    def getUsername(self):
        return self.textCtrlUser.GetValue()

    def getPassword(self):
        return self.textCtrlPass.GetValue()
        
    def loadFavorites(self):
    	self.choiceFavorites.Append("")

    	try:
            for item in self.favorites:
                self.choiceFavorites.Append(item[2] + "@" + item[1])
        except:
            print "Could not load 'favorites' file."

    def doChoice(self, event):
        self.initFavorites()
        
        index = self.choiceFavorites.GetCurrentSelection()
        count = 1
        
        if index > 0:
            for item in self.favorites:
                if count == index:
                    self.textCtrlHost.SetValue(item[1])
                    self.textCtrlUser.SetValue(item[2])
                    self.textCtrlPass.SetValue(item[3])
                count += 1
        else:
            self.textCtrlHost.SetValue("")
            self.textCtrlUser.SetValue("")
            self.textCtrlPass.SetValue("")

    def initFavorites(self):
        self.favorites = csv.reader(file("favorites.txt"), delimiter = "\t")
    
    def doBind(self):
        self.choiceFavorites.Bind(wx.EVT_CHOICE, self.doChoice)
    
    def doLayout(self):
        self.flexFields.Add(self.staticTextHost, -1, wx.ALL, 5)
        self.flexFields.Add(self.textCtrlHost, -1, wx.ALL, 3)
        
        self.flexFields.Add(self.staticTextUser, -1, wx.ALL, 5)
        self.flexFields.Add(self.textCtrlUser, -1, wx.ALL, 3)
        
        self.flexFields.Add(self.staticTextPass, -1, wx.ALL, 5)
        self.flexFields.Add(self.textCtrlPass, -1, wx.ALL, 3)
        
        self.staticBoxConnect.Add(self.flexFields)
        self.staticBoxFavorites.Add(self.choiceFavorites, -1, wx.ALIGN_CENTER | wx.ALL, 5)
        
        self.flexBox.Add(self.staticBoxConnect, -1, wx.LEFT | wx.RIGHT | wx.TOP, 15)
        self.flexBox.Add(self.staticBoxFavorites, -1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 15)
        self.flexBox.Add(self.buttonConnect, -1, wx.ALIGN_CENTER | wx.ALL, 15)
        
        self.SetSizerAndFit(self.flexBox)

