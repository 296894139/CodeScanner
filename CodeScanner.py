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

        self.propertiesContained={
            "train_parser":0,
            "eval_parser":0
        }

        # methods not included in our design file
        self.otherMethods=[]

    def pylint(self):
        # rate the code
        from pylint.lint import Run
        Run([self.filepath],do_exit=False)
    def extractFuns(self):
        # extract all functions from the file,return the start and end line of a function
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
        #check all the methods in py file
        with open(self.filepath,'r') as f:
            lines=f.readlines()
            funs=self.extractFuns()
            for fun in funs:

                begin=fun[0]
                other=True
                for method in self.methodsContained:
                    if(method in lines[begin].split("(")[0]):
                        other=False
                        self.methodsContained[method]=1
                        break

                if(other):
                    line=lines[begin]
                    self.otherMethods.append(line.replace("def","").strip()[:-1])

    def memberPropertyCheck(self):
        with open(self.filepath,'r') as f:
            lines=f.readlines()
            funs=self.extractFuns()
            for fun in funs:
                begin=fun[0]
                end=fun[1]
                if("__init__" in lines[begin]):
                    for i in range(begin,end+1):
                        if("train_parser" in lines[i]):
                            self.propertiesContained["train_parser"]=1
                        if("eval_parser" in lines[i]):
                            self.propertiesContained["eval_parser"]=1

c=CodeScanner("kmeans.py")
c.memberMethodsCheck()
c.memberPropertyCheck()
c.pylint()
print(c.methodsContained)
print(c.otherMethods)
print(c.propertiesContained)

