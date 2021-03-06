
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
        return DirectoryPath+filename+'v_'+str(i)+TypeFile
    else:
        return DirectoryPath+filename+TypeFile
def getFilesbyType(typFile,path=None):
    r = [f for f in os.listdir(path) if(typFile in f)]
    return r
def getDirectories(path=None):
    a = [f for f in os.listdir(path) if not '.' in f]
    return a
def createDirector(dir,path=None):
    curDir=getDirectories(path)
    if path==None:
        path=''
    if dir in curDir:
        i=2
        while(dir+str(i) in curDir):
            i+=1
        dir=dir+str(i)
    return path+dir
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
def saveData(name,data,filter_ord,filter_mask=None):
    rn,_=getNameFromPath(name)
    filter_ord[rn]=data
    if filter_mask:
        filter_ord[rn+'m']=filter_mask
    with open(name, 'wb') as handle:
        pickle.dump(filter_ord, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return filter_ord
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