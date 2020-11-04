# Sir
Multi-dimensional array storage format

SIR file format experiment
author Ivan komlev <ivankomlev@gmail.com>
link http://www.joomlaboat.com
copyright Copyright (C) 2020. All Rights Reserved
license GNU/GPL Version 2 or later - http://www.gnu.org/licenses/gpl-2.0.html
 
Multi-dimensional array storage format
This is just an experiment yet
It can save Multi-dimensional arrays to file and read them
The data is save in bytes to be compact and have random access option
Currently supported types: int, float, string, list

Data types:
https://docs.python.org/3/library/struct.html
 
 
THIS EXAMPLE SAVES MULTI-DIMENTIONAL ARRAY TO FILE AND READS IT


a=[1,['Hello','World','Dog',3,3,3,3,3,3,3,["SOME VERY DEEP WORD"]],99]


print("Array before saving:")
print(a)

newSirFile=SirData()
newSirFile.saveArray2File("1.sir",a)
print("File saved.")


b=newSirFile.loadFile2Array("1.sir")
print("Load file to array:")
print(b)


print("Also you can access individual cells [1]:")
c=newSirFile.loadFile2Array("1.sir",[1])
print(c)

print("Or individual cell value [1,10,0] (Its equivalent to [1][10][0]):")
newSirFile.openFile("1.sir")
d=newSirFile.getCell([1,10,0])
print(d)
newSirFile.closeFile()
