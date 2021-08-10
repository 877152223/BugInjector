import os
filelist1=os.listdir('/home/opc/MLDATA/diff')
for name in filelist1:
    filelist=os.listdir('/home/opc/MLDATA/diff/'+name)
    for file in filelist:
        try:
            with open('/home/opc/MLDATA/diff/'+name+'/'+file) as codefile:
                print('/home/opc/MLDATA/diff/'+name+'/'+file)
                lines=codefile.readlines()
                print(1)
                os.popen('mkdir -p /home/opc/MLDATA/SPLITTED/'+name)
                print(2)
                aimedfile=open('/home/opc/MLDATA/SPLITTED/'+name+'/'+file,'w')
                print(3)
                for line in lines:
                    if(not line.strip().startswith('#include')):
                        aimedfile.write(line)
                aimedfile.close()
        except:
            pass



