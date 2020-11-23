
import os
import os.path
from os import path
from os import getcwd
import pickle

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
def getNameFromPath(filePath):
    name=os.path.basename(filePath)
    f_name, f_ext = os.path.splitext(name)
    return f_name, f_ext
def saveData(name,data):
    with open(name, 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
def loadData(name):
    with open(name, 'rb') as handle:
        return pickle.load(handle)
def incName():
    usedNames=getFilesbyType('.png','FilterOp')
    maxN= -1
    for i in usedNames:
        onlyName,_=getNameFromPath(i)
        if int(onlyName)>maxN:
            maxN=int(onlyName)
    maxN=str(maxN+1)

    nameD=createFilePath(maxN,'.info',r'FilterOp/')
    nameP=createFilePath(maxN,'.png',r'FilterOp/')
    return nameP,nameD