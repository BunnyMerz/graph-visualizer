def remove_comentary(line: str):
    x = 0
    for c in line:
        if c == "#":
            return line[:x]
        x+=1
    return line

class Config():
    def __init__(self,path,default={}):
        self.path = path
        self.config = self.read_info()
        for key in default:
            try:
                self.config[key]
            except KeyError:
                self.config[key] = default[key]


    def read_info(self):
        out = {}
        with open(self.path, 'r') as c:
            for line in c.readlines():
                l = remove_comentary(line.rstrip())

                ## Separate by first =
                s = l.split('=',1)
                if len(s) != 2:
                    continue
                t,x = s

                ## value maybe a list
                x = x.split(',')
                if len(x) == 1:
                    x = x[0]
                ##
                out[t] = x
        return out