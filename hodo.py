#!/usr/bin/env python
# coding=utf-8
import sys

# global keyword
PDB = "MTIT"
uPDB = "MTIU"

class BOOK:
    'book'
    section = 0
    author = "" # utf16
    name = ""
    uPDB = 0
    Vol = list()
    Title = list()
    TotSect = ""
    def __init__(self):
        return
        
    def show(self):
        print(self.author, "  ", '%d' %(self.section-2), "sections" )
        print(self.name)
        print(self.TotSect)
        i = 0
        for i in range(self.section-1):
            if i == 0 or i == (self.section-1):
                print(i,":",'%x' %(self.Vol[i]))
            else:
                print(i, ":", '%x' %(self.Vol[i]), ":", self.Title[i-1])
            i += 1
            
    def parseHeader(self, header):
        i=0
        while header[i] != 0:
            i += 1
        version = str(header[64:68], encoding='utf8');
        if version == uPDB:
            self.uPDB = 1;
            self.author = str(header[0:i], encoding='utf16');
        else:
            self.uPDB = 0;
            self.name = str(header[0:i], encoding='big5');
        self.section = header[77]+(header[76]<<8)

    def initVolume(self, fn):
        fn.seek(78)
        header = fn.read(8*self.section)
        i = 0
        for i in range(self.section-1):
            self.Vol.append((header[i*8]<<24)+(header[i*8+1]<<16)+(header[(i*8)+2]<<8)+(header[(i*8)+3]))
            i += 1
    def initPDB(self, fn):
        fn.seek(78+8*self.section)
        readahead = 30
        header = fn.read(readahead)     
        i = 8
        for i in range(readahead):
            if header[i] == 0x19 and header[i+1] == 0x19 and header[i+2] == 0x191919:
                self.name = str(header[8:i], encoding='big');
                break;
            i += 1
        if i >= range(sz):
            return 0
        i += 3
        return i+1
        
    def inituPDB(self, fn):
        fn.seek(self.Vol[0])
        readahead = self.Vol[1]-self.Vol[0]
        header = fn.read(readahead)
        i = startoff = 8
        for i in range(startoff, readahead):
            if header[i] == 27 and header[i+1] == 0 and header[i+2] == 27 and header[i+3] == 0 and header[i+4] == 27 and header[i+5] == 0:
                break;
            i += 1

        self.name = str(header[startoff:i], encoding='utf16')
           
        i = i+6
        startoff = i
        for i in range(startoff, readahead):
            if header[i] == 27 and header[i+1] == 0x00:
                self.TotSect = str(header[startoff:i], encoding='utf8');
                #self.TotSect = str(header[startoff:i]);
                break;
            i += 1
        
        # Initialize section title.
        i = i + 2
        startoff = i
        for i in range(startoff, readahead):
            if header[i] == 13 and header[i+1] == 0 and header[i+2] == 10 and header[i+3] ==0:
                self.Title.append(str(header[startoff:i], encoding='utf16'))
                i += 4
                startoff = i
            else:
                i += 1        
        self.Title.append(str(header[startoff:i], encoding='utf16'))
        return 0
        
        
    def initBook(self, fn):
        if self.uPDB == 1:
            self.inituPDB(fn)
        else:
            self.initPDB(fn)
   
    def readVol(self, fn, vol):
        if(vol > (self.section-1)):
            print("too many section:" ,vol)
            return -1
        fn.seek(self.Vol[vol])
        readahead = self.Vol[vol+1]-self.Vol[vol]
        header = fn.read(readahead)
        print(str(header[0:400], encoding='utf16'))
        
   
book="12G3b.updb"

fn = open(book, "rb")
header = fn.read(78)
bk=BOOK()
bk.parseHeader(header)
bk.initVolume(fn)
bk.initBook(fn)
bk.readVol(fn,3)
fn.close()
