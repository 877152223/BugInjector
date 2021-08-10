import json
import os
import urllib3
import time

def readCommit(http,owner,repos,shaListPath):
    page=1
    while(True):
        url='https://api.github.com/repos/'+owner+'/'+repos+'/commits?per_page=100'
        result=getSHA1(http,url + '&page=' + str(page),shaListPath)
        page += 1
        print('page number is '+str(page))
        if(result==-1):
            return 1

def getSHA1(http,url,shaListPath):
    #os.popen('touch '+shaListPath+'/Sha')
    file=open(shaListPath+'/Sha','a+',encoding='utf8')
    #os.popen('touch ' + shaListPath + '/shaWithMessage')
    file2 = open(shaListPath+'/shaWithMessage', 'a+',encoding='utf8')
    try:
        #time.sleep(2)
        r = http.request('GET', url)
    
        data = json.loads(r.data)
        if(len(data)==0):
            return -1
        for commit in data:
            message=commit['commit']['message'].lower()
            keywords=['close','fix','resolve']
            is_bug=False
            for keyword in keywords:
                if((keyword in message) and (('bug' in message) or ('issue' in message))):
                    is_bug=True
                    break
            if(is_bug==True):
                sha=commit['sha']
                print('sha is '+sha)
                print('message is '+message)
                file.writelines(sha+'\n')
                file2.writelines(sha+'\n')
                file2.writelines(message+'\n')
                #time.sleep(30)
        file.close()
        file2.close()
        return 1
    except:
        print('there is an errora')
        file.close()
        file2.close()

def getDiff(projectPath,shaListPath,storePath):
    print('?????')
    file=open(shaListPath+'/Sha',encoding='utf8')
    shaList=file.readlines()
    file.close()
    os.chdir(projectPath)
    for sha in shaList:
        sha = sha[:-2]
        before = open(storePath + '/' + sha + '_before.c', 'w')
        after = open(storePath + '/' + sha + '_after.c', 'w')
        diff = open(storePath + '/' + sha + '_diff.c', 'w')
        containCode = False
        commitComment = True
        start=False
        isC=False
        try:

            command=os.popen('git show '+sha)
            output=command.read()
            print(output)

            lines=output.split('\n')
            for line in lines:
                if(line.startswith('diff --git')):
                    start=False
                if(start == False):
                    if(line.startswith('--') or line.startswith('++')):
                        suffix=(line.split('/')[-1]).split('.')[-1]
                        if((suffix=='c') or (suffix=='cpp') or (suffix=='h')):
                            isC=True
                    if(line.startswith('@@')):
                        line=line.split('@@')[-1]
                        start=True
                if(start):
                    if(line.startswith('@@')):
                        line="\n\n\n ##??Mark of a New File#  \n\n\n\n"+line.split('@@')[-1]
                    if((';' in line) and ('//' not in line)):   #Does the lines contain any code?
                        containCode=True
                    diff.writelines(line+'\n')
                    if(len(line)==0):
                        before.writelines('\n')
                        after.writelines('\n')
                    elif(line[0]=='-' and (not line.startswith('---'))):
                        if('//' not in line):                #Is only comment changed?
                            commitComment=False
                        before.writelines(' '+line[1:]+'\n')
                    elif(line[0]=='+' and (not line.startswith('+++'))):
                        if('//' not in line):
                            commitComment=False
                        after.writelines(' '+line[1:]+'\n')
                    else:
                        before.writelines(line + '\n')
                        after.writelines(line + '\n')
            if((not containCode) or commitComment or (not isC)):
                raise Exception()
            before.close()
            after.close()
            diff.close()
        except:
            before.close()
            after.close()
            diff.close()
            os.remove(storePath + '/' + sha + '_before.c')
            os.remove(storePath + '/' + sha + '_after.c')
            os.remove(storePath + '/' + sha + '_diff.c')
            continue



def all(link):
    url = 'https://github.com/' + link
    struct=url.split('/')
    owner=struct[3]
    repos=struct[4]
    headers={'Authorization':'token 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',
             'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'}
    http = urllib3.PoolManager(headers=headers)
    projectPath = '/home/ubuntu/MLDATA/repos/'+repos
    print('mkdir -p'+projectPath)
    os.popen('mkdir -p '+projectPath)
    shaListPath ='/home/ubuntu/MLDATA/sha/'+repos
    os.popen('mkdir -p ' + shaListPath)
    storePath = '/home/ubuntu/MLDATA/diff/'+repos
    os.popen('mkdir -p ' + storePath)
    os.popen('git clone '+url+' '+projectPath).read()

    readCommit(http,owner,repos,shaListPath)
    getDiff(projectPath,shaListPath,storePath)

if(__name__=='__main__'):
    list=open('/home/ubuntu/MLDATA/star.csv')
    lines=list.readlines()
    count=0
    for line in lines:
        count+=1
        name=line.split(',')[1]
        print('Current repos is '+name+'\n')
        all(name)
        if(count>500):
            exit()
