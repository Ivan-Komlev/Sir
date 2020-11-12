"""
 * SIR file format experiment
 * Multi-dimensional array storage format
 * Version 2 includes start index and compression
 
 * @author Ivan komlev <ivankomlev@gmail.com>
 * @link http://www.joomlaboat.com
 * @github https://github.com/Ivan-Komlev/Sir
 * @copyright Copyright (C) 2020. All Rights Reserved
 * @license GNU/GPL Version 2 or later - http://www.gnu.org/licenses/gpl-2.0.html
  
 * This is just an experiment yet
 * It can save Multi-dimensional arrays to file and read them
 * The data is save in bytes to be compact and have random access option
 * Currently supported types: int, float, string, list

 * Data types:
 * https://docs.python.org/3/library/struct.html

 THIS EXAMPLE SAVES MULTI-DIMENTIONAL ARRAY TO FILE AND READS IT
  
"""

import os.path
from os import path
from struct import *

class SirFile:

    def __init__(self):
        self.byteOrder='<' # < - little-endian, > - big-endian
        self.addressBlockFormat='H' # Formats: H - unsigned short (2 bytes); L - unsigned long (4 bytes); Q - unsigned long long (8 bytes).
        self.addressBlockSize=2 # 2 bytes
        self.typeBlockFormat='B' # 1 byte
        self.typeBlockSize=1 # 1 byte
        self.file=False

    def createEmptyFile(self,filename):
        if path.exists(filename):
            return False
        
        buffer = b'sir' + pack(self.byteOrder + self.addressBlockFormat + self.addressBlockFormat, 0, 0)
        #file header example = b'sir\x00\x00\x00\x00   - empty file. First block \x00\x00 is the address where data storage starts. second two bytes (H Format) \x00\x00 is the garbage collector address.
    
        newFile=open(filename,"wb")
        newFile.write(buffer)
        newFile.close()
    
        return True
        
    
    def getAddressTablePosition(self,file):
        file.seek(3,0)
        buffer = file.read(self.addressBlockSize)
        values=unpack(self.byteOrder + self.addressBlockFormat, buffer)
        address = values[0]
        return address;
    
    def getCellPositionOrValue(self,file,position,index):

        offset=0
        file.seek(position,0)
        buffer=file.read(self.typeBlockSize+self.addressBlockSize+self.addressBlockSize)
    
        positionOffset=position+self.typeBlockSize+self.addressBlockSize+self.addressBlockSize
    
        values=unpack(self.byteOrder + self.typeBlockFormat + self.addressBlockFormat + self.addressBlockFormat, buffer)
    
        type=values[0]
        blockFormat=self.addressBlockFormat
        blockSize=self.addressBlockSize
        if(type!=0):
            #This is data table not address table
            blockFormat=chr(type)
            blockSize = calcsize(blockFormat)
    
        startIndex=values[1]
        cellCount=values[2]
    
        if(index>=offset and index<offset+cellCount):
            cellPosition=positionOffset+blockSize*(index-offset)
            file.seek(cellPosition,0)
            buffer=file.read(blockSize)
        
            if type==0:
                values=unpack(self.byteOrder + blockFormat, buffer)
                return [cellPosition,values[0],type] #address cell position,position,type
            else:
                return [cellPosition,buffer,type] #address cell position,position,type
    
        

        return [0,0,0] # not found
    
    def readCellLength(self,file,position):
    
        if position==0:
            position=self.getAddressTablePosition(file)
    
        offset=0
        file.seek(position,0)
        buffer=file.read(self.typeBlockSize+self.addressBlockSize+self.addressBlockSize)
        positionOffset=position+self.typeBlockSize+self.addressBlockSize+self.addressBlockSize
        values=unpack(self.byteOrder + self.typeBlockFormat + self.addressBlockFormat + self.addressBlockFormat, buffer)
    
        type=values[0]
        blockFormat=chr(type)
        startIndex=values[1]
        blockSize = calcsize(blockFormat)
    
        cellCount=values[2]
        
        return cellCount
    
    def getCellLength(self,file,cellAddress):
    
        cellPosition=[3,self.getAddressTablePosition(file)]

        if(cellPosition[0]==0 or cellPosition[1]==0):
            return 0
        
        if(len(cellAddress)==0):
            length=self.readCellLength(file,cellPosition[1])
            return length
        
        position=cellPosition[1]

        for i in range(0,len(cellAddress)):
            cellPosition=self.getCellPositionOrValue(file,position,cellAddress[i])
            if cellPosition[1]==0:
                return 0
            
            position=cellPosition[1]
            
        length=self.readCellLength(file,cellPosition[1])
        return length
    
    
    def bytes2value(self,buffer,type):
        
        if type==0:
            return []
            
        blockFormat=chr(type)

        if len(buffer)==0:
            return False
    
        if blockFormat=='i':
            values=unpack(self.byteOrder + blockFormat, buffer)
            return values[0]
            
        if blockFormat=='s':
            return buffer.decode("utf-8") 
    
        if blockFormat=='c':
            return buffer
    
    def getCellValue(self,file,position):

        offset=0
        file.seek(position,0)
        buffer=file.read(self.typeBlockSize+self.addressBlockSize+self.addressBlockSize)
        positionOffset=position+self.typeBlockSize+self.addressBlockSize+self.addressBlockSize
        values=unpack(self.byteOrder + self.typeBlockFormat + self.addressBlockFormat + self.addressBlockFormat, buffer)
    
        type=values[0]
        blockFormat=chr(type)
        startIndex=values[1]
        blockSize = calcsize(blockFormat)
    
        cellCount=values[2]
        
        if type==0:
            return []
        
        if cellCount==0:
            return b''
    
        file.seek(positionOffset,0)
        buffer=file.read(cellCount)
        
        return self.bytes2value(buffer,type)
    
    def appendDataValue(self,file,cellPosition,type, data, startIndex, numberOfElements=1, allElementsAreTheSame=False):
        fileSize=file.seek(0, os.SEEK_END)
    
        blockFormat=self.addressBlockFormat
        blockSize=self.addressBlockSize
        if(type!=0):
            #This is data table not address table
            blockFormat=chr(type)
            blockSize = calcsize(blockFormat)
       
        if allElementsAreTheSame:
            dataLength = - numberOfElements #creating virtual array, one element and the count how many of them are there - virtually
        else:
            dataLength = numberOfElements #adding space for, not repeating data

    
        buffer = pack(self.byteOrder + self.typeBlockFormat + self.addressBlockFormat + self.addressBlockFormat, type, startIndex, dataLength)
        
        if allElementsAreTheSame:
            buffer += data
        else:
            buffer += data * numberOfElements

        buffer+= pack(self.byteOrder + self.addressBlockFormat, 0) # addrees of next possible chank of data
    
        #Save data
        file.seek(fileSize,0)
        file.write(buffer)
    
        #Save address
        buffer= pack(self.byteOrder + self.addressBlockFormat, fileSize) # addrees of next possible chank of data
        file.seek(cellPosition[0],0)
        file.write(buffer)
    
        return fileSize #return address table positoin
    
    def saveData(self,file,cellAddress,type,dataValue):  #cellAddress is an array of coordinates x,y,z,t etc. Example [0,1,0,2] this is address is similar to Python style: array[1][1][1][2]
        #[position in file,value (next position)]
        cellPosition=[3,self.getAddressTablePosition(file)]
    
        for i in range(0,len(cellAddress)):
            if(cellPosition[1]==0):
                buffer = pack(self.byteOrder + self.addressBlockFormat, 0) #* cellAddress[i] # to add address space for all elements, temporary solution
                #cellPosition[1]=self.appendDataValue(file,cellPosition,0, buffer, startIndex=cellAddress[i], numberOfElements=1, allElementsAreTheSame=False)
                cellPosition[1]=self.appendDataValue(file,cellPosition,0, buffer, startIndex=0, numberOfElements=cellAddress[i]+1, allElementsAreTheSame=False)

            cellPosition=self.getCellPositionOrValue(file,cellPosition[1],cellAddress[i])

        if cellPosition[1]==0:
            self.appendDataValue(file,cellPosition,type,dataValue, startIndex=cellAddress[i], numberOfElements=len(dataValue), allElementsAreTheSame=False)
        else:
            raise Exception("Cell position is not null. Cannot overwrite data, only append.")

        return True

    def readData(self,file,cellAddress):

        position=self.getAddressTablePosition(file)
        if(position==0):
            return None
        
        for i in range(0,len(cellAddress)):
            cellPosition=self.getCellPositionOrValue(file,position,cellAddress[i])
            if cellPosition[2]!=0:
                return self.bytes2value(cellPosition[1],cellPosition[2])
            else:
                if cellPosition[1]==0:
                    raise IndexError("Index out of range")
                    return [False,0]
                
            position=cellPosition[1]
        
        value=self.getCellValue(file,position)
    
        return value
        
    def openFile(self,filename):
        if path.exists(filename):
            self.file=open(filename,"rb+")
        else:
            raise IOError("File not found")
            return False
            
    def closeFile(self):
        if self.file!=False:
            self.file.close()
        else:
            raise IOError("File not found")
            return False