class CodeScanner():
    def __init__(self,filepath):

        self.filepath=filepath

        self.methodsContained={
            "__init__(self)":0,
            "__construct(self,**build_args_kw)":0,
            "load(self,path)":0,
            "train(self,train_parser)":0,
            "predict(self,path)":0,
            "eval(self,eval_parser)":0,
            "save(self,path,construct_args)":0,
            "monitor(self)":0
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
    def _extractFuns(self):
        # extract all functions from the file,return the start and end line of a function
        with open(self.filepath,'r') as f:
            lines=f.readlines()
            funs=[[]]
            begin=-1
            space=-1
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
            if(begin!=-1):
                funs.append([begin,len(lines)-1])
            assert (len(funs)>=1)
            funs.remove([])
            return funs

    def memberMethodsCheck(self):
        #check all the methods in py file
        with open(self.filepath,'r') as f:
            lines=f.readlines()
            funs=self._extractFuns()
            for fun in funs:

                begin=fun[0]
                other=True
                for method in self.methodsContained:
                    if(method == lines[begin].replace("def ","").replace(":","").replace(" ","").strip()):
                        other=False
                        self.methodsContained[method]=1
                        break

                if(other):
                    line=lines[begin]
                    self.otherMethods.append(line.replace("def","").strip()[:-1])

    def memberPropertyCheck(self):
        with open(self.filepath,'r') as f:
            lines=f.readlines()
            funs=self._extractFuns()
            for fun in funs:
                begin=fun[0]
                end=fun[1]
                if("__init__(self)" in lines[begin]):
                    for i in range(begin,end+1):
                        if("train_parser" in lines[i]):
                            self.propertiesContained["train_parser"]=1
                        if("eval_parser" in lines[i]):
                            self.propertiesContained["eval_parser"]=1

c=CodeScanner("test.py")
c.memberMethodsCheck()
c.memberPropertyCheck()
c.pylint()

print(c.methodsContained)
print(c.otherMethods)
print(c.propertiesContained)


