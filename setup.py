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

from distutils.core import setup
import py2exe

setup(
    windows = ["TheFTPClient.py"],
    options = {"py2exe": {
        "packages": [
            "wx",
            "csv",
            "ftplib",
            "tempfile",
            ],
        "compressed": 1,
        "optimize": 2,
        }},
    name = "The FTP Client",
    version = "0.1",
    data_files = [
            ("", [
                "TheFTPClient.exe.manifest",
                "favorites.txt",
                ]),
            ("assets", [
                "assets/icon.ico",
                "assets/file.png",
                "assets/file-list.png",
                "assets/folder.png",
                "assets/folder-list.png",
                "assets/icon.png",
                "assets/refresh.png",
                "assets/up.png",
                ]),
        ]
)
