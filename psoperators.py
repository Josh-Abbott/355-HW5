# Name: Josh Abbott
# Collaborators:

from colors import *
from psexpressions import StringValue, DictionaryValue, CodeArrayValue

class PSOperators:
    def __init__(self,scoperule):
        #stack variables
        self.opstack = []  #assuming top of the stack is the end of the list
        self.dictstack = []  #assuming top of the stack is the end of the list
        self.scope = scoperule
        self.index = 0
        # The environment that the REPL evaluates expressions in.
        # Uncomment this dictionary in part2
        self.builtin_operators = {
            "add":self.add,
            "sub":self.sub,
            "mul":self.mul,
            "mod":self.mod,
            "eq":self.eq,
            "lt": self.lt,
            "gt": self.gt,
            "dup": self.dup,
            "exch":self.exch,
            "pop":self.pop,
            "copy":self.copy,
            "count": self.count,
            "clear":self.clear,
            "stack":self.stack,
            "dict":self.psDict,
            "string":self.string,
            "length":self.length,
            "get":self.get,
            "put":self.put,
            "getinterval":self.getinterval,
            "putinterval":self.putinterval,
            "search" : self.search,
            "def":self.psDef,
            "if":self.psIf,
            "ifelse":self.psIfelse,
            "for":self.psFor
        }
    #------- Operand Stack Helper Functions --------------
    
    """
        Helper function. Pops the top value from opstack and returns it.
    """
    def opPop(self):
        if len(self.opstack) > 0:
            x = self.opstack[len(self.opstack) - 1]
            self.opstack.pop(len(self.opstack) - 1)
            return x
        else:
            print("Error: opPop - Operand stack is empty")

    """
       Helper function. Pushes the given value to the opstack.
    """
    def opPush(self,value):
        self.opstack.append(value)

    #------- Dict Stack Helper Functions --------------
    """
       Helper function. Pops the top dictionary from dictstack and returns it.
    """  
    def dictPop(self):
        if len(self.dictstack) > 0:
            x = self.dictstack[len(self.dictstack) - 1]
            self.dictstack.pop(len(self.dictstack) - 1)
            return x
        else:
            print("Error: dictPop - Dictionary stack is empty")
    """
       Helper function. Pushes the given dictionary onto the dictstack. 
    """   
    def dictPush(self, d):
        self.dictstack.append(d)
    """
       Helper function. Adds name:value pair to the top dictionary in the dictstack.
       (Note: If the dictstack is empty, first adds an empty dictionary to the dictstack then adds the name:value to that. 
    """  
    def define (self ,name, value):
        length = len(self.dictstack)
        if len(self.dictstack) == 0:
            self.dictPush((0, {}))
            self.index += 1
        if (isinstance(self.dictstack[length-1][1],DictionaryValue)):
            self.dictstack[length-1][1].value[name] = value
        else:
            self.dictstack[length-1][1][name] = value

    """
       Helper function. Searches the dictstack for a variable or function and returns its value. 
       (Starts searching at the top of the dictstack; if name is not found returns None and prints an error message.
        Make sure to add '/' to the begining of the name.)
    """
     
    def lookup(self,name):
        if len(self.dictstack) > 0:
            name_str = '/' + name
            value = None
            if self.scope == 'static':
                for i in range(self.index):
                    if isinstance(self.dictstack[i][1], dict):
                        value = self.dictstack[i][1].get(name_str, None)
                        if value != None:
                            return value
                    else:
                        value = self.dictstack[i][1].value.get(name_str, None)
                        if value != None:
                            return value
            else:
                for i in reversed(self.dictstack):
                    if isinstance(i[1], dict):
                        value = i[1].get(name_str, None)
                        if value != None:
                            return value
                    else:
                        value = i[1].value.get(name_str, None)
                        if value != None:
                            return value
            return value
    
    #------- Arithmetic Operators --------------

    """
       Pops 2 values from opstack; checks if they are numerical (int); adds them; then pushes the result back to opstack. 
    """  
    def add(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1,int) or isinstance(op1,float))  and (isinstance(op2,int) or isinstance(op2,float)):
                self.opPush(op1 + op2)
            else:
                print("Error: add - one of the operands is not a number value")
                self.opPush(op2)
                self.opPush(op1)             
        else:
            print("Error: add expects 2 operands")

    """
       Pops 2 values from opstack; checks if they are numerical (int); subtracts them; and pushes the result back to opstack. 
    """ 
    def sub(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1,int) or isinstance(op1,float))  and (isinstance(op2,int) or isinstance(op2,float)):
                self.opPush(op2 - op1)
            else:
                print("Error: sub - one of the operands is not a number value")
                self.opPush(op2)
                self.opPush(op1)             
        else:
            print("Error: sub expects 2 operands")

    """
        Pops 2 values from opstack; checks if they are numerical (int); multiplies them; and pushes the result back to opstack. 
    """
    def mul(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1,int) or isinstance(op1,float))  and (isinstance(op2,int) or isinstance(op2,float)):
                self.opPush(op1 * op2)
            else:
                print("Error: mul - one of the operands is not a number value")
                self.opPush(op1)
                self.opPush(op2)             
        else:
            print("Error: mul expects 2 operands")

    """
        Pops 2 values from stack; checks if they are int values; calculates the remainder of dividing the bottom value by the top one; 
        pushes the result back to opstack.
    """
    def mod(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1,int) or isinstance(op1,float))  and (isinstance(op2,int) or isinstance(op2,float)):
                self.opPush(op2 % op1)
            else:
                print("Error: mod - one of the operands is not a number value")
                self.opPush(op1)
                self.opPush(op2)             
        else:
            print("Error: mod expects 2 operands")

    """ Pops 2 values from stacks; if they are equal pushes True back onto stack, otherwise it pushes False.
          - if they are integers or booleans, compares their values. 
          - if they are StringValue values, compares the `value` attributes of the StringValue objects;
          - if they are DictionaryValue objects, compares the objects themselves (i.e., ids of the objects).
        """
    def eq(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1,int) or isinstance(op1,bool))  and (isinstance(op2,int) or isinstance(op2,bool)):
                self.opPush(op1 == op2)
            elif (isinstance(op1, StringValue) and (isinstance(op2, StringValue))): 
                self.opPush(op1.value == op2.value)
            elif (isinstance(op1, DictionaryValue) and (isinstance(op2, DictionaryValue))):
                self.opPush(id(op1) == id(op2))
            else:
                print("Error: eq - one of the operands is not a valid value")
                self.opPush(op1)
                self.opPush(op2)             
        else:
            print("Error: add expects 2 operands")

    """ Pops 2 values from stacks; if the bottom value is less than the second, pushes True back onto stack, otherwise it pushes False.
          - if they are integers or booleans, compares their values.
          - if they are StringValue values, compares the `value` attributes of them;
          - if they are DictionaryValue objects, compares the objects themselves (i.e., ids of the objects).
    """  
    def lt(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1,int) or isinstance(op1,bool))  and (isinstance(op2,int) or isinstance(op2,bool)):
                self.opPush(op2 < op1)
            elif (isinstance(op1, StringValue) and (isinstance(op2, StringValue))): 
                self.opPush(op2.value < op1.value)
            elif (isinstance(op1, DictionaryValue) and (isinstance(op2, DictionaryValue))):
                self.opPush(op2 < op1)
            else:
                print("Error: lt - one of the operands is not a valid value")
                self.opPush(op1)
                self.opPush(op2)             
        else:
            print("Error: lt expects 2 operands")


    """ Pops 2 values from stacks; if the bottom value is greater than the second, pushes True back onto stack, otherwise it pushes False.
          - if they are integers or booleans, compares their values. 
          - if they are StringValue values, compares the `value` attributes of them;
          - if they are DictionaryValue objects, compares the objects themselves (i.e., ids of the objects).
    """  
    def gt(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()
            if (isinstance(op1,int) or isinstance(op1,bool))  and (isinstance(op2,int) or isinstance(op2,bool)):
                self.opPush(op2 > op1)
            elif (isinstance(op1, StringValue) and (isinstance(op2, StringValue))): 
                self.opPush(op2.value > op1.value)
            elif (isinstance(op1, DictionaryValue) and (isinstance(op2, DictionaryValue))):
                self.opPush(op2 > op1)
            else:
                print("Error: gt - one of the operands is not a valid value")
                self.opPush(op1)
                self.opPush(op2)             
        else:
            print("Error: gt expects 2 operands")

    #------- Stack Manipulation and Print Operators --------------
    """
       This function implements the Postscript "pop operator". Calls self.opPop() to pop the top value from the opstack and discards the value. 
    """
    def pop (self):
        if (len(self.opstack) > 0):
            self.opPop()
        else:
            print("Error: pop - not enough arguments")

    """
       Prints the opstack and dictstack. The end of the list is the top of the stack. 
    """
    def stack(self):
        print(OKGREEN+"===**opstack**===")
        for item in reversed(self.opstack):
            print(item)
        print(RED+"===**dictstack**===")
        length = len(self.dictstack)-1
        for item in reversed(self.dictstack):
            print("----", length, "----", item[0], "----")
            for item2 in item[1]:
                print(item2, "     ", item[1].get(item2))
            length -= 1
        print("================="+ CEND)


    """
       Copies the top element in opstack.
    """
    def dup(self):
        if len(self.opstack) > 0:
            elem = self.opPop()
            self.opPush(elem)
            self.opPush(elem)

    """
       Pops an integer count from opstack, copies count number of values in the opstack. 
    """
    def copy(self):
        if len(self.opstack) > 0:
            count = self.opPop()
            if (isinstance(count, int)):
                copy = self.opstack[:]
                for i in range(len(self.opstack)-count, len(self.opstack)):
                    self.opPush(copy[i])
            else:
                self.opPush(count)
            

    """
        Counts the number of elements in the opstack and pushes the count onto the top of the opstack.
    """
    def count(self):
        self.opPush(len(self.opstack))
        
    """
       Clears the opstack.
    """
    def clear(self):
        self.opstack.clear()
        
    """
       swaps the top two elements in opstack
    """
    def exch(self):
        if len(self.opstack) > 1:
            op1 = self.opPop()
            op2 = self.opPop()

            self.opPush(op1)
            self.opPush(op2)

    # ------- String and Dictionary creator operators --------------

    """ Creates a new empty string  pushes it on the opstack.
    Initializes the characters in the new string to \0 , i.e., ascii NUL """
    def string(self):
        if len(self.opstack) > 0:
            length = self.opPop()
            empty = StringValue('')
            empty.value = '(' + '\0'*length + ')'
            self.opPush(empty)
    
    """Creates a new empty dictionary  pushes it on the opstack """
    def psDict(self):
        if len(self.opstack) > 0:
            self.opPop()
            empty = DictionaryValue('')
            empty.value = {}
            self.opPush(empty)

    # ------- String and Dictionary Operators --------------
    """ Pops a string or dictionary value from the operand stack and calculates the length of it. Pushes the length back onto the stack.
       The `length` method should support both DictionaryValue and StringValue values.
    """
    def length(self):
        if len(self.opstack) > 0:
            top = self.opPop() 
            if (isinstance(top, StringValue)):
                sliced = top.value[1:-1]
                self.opPush(len(sliced))
            elif (isinstance(top, DictionaryValue)):
                self.opPush(len(top.value))
            else:
                self.opPush(top)

    """ Pops either:
         -  "A (zero-based) index and an StringValue value" from opstack OR 
         -  "A `name` (i.e., a key) and DictionaryValue value" from opstack.  
        If the argument is a StringValue, pushes the ascii value of the the character in the string at the index onto the opstack;
        If the argument is an DictionaryValue, gets the value for the given `name` from DictionaryValue's dictionary value and pushes it onto the opstack
    """
    def get(self):
        if len(self.opstack) > 1:
            index = self.opPop()
            value = self.opPop()
            if (isinstance(value, StringValue)):
                self.opPush(ord(value.value[index+1]))
            elif (isinstance(value, DictionaryValue)):
                self.opPush(value.value[index])
            else:
                print("Error: get - one of the operands is not a valid value")
                self.opPush(value)
                self.opPush(index)             
        else:
            print("Error: get expects 2 operands")

   
    """
    Pops either:
    - "An `item`, a (zero-based) `index`, and an StringValue value from  opstack", OR
    - "An `item`, a `name`, and a DictionaryValue value from  opstack". 
    If the argument is a StringValue, replaces the character at `index` of the StringValue's string with the character having the ASCII value of `item`.
    If the argument is an DictionaryValue, adds (or updates) "name:item" in DictionaryValue's dictionary `value`.
    """
    def put(self):
        if len(self.opstack) > 2:
            item = self.opPop()
            index = self.opPop()
            value = self.opPop()
            if (isinstance(value, StringValue) and isinstance(item, int) and isinstance(index, int)):
                value.value = value.value[0:index+1] + chr(item) + value.value[index+2:]
            elif (isinstance(value, DictionaryValue)):
                value.value[index] = item
            else:
                print("Error: put - one of the operands is not a valid value")
                self.opPush(item)
                self.opPush(index)
                self.opPush(value)             
        else:
            print("Error: put expects 2 operands")

    """
    getinterval is a string only operator, i.e., works only with StringValue values. 
    Pops a `count`, a (zero-based) `index`, and an StringValue value from  opstack, and 
    extracts a substring of length count from the `value` of StringValue starting from `index`,
    pushes the substring back to opstack as a StringValue value. 
    """ 
    def getinterval(self):
        if len(self.opstack) > 2:
            count = self.opPop()
            index = self.opPop()
            value = self.opPop()
            if (isinstance(value, StringValue) and isinstance(count, int) and isinstance(index, int)):
                substring = '(' + value.value[index+1:index+count+1] + ')'
                newSV = StringValue(substring)
                self.opPush(newSV)
            else:
                self.opPush(value)
                self.opPush(index)
                self.opPush(count)

    """
    putinterval is a string only operator, i.e., works only with StringValue values. 
    Pops a StringValue value, a (zero-based) `index`, a `substring` from  opstack, and 
    replaces the slice in StringValue's `value` from `index` to `index`+len(substring)  with the given `substring`s value. 
    """
    def putinterval(self):
        if len(self.opstack) > 2:
            sub = self.opPop()
            index = self.opPop()
            value = self.opPop()
            if (isinstance(value, StringValue) and isinstance(sub, StringValue) and isinstance(index, int)):
                value.value = value.value[0:index+1] + str(sub)[14:-3] + value.value[index+len(str(sub)[14:-3])+1:]
            else:
                self.opPush(value)
                self.opPush(index)
                self.opPush(sub)

    """
    search is a string only operator, i.e., works only with StringValue values. 
    Pops two StringValue values: delimiter and inputstr
    if delimiter is a sub-string of inputstr then, 
       - splits inputstr at the first occurence of delimeter and pushes the splitted strings to opstack as StringValue values;
       - pushes True 
    else,
        - pushes  the original inputstr back to opstack
        - pushes False
    """
    def search(self):
        if len(self.opstack) > 1:
            delimiter = self.opPop()
            inputstr = self.opPop()
            if (isinstance(delimiter, StringValue) and (isinstance(inputstr, StringValue))):
                sliced1 = delimiter.value[1:-1]
                sliced2 = inputstr.value[1:-1]
                if sliced1 in sliced2:
                    splitstr = sliced2.split(sliced1, 1)
                    newstr1 = StringValue('')
                    newstr1.value = '(' + splitstr[1] + ')'
                    newstr2 = StringValue('')
                    newstr2.value = '(' + splitstr[0] + ')'
                    self.opPush(newstr1)
                    self.opPush(delimiter)
                    self.opPush(newstr2)
                    self.opPush(True)
                else: 
                    self.opPush(inputstr)
                    self.opPush(False)
            else:
                self.opPush(inputstr)
                self.opPush(delimiter)

    # ------- Operators that manipulate the dictstact --------------
    """ Pops a name and a value from stack, adds the definition to the dictionary at the top of the dictstack. """
    def psDef(self):
        if len(self.opstack) > 1:
            value = self.opPop()
            name = self.opPop()
            self.define(name, value)

    # ------- if/ifelse Operators --------------
    """ if operator
        Pops a CodeArrayValue object and a boolean value, if the value is True, executes (applies) the code array by calling apply.
       Will be completed in part-2. 
    """
    def psIf(self):
        if len(self.opstack) > 1:
            codearray = self.opPop()
            boolvalue = self.opPop()
            if (isinstance(codearray, CodeArrayValue) and isinstance(boolvalue, bool)):
                if boolvalue == True:
                    codearray.apply(self)
                else:
                    self.opPush(boolvalue)
                    self.opPush(codearray)    
            else:
                self.opPush(boolvalue)
                self.opPush(codearray)


    """ ifelse operator
        Pops two CodeArrayValue objects and a boolean value, if the value is True, executes (applies) the bottom CodeArrayValue otherwise executes the top CodeArrayValue.
        Will be completed in part-2. 
    """
    def psIfelse(self):
        if len(self.opstack) > 2:
            codearray1 = self.opPop()
            codearray2 = self.opPop()
            boolvalue = self.opPop()
            if (isinstance(codearray1, CodeArrayValue) and isinstance(codearray2, CodeArrayValue) and isinstance(boolvalue, bool)):
                if boolvalue == True:
                    codearray2.apply(self)
                else:
                    codearray1.apply(self)
            else:
                self.opPush(boolvalue)
                self.opPush(codearray2)
                self.opPush(codearray1)


    #------- Loop Operators --------------
    """
       Implements for operator.   
       Pops a CodeArrayValue object, the end index (end), the increment (inc), and the begin index (begin) and 
       executes the code array for all loop index values ranging from `begin` to `end`. 
       Pushes the current loop index value to opstack before each execution of the CodeArrayValue. 
       Will be completed in part-2. 
    """ 
    def psFor(self):
        if len(self.opstack) > 3:
            codearray = self.opPop()
            end = self.opPop()
            inc = self.opPop()
            begin = self.opPop()
            if (isinstance(codearray, CodeArrayValue) and isinstance(end, int) and isinstance(inc, int) and isinstance(begin, int)):
                for x in range(begin, end+inc, inc):
                    self.opPush(x)
                    codearray.apply(self)

    """ Cleans both stacks. """      
    def clearBoth(self):
        self.opstack[:] = []
        self.dictstack[:] = []

    """ Will be needed for part2"""
    def cleanTop(self):
        if len(self.opstack)>1:
            if self.opstack[-1] is None:
                self.opstack.pop()

