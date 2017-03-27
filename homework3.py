import copy
class Resolution:
    def __init__(self):
     pass
    def applyResolution(self,kbVal,substring,query,trace):
        resultFlag = False
        for queryFromKB in kbVal:
            if(resultFlag):
                break
            trace=[]
            for j in range(0,len(queryFromKB)):
                temp = ""
                if(substring.startswith('~')):
                    temp=substring[1:len(substring)]
                else:
                    temp=substring
                if(temp in ''.join(queryFromKB)):
                    if((substring.startswith('~') and queryFromKB[0].startswith('~')) or (substring.startswith('~')==False and queryFromKB[0].startswith('~') ==False)):
                        continue
                    StringafterUnification,dict=unifyString(queryFromKB,query)
                    #constants=StringafterUnification.unifiedConstants
                    newstring=[]
                    newstring=StringafterUnification.getUnifiedString(dict)
                    isUnified =StringafterUnification.unified
                    if(isUnified is True and len(newstring)!=0):
                        return True
                    elif(isUnified is True):
                        kbVal.append(newstring)
                        trace.append(newstring)
                        if(self.applyResolution(kbVal,newstring[0][0:newstring[0].index('(')+1], newstring[0], trace)and (len(newstring)<2 or self.applyResolution(kbVal, newstring[1][0:newstring[1].index('(')+1],newstring[1], trace))):
                            return True
                    else:
                        continue
                else:
                    continue
        return False
class Unification:
    def __init__(self,unified,unifiedConstants):
        self.unified=unified
        self.unifiedConstants=unifiedConstants
    def getUnifiedString(self,result):
        unifiedquerystack=[]
        for key in result:
            unifiedquery=''
            if(key=="constants"):
                unifiedquery+=str(result[key])
            unifiedquerystack.append(unifiedquery)
        return unifiedquerystack
    def setUnified(self,boolval):
        self.unified=boolval
    def setConstants(self,cons):
        self.unifiedConstants=cons

class Node:
      def __init__(self,value,left,right):
        self.value = value
        self.left =left
        self.right = right
def negatequery(query):
    tempquery =""
    if(query[0] == '~'):
        qlen=len(query)
        tempquery+=query[1:qlen]
    else:
        tempquery+="~"
        tempquery+=query
    return tempquery
def separateandor(root,cnfpredicates):
     newlist=[]
     stringBuffer=""
     for cnfstatement in cnfpredicates:
         if(cnfstatement!="^"):
            stringBuffer+=cnfstatement
         else:
            newlist.append(stringBuffer)
            stringBuffer=""
     newlist.append(stringBuffer)
     return newlist
def splitArray(root,cnfExpressions):
    if(root==None):
        return None
    splitArray(root.left, cnfExpressions)
    cnfExpressions.append(root.value)
    splitArray(root.right,cnfExpressions)
def applyDistributiveLaw(root):
    root = applyDistribution(root)
    if(root.left!=None):
        root.left=applyDistribution(root.left)
    if(root.right!=None):
        root.right=applyDistribution(root.right)
    return root
def applyDistribution(root):
    if(root.value=="|" or root.value=="&"):
            left = applyDistribution(root.left)
            right = applyDistribution(root.right)
            root= distribute(root,left,right)
            return root
    else:
        return root
def distribute(root,left,right):
    if (root.value=="|"):
        if left.value=="&":
             p1=Node("|",left.left, right)
             p2=Node("|",left.right, right)
             x1= Node("&",p1,p2)
             return x1
        if (right.value=="&"):
            p1=Node("|",right.left, left)
            p2=Node("|",right.right,left)
            x1=Node("&",p1,p2)
            return x1
    return root
def constructTree(postfixexpr):
        stack = []
        iter1=0
        operator=['&','^','v','|','=','~']
        while iter1 < len(postfixexpr):
           if postfixexpr[iter1] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                strr=''
                while(postfixexpr[iter1]!=')'):
                    strr+=postfixexpr[iter1]
                    iter1+=1
                strr+=postfixexpr[iter1]
                t = Node(strr,None,None)
                stack.append(t)
                iter1+=1
           elif postfixexpr[iter1] in operator:
                if postfixexpr[iter1]=='~' and postfixexpr[iter1-1]==')':
                        temp=stack.pop()
                        temp.value='~'+temp.value
                        iter1+=1
                        stack.append(temp)
                else:
                        val=postfixexpr[iter1]
                        if val=='=':
                            val=postfixexpr[iter1]+postfixexpr[iter1+1]
                            iter1+=1
                        t = Node(val,None,None)
                        if(stack):
                            t1=Node('',None,None)
                            t1 = stack.pop()
                        if(stack):
                            t2=Node('',None,None)
                            t2 = stack.pop()
                        t.right = t1
                        t.left = t2
                        stack.append(t)
                        iter1+=1
        t = stack.pop()
        return t
def formCNFTree(root):
    if(root != None ):
        if(root.value==""):
            if(root.right!=None):
                root.value=root.right.value
                root.left=root.right.left
                root.right=root.right.right
            formCNFTree(root)
        formCNFTree(root.left)
        formCNFTree(root.right)
def cnfexpression(root):
    if(root is not None):
        if(root.value is not None):
            if(root.value=='=>'):
                root.value='|'
                t1=root.left
                negateSubtree(t1)
            if(root.value=='~'):
                root.value=''
                negateSubtree(root.right)
        cnfexpression(root.left)
        cnfexpression(root.right)
def negateSubtree(child):
    if(child!= None):
        child=negateTree(child)
        leftChild=child.left
        rightChild=child.right
        if(leftChild!=None):
            if(leftChild.value!=""):
                negateSubtree(leftChild)
            else:
                child = leftChild.right
        if(rightChild!=None):
            if(rightChild.value!=""):
                negateSubtree(rightChild)
            else:
                child = rightChild
        return child
def negateTree(child1):
    if(child1!=None and child1!=''):
        c = child1.value[0]
        if(c.isupper()):
            child1.value="~" + child1.value
        elif(c=='~'):
            if(len(child1.value)>1):
                child1.value=child1.value[1:]
            else:
                child1 = negateSubtree(child1.right)
        elif(c == '|'):
            child1.value="&"
        elif(c == '&'):
            child1.value="|"
    return child1
def inorder(root):
    stacktree=[]
    if(root!=None):
        inorder(root.left)
        stacktree.append(root)
        inorder(root.right)
    return stacktree
def postfixexpression(sentence):
        postfix = []
        opStack = []
        pexpression=''
        OPERATOR = ["&", "|", "~", "^","v","="]
        i=0
        while(i<len(sentence)):
            length=0
            stringadd =''
            if sentence[i] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                while(sentence[i]!=')'):
                    stringadd+=sentence[i]
                    i+=1
                stringadd+=sentence[i]
                postfix.append(stringadd)
                i+=1
            else:
                if sentence[i]=='(':
                    opStack.append(sentence[i])
                elif sentence[i] == ')':
                    topToken = opStack.pop()
                    while topToken != '(':
                        postfix.append(topToken)
                        topToken = opStack.pop()
                else:
                    if(sentence[i] in OPERATOR):
                        x=sentence[i]
                        if(sentence[i]=='='):
                                x='=>'
                        if(sentence[i]=='^'):
                                x='&'
                        if(sentence[i]=='v'):
                                x='|'
                        opStack.append(x)
                i+=1
        while length<len(opStack):
            postfix.append(opStack.pop())
        for item in postfix:
            pexpression+=item
        return pexpression
def Queryargs(query):
        index1=query.index('(')+1
        index2=query.index(')')
        queryparts = query[index1:index2].split(',')
        return queryparts
def Predicate(query):
    for char in query:
        if(char.isupper()):
            pos=query.index("(")
            i=query.index(char)
            return query[i:pos]
    return ""
def Replacement(constants,predicatename,kb,query):
    output={}
    queryname = []
    constantnames =[]
    replacementvalues={}
    variables =[]
    for kbstrings in kb:
        index1=kbstrings.index("(")+1
        index2=kbstrings.index(")")
        KBSplit=kbstrings[index1:index2].split(',')
        if(len(constants)==len(KBSplit)):
            for i in range(0,len(constants)):
                val=constants[i]
                if(val[0].isupper()):
                    if(KBSplit[i][0].isupper()==False):
                        replacementvalues[KBSplit[i]]=val
                else:
                    if(KBSplit[i][0].isupper()):
                        replacementvalues[val]=KBSplit[i]
                        variables.append(val)

    for kbstrings in kb:
        keyvalues=replacementvalues.keys()
        for eachkey in keyvalues:
            kbstrings=kbstrings.replace("," + eachkey + ",", "," + replacementvalues[eachkey] + ",")
            kbstrings= kbstrings.replace("(" + eachkey , "(" + replacementvalues[eachkey])
            kbstrings = kbstrings.replace(eachkey + ")",  replacementvalues[eachkey] + ")")
        constantnames.append(kbstrings)

    if(len(variables)>0):
        morekeys = replacementvalues.keys()
        for keyy in morekeys:
            query = query.replace("," + keyy + ",", "," + replacementvalues[keyy] + ",")
            query = query.replace("(" + keyy , "(" + replacementvalues[keyy])
            query = query.replace( keyy + ")",  replacementvalues[keyy] + ")")
    queryname.append(query)
    output["constants"]=constantnames
    output["query"]=queryname
    return output
def unifyString(kb,query):
    value = False
    queryValues = Queryargs(query)
    predicateStart = Predicate(query)
    result = Replacement(queryValues,predicateStart,kb,query)
    constantsKB = result["constants"]
    kbcons=copy.deepcopy(constantsKB)
    nquery = result["query"][0]
    unifiedResult=Unification(value,kbcons)
    if(not constantsKB):
        value = unify(kb,nquery)
    else:
        value = unify(constantsKB,nquery)
        if(value == True):
            unifiedResult.setUnified(True)
            unifiedResult.setConstants(constantsKB)
        else:
            unifiedResult.unified=False
            unifiedResult.unifiedConstants=constantsKB
    return unifiedResult,result
def readFile(inputfile):
    f=open(inputfile)
    contents=f.readlines()
    noq=int(contents[0].rstrip())
    queries=[]
    for i in range(0,noq):
        contents[i+1]=contents[i+1].replace(" ","")
        queries.append(contents[i+1].rstrip())
    noKB=int(contents[noq+1])
    KB=[]
    postfixfinal=[]
    CNFKB=[]
    for k in range(noq+2,noKB+noq+2):
        contents[k]=contents[k].replace(" ","")
        KB.append(contents[k].rstrip())
    for m in range(0,noKB):
        post1=postfixexpression(KB[m])
        postfixfinal.append(post1)
        treeroot=constructTree(post1)
        stacktreefinal=inorder(treeroot)
        roottree=stacktreefinal.pop()
        cnfexpression(roottree)
        formCNFTree(roottree)
        objectroot=applyDistributiveLaw(roottree)
        cnfstring=[]
        splitArray(objectroot,cnfstring)
        cnfsentence=separateandor(objectroot,cnfstring)
        CNFKB.append(cnfsentence)
    KBSize=0
    KnowledgeBase = []
    while(KBSize<len(CNFKB)):
        clauses=CNFKB[KBSize]
        splitKB = []
        for j in range(0,len(clauses)):
            splitKB.append(clauses[j])
        if(len(clauses) >1):
            KnowledgeBase.append(splitKB)
        else:
            KnowledgeBase.insert(0,splitKB)
        KBSize+=1
    Answer=[]
    for count in range(0,len(queries)):
        KnowledgeBasePerQuery=copy.deepcopy(KnowledgeBase)
        querySentences =[]
        substring =""
        actualQuery =""
        query = queries[count]
        splitSentences=query.split("|")
        for xx2 in range(0,len(splitSentences)):
            actualQuery = negatequery(splitSentences[xx2])
            querySentences.append(actualQuery)
        substring = actualQuery[:actualQuery.index('(') + 1]
        KnowledgeBasePerQuery.append(querySentences)
        trace=[]
        resolute=Resolution()
        flag = resolute.applyResolution(KnowledgeBasePerQuery, substring, actualQuery,trace)
        ans=False
        if(flag):
            ans=True
        else:
            ans=False
        Answer.append(ans)
    return Answer
def unify(kb,query):
    value = False
    for kbsent in kb:
        if('~' in query):
            equateString = query[1:]
            if(equateString in kbsent):
                kb.remove(kbsent)
                value = True
        else:
            equateString = "~" +query
            if(equateString in kbsent):
                kb.remove(kbsent)
                value = True
    return value
def main():
    output=readFile('input.txt')
    fileout=open("output.txt",'w')
    for i in output:
        fileout.write(str(i))
        fileout.write('\n')
if __name__== "__main__" :
    main()
