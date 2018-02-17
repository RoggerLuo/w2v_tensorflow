from main import Task
import os
t = Task()

# f2 = open("./corpus/知乎/家庭原因造就的童年心理创伤有可能被修复吗.txt","r")  
# lines = f2.readlines()  
# length = len(lines)

path_name = './crawler/result'
for x in range(20):

    for item in os.listdir(path_name):
        full_path = os.path.abspath(os.path.join(path_name, item))
        print(full_path)



        file_opened = open(full_path)
        lines = file_opened.readlines()        
        length = len(lines)
        for i in range(length):
            print('[第%d轮]' %x)
            print('    当前第%d段,一共%d段:' %(i,length))
            trimmedContent = lines[i].strip()
            if len(trimmedContent) > 20:
                print (trimmedContent)
                t.readTxtLine(trimmedContent)
            else: 
                print('    console:当前line太短了,跳过')