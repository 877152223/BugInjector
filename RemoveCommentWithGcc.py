import os

projectlist=os.listdir('/home/opc/MLDATA/SPLITTED')
for project in projectlist:
    batch=True
            
    if(batch):
        filelist=os.listdir('/home/opc/MLDATA/SPLITTED/'+project)
        os.popen('mkdir '+'/home/opc/MLDATA/SPLITTED_PREPROCESS/'+project)
        for file in filelist:
            type=file.split('_')[1].split('.')[0]
            if(type=='after' or type=='before'):
                path='/home/opc/MLDATA/SPLITTED/'+project+'/'+file
                aimedfile='/home/opc/MLDATA/SPLITTED_PREPROCESS/'+project+'/'+file
                command='gcc -E '+path+' -o '+aimedfile
                #rumtime1=os.popen('touch '+aimedfile)
                runtime=os.popen(command)
                print(command)
                print(runtime.errors)
        

