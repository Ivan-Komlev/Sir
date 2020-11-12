
"""
 * SIR file format experiment
 * THIS EXAMPLE SAVES MULTI-DIMENTIONAL ARRAY TO FILE AND READS IT
  
 * @author Ivan komlev <ivankomlev@gmail.com>
 * @link http://www.joomlaboat.com
 * @github https://github.com/Ivan-Komlev/Sir
 * @copyright Copyright (C) 2020. All Rights Reserved
 * @license GNU/GPL Version 2 or later - http://www.gnu.org/licenses/gpl-2.0.html
 
"""
from SirFile import SirFile
from SirData import SirData

a=[1,['Hello','World','Dog',3,3,3,3,3,3,3,["SOME VERY DEEP WORD"]],99]


print("Array before saving:")
print(a)
print()

newSirFile = SirData()
newSirFile.saveArray2File("8.sir",a)
print("File \"8.sir\" saved.")
print()

b=newSirFile.loadFile2Array("8.sir")
print("\nLoad file to array:")
print(b)


print("\nAlso you can read individual cells [1,2] as array:")
c=newSirFile.loadFile2Array("8.sir",[1,2])
print(c)



#trying to open file that doesn't exists
try:
    print("\nTrying to open file: \"9.sir\".")
    newSirFile.openFile("9.sir")
except IOError:
    print("9.sir File not found. Trying to open another file \"8.sir\".")
    newSirFile.openFile("8.sir")

#read cell value
print ("\nTrying to read cell value index [1,2]")
try:
    d=newSirFile.getCell([1,2])
    print(d)
except:
    pass


#read cell value where the index is out of range
#The class will raise IndexError("Index out of range")
print ("\nTrying to read cell value index [3]")
try:
    d=newSirFile.getCell([3])
    print(d)
except Exception as e:
    print ("e: "+str(e))
    print ("The index is way out of reach. Try another one")
finally:
    print ("....")


newSirFile.closeFile()
