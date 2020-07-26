class CodeScanner():
    def __init__(self,filepath):
        self.filepath=filepath
        self.methodsContained={
            "__init__":0,
            "__construct":0,
            "load":0,
            "train":0,
            "predict":0,
            "eval":0,
            "save":0,
            "monitor":0
        }
    def pylint(self):
        from pylint.lint import Run
        Run([self.filepath])

    def extractFuns(self):
        with open(self.filepath,'r') as f:
            lines=f.readlines()
            funs=[[]]
            begin=-1
            spaces=-1
            for index,line in enumerate(lines):
                if(begin!=-1):
                    tem_space=0
                    while(line[tem_space]==' '):
                        tem_space=tem_space+1
                    if(tem_space==space):
                        funs.append([begin,index-1])
                        begin=-1
                        space=-1
                if('def ' in line):
                    begin=index
                    tem_space=0
                    while(line[tem_space]==' '):
                        tem_space=tem_space+1
                    space=tem_space
            assert (len(funs)>=1)
            funs.remove([])
            return funs

    def memberMethodsCheck(self):
        with open(self.filepath,'r') as f:
            lines=f.readlines()
            funs=self.extractFuns()
            for fun in funs:
                begin=fun[0]
                for method in self.methodsContained:
                    if(method in lines[begin]):
                        self.methodsContained[method]=1
c=CodeScanner("kmeans.py")
c.memberMethodsCheck()
print(c.methodsContained)



