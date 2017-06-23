

with open('/home/yuxiang/py_project/log.log') as log:
    for line in log:
        if(line.startswith('INFO:root:####')):
            print(line)
            url = line[line.index('http'):]
            print(url)
