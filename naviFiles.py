
import os
import os.path
from os import path
from os import getcwd

DirectoryPath = os.getcwd()+'\\'

def createFilePath(filename,TypeFile,DirectoryPath=DirectoryPath):
    if path.exists(DirectoryPath+filename+TypeFile):
        i=2
        while (path.exists(DirectoryPath+filename+'v'+str(i)+TypeFile)):
            i+=1
        return DirectoryPath+filename+'V_'+str(i)+TypeFile
    else:
        return DirectoryPath+filename+TypeFile
def getFilesbyType(typFile,path=None):
    r = [f for f in os.listdir(path) if(typFile in f)]
    return r
def fileFromList(tFile,path=None):
    files_List= getFilesbyType(tFile,path)
    print('Which file do you want to use?')
    op=0
    for i in files_List:
        print(i+" option ("+str(op)+")")
        op+=1
    op=int(input("File(option) selected :"))
    if path:
        return path+files_List[op]
    return files_List[op]