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
import time
import os.path
import tempfile
import threading

class ExplorerDropTarget(wx.FileDropTarget):
    def __init__(self, explorer):
        wx.FileDropTarget.__init__(self)
        self.explorer = explorer
        
    def OnDropFiles(self, x, y, filenames):
        for filename in filenames:
            self.explorer.ftp.upload(filename)

        self.explorer.doRefresh('.')

class Explorer(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "The FTP Client")

        self.timer = wx.Timer(self)
        self.threads = []
        self.ftp = None

        self.SetIcon(wx.Icon("assets/icon.ico", wx.BITMAP_TYPE_ICO))
        self.Bind(wx.EVT_SIZE, self.onSize)
        
        bmpFile = wx.Image("assets/file.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        bmpFolder = wx.Image("assets/folder.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        bmpRefresh = wx.Image("assets/refresh.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        bmpUp = wx.Image("assets/up.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
	
        self.panel = wx.Panel(self, -1)
        self.boxMain = wx.BoxSizer(wx.VERTICAL)
        self.boxActions = wx.FlexGridSizer(rows = 1, cols = 4, vgap = 3, hgap = 3)
        self.buttonNewFile = wx.BitmapButton(self.panel, -1, bmpFile)
        self.buttonNewFolder = wx.BitmapButton(self.panel, -1, bmpFolder)
        self.buttonRefresh = wx.BitmapButton(self.panel, -1, bmpRefresh)
        self.buttonUp = wx.BitmapButton(self.panel, -1, bmpUp)
        
        self.listCtrlFilesAndFolders = wx.ListCtrl(self.panel, -1, style=wx.LC_REPORT)

        dropTarget = ExplorerDropTarget(self)
        self.listCtrlFilesAndFolders.SetDropTarget(dropTarget)

        wx.EVT_LIST_BEGIN_DRAG(self, self.listCtrlFilesAndFolders.GetId(), self.onDragInit)
        
        self.doBind()
        self.doMenu()
        self.doLayout()

    def doBind(self):
        self.buttonNewFile.Bind(wx.EVT_BUTTON, self.buttonNewFileClick)
        self.buttonNewFolder.Bind(wx.EVT_BUTTON, self.buttonNewFolderClick)
        self.buttonRefresh.Bind(wx.EVT_BUTTON, self.buttonRefreshClick)
        self.buttonUp.Bind(wx.EVT_BUTTON, self.buttonUpClick)
        self.listCtrlFilesAndFolders.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.listActivated)
        
    def doLayout(self):
        self.SetSize(wx.Size(400, 325))
        self.SetMinSize(self.GetSize())
        
        self.boxActions.Add(self.buttonNewFile, 0, 0)
        self.boxActions.Add(self.buttonNewFolder, 0, 0)
        self.boxActions.Add(self.buttonRefresh, 0, 0)
        self.boxActions.Add(self.buttonUp, 0, 0)
        
        self.boxActions.AddGrowableCol(2, 0)
        
        self.boxMain.Add(self.boxActions, 0, wx.EXPAND | wx.ALL, 3)
        self.boxMain.Add(self.listCtrlFilesAndFolders, 1, wx.EXPAND | wx.ALL)
        
        self.panel.SetSizer(self.boxMain)
        self.status = self.CreateStatusBar()
        self.Centre()

    def doMenu(self):
        menuBar = wx.MenuBar()

        menuFile = wx.Menu()
        menuEdit = wx.Menu()
        menuHelp = wx.Menu()
        
        newFile = menuFile.Append(-1, "New &File\tCtrl-F", "Create a New File")
        newFolder = menuFile.Append(-1, "New Fol&der\tCtrl-D", "Create a New Folder")
        menuFile.AppendSeparator()
        quitApp = menuFile.Append(-1, "&Quit\tCtrl-Q", "Quit The FTP Client")

        refreshItems = menuEdit.Append(-1, "&Refresh\tCtrl-R", "Refresh List")
        deleteItem = menuEdit.Append(-1, "Delete", "Delete Selected Item")

        about = menuHelp.Append(-1, "About", "About The FTP Client")
        
        menuBar.Append(menuFile, "File")
        menuBar.Append(menuEdit, "Edit")
        menuBar.Append(menuHelp, "Help")

        self.Bind(wx.EVT_MENU, self.buttonNewFileClick, newFile)
        self.Bind(wx.EVT_MENU, self.buttonNewFolderClick, newFolder)
        self.Bind(wx.EVT_MENU, self.doQuit, quitApp)
        self.Bind(wx.EVT_MENU, self.doRefresh, refreshItems)
        self.Bind(wx.EVT_MENU, self.buttonDeleteClick, deleteItem)
        self.Bind(wx.EVT_MENU, self.doAbout, about)
        
        self.SetMenuBar(menuBar)

    def onSize(self, event):
        (x, y) = self.GetSize()
        
        self.listCtrlFilesAndFolders.SetColumnWidth(0, (x*0.66))
        self.listCtrlFilesAndFolders.SetColumnWidth(1, (x*0.25))

        event.Skip()
    
    def doRefresh(self, directory = ''):  
        self.status.SetStatusText("Loading directory...")

        (x, y) = self.GetSize()
        
        self.listCtrlFilesAndFolders.ClearAll()
        
        self.listCtrlFilesAndFolders.InsertColumn(0, "Name")
        self.listCtrlFilesAndFolders.InsertColumn(1, "Size")
        self.listCtrlFilesAndFolders.SetColumnWidth(0, (x*0.66))
        self.listCtrlFilesAndFolders.SetColumnWidth(1, (x*0.25))

        imageList = wx.ImageList(16, 16, True)
        imageList.Add(wx.Bitmap("assets/folder-list.png", wx.BITMAP_TYPE_PNG))
        imageList.Add(wx.Bitmap("assets/file-list.png", wx.BITMAP_TYPE_PNG))
        
        self.listCtrlFilesAndFolders.AssignImageList(imageList, wx.IMAGE_LIST_SMALL)
        
        if directory:
            self.ftp.directory(directory)
        
        for item in self.ftp.output:
            length = self.listCtrlFilesAndFolders.GetItemCount()
            
            kind = item[0][0]
            permissions = item[0]
            bit = item [1]
            user = item[2]
            group = item[3]
            size = item[4]
            month = item[5]
            day = item[6]
            time = item[7]
            title = item[8]
            
            self.listCtrlFilesAndFolders.InsertStringItem(length, title)
            self.listCtrlFilesAndFolders.SetStringItem(length, 1, size)

            if kind == "d":
                self.listCtrlFilesAndFolders.SetItemImage(length, 0)
            elif kind == "l":
                self.listCtrlFilesAndFolders.SetItemImage(length, 1)
            else:
                self.listCtrlFilesAndFolders.SetItemImage(length, 1)

        self.status.SetStatusText(self.ftp.getCurrentDirectory())
        

    def setFTP(self, ftp):
        self.ftp = ftp
        self.doRefresh('.')
        self.SetTitle(self.ftp.getHostname())

    def doAbout(self, event):
        dialogAbout = wx.MessageDialog(
            None,
            "The FTP Client, Copyright (c) 2006, Jason Johnson",
            "About The FTP Client",
            wx.OK
        )
        dialogAbout.ShowModal()
        dialogAbout.Destroy()

    def doQuit(self, event):
        self.ftp.disconnect()
        self.Destroy()

    def onDragInit(self, event):
        tmpName = tempfile.mktemp()
        tmpFile = file(tmpName, "w+b")
        
        selected = self.listCtrlFilesAndFolders.GetFirstSelected()
        selectedText = self.listCtrlFilesAndFolders.GetItemText(selected)

        finalPath = os.path.dirname(tmpName) + "\\" + selectedText

        self.ftp.download(selectedText, tmpFile)
        
        tmpFile.close()

        try:
            os.rename(tmpName, finalPath)
        except:
            pass
        
        data = wx.FileDataObject()
        data.AddFile(finalPath)
        
        source = wx.DropSource(self.listCtrlFilesAndFolders)
        source.SetData(data)
        source.DoDragDrop(True)
        
    def buttonNewFileClick(self, event):
        newFile = ''
        dialogNewFile = wx.TextEntryDialog(
            self,
            "Provide the name of the new file.",
            "New File"
        )

        if(dialogNewFile.ShowModal() == wx.ID_OK):
            newFile = dialogNewFile.GetValue()

        if(newFile != ''):
            self.ftp.createFile(newFile)
            self.doRefresh('.')

        dialogNewFile.Destroy()

    def buttonNewFolderClick(self, event):
        newFolder = ''
        dialogNewFolder = wx.TextEntryDialog(
            self,
            "Provide the name of the new folder.",
            "New Folder"
        )

        if(dialogNewFolder.ShowModal() == wx.ID_OK):
            newFolder = dialogNewFolder.GetValue()

        if(newFolder != ''):
            self.ftp.createFolder(newFolder)
            self.doRefresh('.')

        dialogNewFolder.Destroy()

    def buttonRefreshClick(self, event):
        self.doRefresh('.')

    def buttonUpClick(self, event):
        self.doRefresh('..')

    def buttonDeleteClick(self, event):
        selected = self.listCtrlFilesAndFolders.GetFirstSelected()
        selectedText = self.listCtrlFilesAndFolders.GetItemText(selected)
        
        self.ftp.deleteFile(selectedText)
        self.doRefresh('.')
        
    def listActivated(self, event):
        item = event.GetItem()
        folder = item.GetText()
        
        self.ftp.directory(folder)
        self.doRefresh('.')
