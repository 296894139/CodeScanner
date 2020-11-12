import json
import os
class CodeScanner():
    def __init__(self,rootpath):
        with open(os.path.join(rootpath,"Anylearn_tools.py")) as f:
            lines=f.readlines()
            for line in lines:
                if "import" in line:
                    line=line.replace(" ","").strip()
                    line=line.replace("from"," ").replace("import"," ")
                    self.filepath = os.path.join(rootpath,line.split(" ")[-2],line.split(" ")[-1]+".py")
                    break
        self.args=['nargs','type','default','help','required','option','metavar','action','description','str','int','True','False','const','float']
        #os.path.join(rootpath,"Anylearn_tools.py")
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
        self.train_params_list=[]
        self.eval_params_list=[]
        self.propertiesContained={
            "train_parser":0,
            "eval_parser":0
        }

        # methods not included in our design file
        self.otherMethods=[]

    def parserGet(self):
        #check all the methods in py file
        with open(self.filepath,'r') as f:
            lines=f.readlines()
            for line in lines:
                if "self.train_parser.add_argument" in line:
                    line=line.lstrip()
                    line=line[line.index("(")+1:]
                    line=line[:line.rindex(")")]
                    b = line.index(',')
                    name=line[:b]
                    s = line[b + 1:]

                    s = "{" + s + "}"
                    s = s.replace("=", ":")
                    s = s.replace("'", "\"")

                    for arg in self.args:
                        s = s.replace(" "+arg, " \"" + arg + "\"")
                        s=s.replace(":"+arg,":\"" + arg + "\"")

                    tem=json.loads(s)
                    tem['name']=name

                    '''params=line.split(",")
                    tem={}
                    tem["name"]=params[0].replace("-","").replace("'","").replace('\"',"").replace("\n","")
                    for i in range(1,len(params)):
                        key=params[i].split("=")[0]
                        val=params[i].split("=")[1].replace("\n","")
                        tem[key]= val'''
                    self.train_params_list.append(tem)
                elif "self.eval_parser.add_argument" in line:
                    '''line = line.split("(")[1].replace(")", "")
                    params = line.split(",")
                    tem = {}
                    tem["name"] = params[0].replace("-", "").replace("'", "").replace('\"', "").replace("\n", "")
                    for i in range(1, len(params)):
                        key = params[i].split("=")[0]
                        val = params[i].split("=")[1].replace("\n", "")
                        tem[key] = val'''
                    line = line.lstrip()
                    line = line[line.index("(") + 1:]
                    line = line[:line.rindex(")")]
                    b = line.index(',')
                    name = line[:b]
                    s = line[b + 1:]

                    s = "{" + s + "}"
                    s = s.replace("=", ":")
                    s = s.replace("'", "\"")

                    for arg in self.args:
                        s = s.replace(" " + arg, " \"" + arg + "\"")
                        s = s.replace(":" + arg, ":\"" + arg + "\"")
                    tem = json.loads(s)
                    tem['name'] = name
                    self.eval_params_list.append(tem)
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
        #check all the properties in py file
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

    def main(self):
        legal=True
        self.memberMethodsCheck()
        self.memberPropertyCheck()
        for t in self.methodsContained.values():
            if(t!=1):
                legal=False
        for t in self.propertiesContained.values():
            if (t != 1):
                legal = False
        self.parserGet()
        return legal,self.train_params_list,self.eval_params_list

c=CodeScanner("D:\workspace\XLearn-Algorithm-Source\yolov5")
print(c.main())
#c.memberMethodsCheck()
#c.memberPropertyCheck()
#c.pylint()
'''s1="'--img_size', nargs='+', type='int', default=[640, 640], help='[train, test] image sizes'"
s2="'--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu'"
args=['nargs','type','default','help','required','option','metavar','action','description']
s3="'--adam', action='store_true', help='use torch.optim.Adam() optimizer'"
def go(s):
    b=s.index(',')
    s=s[b+1:]
    s="{"+s+"}"
    s=s.replace("=",":")
    s=s.replace("'","\"")
    for arg in args:
        s = s.replace(" " + arg, " \"" + arg + "\"")
        s = s.replace(":" + arg, ":\"" + arg + "\"")
    print(json.loads(s))'''
#print(c.methodsContained)
#print(c.otherMethods)
#print(c.propertiesContained)
#c.parserGet()
#print(c.eval_params_list)
