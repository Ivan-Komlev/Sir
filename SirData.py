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
from SirFile import SirFile

class SirData(SirFile):

    def __init__(self):
        SirFile.__init__(self)
        
    def convertValue2Bytes(self,value):

        if isinstance(value, (str)) :
            return 's'
        
        if isinstance(value, (int)):
            return 'i'
        
        if isinstance(value, (float)) :
            return 'f'
        
        if isinstance(value, (list)) :
            return ''

        return ''

    def saveArrayRecursively(self,file,cellAddress,arrayOfValues):

        data=b''    
        for i in range(len(arrayOfValues)-1,-1,-1):
            datatype=self.convertValue2Bytes(arrayOfValues[i])
        
            if(datatype==''):
                self.saveArrayRecursively(file,cellAddress+[i],arrayOfValues[i])
            else:
                if(datatype=='s'):
                    data=bytes(arrayOfValues[i], "utf8")
                else:
                    data=pack(self.byteOrder + datatype,arrayOfValues[i])
            
                pos=cellAddress+[i]

                self.saveData(file,cellAddress+[i],ord(datatype),data)
        
    def saveArray2File(self,filename,arrayOfData):
        if path.exists(filename)==False:
            self.createEmptyFile(filename)
            
            file=open(filename,"rb+")
            self.saveArrayRecursively(file,[],arrayOfData)
            file.close()
        else:
            return False
            
    def loadArrayRecursively(self,file,cellAddress):
        value=self.readData(file,cellAddress)
        
        if isinstance(value, (list)):
            count=self.getCellLength(file,cellAddress)
            innerArray=[]
            for i in range(0,count):
                newCellAddress=cellAddress+[i];
                innerArray.append(self.loadArrayRecursively(file,newCellAddress))
            
            return innerArray
        else:
            return value
    
    def loadFile2Array(self,filename,cellAddress=[]): #cellAddress not implemented yet
        
        if path.exists(filename):
            try:
                file=open(filename,"rb+")
            except Exception as e:
                raise Exception(e)
                return False;
            
            count=self.getCellLength(file,cellAddress)
            
            newArray=[]
            
            for i in range(0,count):
                newArray.append(self.loadArrayRecursively(file,cellAddress+[i]))
            
            file.close()
            
            return newArray
        else:
            raise IOError("File not found")
            return False

    def getCell(self,cellAddress=[]):
        if self.file!=False:
            newArray=[]
            
            if len(cellAddress)==0:
                count=self.getCellLength(self.file,cellAddress)
                for i in range(0,count):
                    newArray.append(self.loadArrayRecursively(self.file,cellAddress+[i]))
            else:
                newArray.append(self.loadArrayRecursively(self.file,cellAddress))

            if(len(newArray)==1):
                return newArray[0]
            else:
                return newArray
        else:
            raise IOError("File not opened")
            return False    