from main import Task

t = Task()
f2 = open("./corpus/知乎/家庭原因造就的童年心理创伤有可能被修复吗.txt","r")  
lines = f2.readlines()  
length = len(lines)
for i in range(length):
    print('当前第%d段,一共%d段' %(i,length))
    print (lines[i])
    t.readTxtLine(lines[i])
