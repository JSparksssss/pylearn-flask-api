import ast
from pprint import pprint

def generate_tab(number):
    tab_list = []
    for i in range(number):
        tab_list.append("   ")
    return "".join(tab_list)

def while_cond_args(test,goto):
    if isinstance(test,ast.Compare):
        #The condition has one left node
        if(isinstance(test.left,ast.Name)):
            cond = "if variable "+ test.left.id +" "+ cmp_label(test.ops[0]) + " " + str(test.comparators[0].value) + " then goto " + goto
            return cond
    return True

def iter_args(iter,goto):
    if isinstance(iter,ast.Call):
        if(iter.func.id == "range"):
            cond = "if variable is out of range(" + str(iter.args[0].value) + ")"+" then goto " + goto
            return cond
    return True

#parse the operation
def operation_label(node):
    if isinstance(node,ast.Add):
        return "+"
    elif isinstance(node,ast.Mult):
        return "*"
    elif isinstance(node,ast.Div):
        return "/"
    elif isinstance(node,ast.Sub):
        return "-"

#for whileLoop
def cmp_label(node):
    if isinstance(node,ast.LtE):
        return "is greater than"
    elif isinstance(node,ast.GtE):
        return "is lower than"
    elif isinstance(node,ast.Lt):
        return "is greater than or equal to"
    elif isinstance(node,ast.Gt):
        return "is lower than or equal to"
    elif isinstance(node,ast.Eq):
        return "is not equal to"

def assign_id_or_value(node):
    if isinstance(node,ast.Constant):
        return node.value
    elif isinstance(node,ast.Name):
        return node.id

def parseAssign(tab,node):
    #判断有运算
    if isinstance(node,ast.BinOp) :
        left_node_is_null = isinstance(node.left,ast.Name)or isinstance(node.left,ast.Constant)
        right_node_is_null = isinstance(node.right,ast.Name)or isinstance(node.right,ast.Constant)
        if left_node_is_null and right_node_is_null:     
            row = generate_tab(tab)+ast.unparse(node)
            file.write(row)
            file.write('\n')
            return "("+ ast.unparse(node)+ ")"

        elif left_node_is_null == False and right_node_is_null == False:
            left_node =str(parseAssign(tab,node.left))
            right_node = str(parseAssign(tab,node.right))
            result = left_node + " "+ operation_label(node.op) + " "+ right_node
            row = generate_tab(tab)+result
            file.write(row)
            file.write('\n')
            return result

        elif left_node_is_null == True :
            left_node = str(assign_id_or_value(node.left))
            right_node = str(parseAssign(tab,node.right))
            result = left_node + " "+ operation_label(node.op) + " "+ right_node
            row = generate_tab(tab)+result
            file.write(row)
            file.write('\n')
            return result

        elif right_node_is_null == True :
            left_node =str(parseAssign(tab,node.left))
            right_node = str(assign_id_or_value(node.right))
            result = left_node + " "+ operation_label(node.op) + " "+ right_node
            row = generate_tab(tab)+result
            file.write(row)
            file.write('\n')
            return result

    elif isinstance(node,ast.Name):
        return node.id
    elif isinstance(node,ast.Constant):
        return node.value
def parseForLoop(tab,node):
    row = generate_tab(tab)+"ForLoop:"
    file.write(row)
    file.write('\n')

    #The args
    if node.iter:
        cond = iter_args(node.iter,"ForLoopDone")
        row = generate_tab(tab+1)+cond
        file.write(row)
        file.write('\n')

    parse_body(tab + 1,node.body)


    #modify the iter number
    #
    #
    #


    row = generate_tab(tab + 1) +"goto ForLoop"
    file.write(row)
    file.write('\n')

    row = generate_tab(tab) + "ForLoopDone"
    file.write(row)
    file.write('\n')

    return True

##add try catch
def parseWhileLoop(tab,node):
    row = generate_tab(tab)+"WhileLoop:"
    file.write(row)
    file.write('\n')

    #The args
    if node.test:
        cond = while_cond_args(node.test,"WhileLoopDone")
        print(generate_tab(tab)+cond)
        row = generate_tab(tab)+cond
        file.write(row)
        file.write('\n')

    parse_body(tab + 1,node.body)

    row = generate_tab(tab + 1) +"goto WhileLoop"
    file.write(row)
    file.write('\n')

    row = generate_tab(tab) + "WhileLoopDone"
    file.write(row)
    file.write('\n')

    return True

def parseExpr(tab,node):
    if node.value and isinstance(node.value,ast.Call):
        row = generate_tab(tab)+"call function "+ node.value.func.id
        file.write(row)
        file.write('\n')
        plural = True if len(node.value.args) >= 2 else False
        if plural:
            args = " ".join([ str(arg.value) for arg in node.value.args ])
            row = generate_tab(tab)+ "input args: " + args
            file.write(row)
            file.write('\n')
        else:
            if(hasattr(node.value.args[0],"id")):
                row = generate_tab(tab)+ "input arg:" + node.value.args[0].id
            elif(hasattr(node.value.args[0],"value")):
                row = generate_tab(tab)+ "input arg:" + node.value.args[0].value
            file.write(row)  
            file.write('\n')   
    return True

def parseIfElse(tab,node):
    if isinstance(node.test, ast.Compare):
        row = generate_tab(tab)+"If " + str(node.test.left.id) + " " + str(cmp_label(node.test.ops[0])) + " "+ str(node.test.comparators[0].value) + ", then skip the code"
    file.write(row)
    file.write("\n")

    parse_body(tab + 1, node.body)

    if hasattr(node,'orelse'):
        if isinstance(node.test, ast.Compare):
            row = generate_tab(tab)+"If " + str(node.test.left.id) + " " + str(cmp_label(node.test.ops[0])) + " "+ str(node.test.comparators[0].value) + ", then run these code"
        file.write(row)
        file.write("\n")

        parse_body(tab + 1, node.orelse)
    
    return True

def parse_body(tab,body):
    for node in body :    
        if isinstance(node,ast.Assign):
            result = str(parseAssign(tab,node.value))
            row = generate_tab(tab) + node.targets[0].id + " " + "=" + " "+result
            file.write(row)
            file.write('\n')
        elif isinstance(node,ast.For):
            parseForLoop(tab,node)
        elif isinstance(node,ast.While):
            parseWhileLoop(tab,node)
        elif isinstance(node,ast.FunctionDef):
            print("ast.FunctionDef")
            print(node)
        elif isinstance(node,ast.Expr):
        #check value whether it is call function
            parseExpr(tab,node)
        elif isinstance(node,ast.If):
            parseIfElse(tab,node)
        #elif isinstance(node,ast.Switch):
        #Python not like to provide switch function
    
def parse_ast_tree(tab,tree):
    if isinstance(tree,ast.Module):
        # row = "Module Start"
        # file.write(row)
        # file.write('\n')
        row = "st=>start: Module Start"
        flowchart_file.write(row)
        flowchart_file.write('\n')

    # parse_body(tab,tree.body)
        
    if isinstance (tree,ast.Module):
        # row = "Module Done"
        # file.write(row)
        # file.write('\n')
        row = "e=>end: Module End"
        flowchart_file.write(row)
        flowchart_file.write('\n')
        

#Main function
def parse_flowchart_code(filename):
    ##To record all steps for output
    steps = []
    #Add a function to run the code to check whether there are any problems

    #No indent for the first row in the parse bracket
#     tree = ast.parse("""
# a = 1
# b = (a + 1)*2
# for i in range(3):
#     for j in range(2):
#         print(b)
# """)
    global file
    global flowchart_file
    file = open("pseudo_code.txt", 'w')
    flowchart_file = open("flowchart.txt", 'w')
    print(flowchart_file)
    code = ""
    with open(filename) as f:
        code = code + f.read()
    print("[ast_node.py]Origin code is:",code)
    tree = ast.parse(code)

    astTree = ast.dump(tree)
    pprint(astTree) #Print tree
    # pprint(tree.body) #Print all child nodes

    parse_ast_tree(1,tree)

    #Remember close all file pointers
    file.close()
    flowchart_file.close()
