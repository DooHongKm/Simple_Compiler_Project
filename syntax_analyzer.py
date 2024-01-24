import sys
from anytree import Node, RenderTree
from anytree.exporter import DotExporter

# LINUX에서 입력받은 파일이름으로 파일 내용을 input에 저장
# "python syntax_analyzer.py input.txt"로 실행 가능
input_file = sys.argv[1]
with open(input_file, 'r') as file:
    input = file.read()



# input을 tokenize하여 리스트에 저장
# input을 사용하면 외부 파일에서 input sequence을 받아와 파싱 가능
# input1, input2를 사용하면 위에 명시된 input sequence를 파싱 가능
tokens = input.split(' ')
tokens.append('$') 

# SLR Parsing에 이용되는 non-ambiguous한 grammars
# 첫번째 grammar는 0번, 마지막 grammar는 38번 -> 총 39개의 grammar
slr_grammars = """CODE -> VDECL CODE
CODE -> FDECL CODE
CODE -> CDECL CODE
CODE -> epsilon
VDECL -> vtype id semi
VDECL -> vtype ASSIGN semi
ASSIGN -> id assign RHS
RHS -> EXPR
RHS -> literal
RHS -> character
RHS -> boolstr
EXPR -> EXPR addsub EXPR1
EXPR -> EXPR1
EXPR1 -> EXPR1 multdiv EXPR2
EXPR1 -> EXPR2
EXPR2 -> lparen EXPR rparen
EXPR2 -> id
EXPR2 -> num
FDECL -> vtype id lparen ARG rparen lbrace BLOCK RETURN rbrace
ARG -> vtype id MOREARGS
ARG -> epsilon
MOREARGS -> comma type id MOREARGS
MOREARGS -> epsilon
BLOCK -> STMT BLOCK
BLOCK -> epsilon
STMT -> VDECL
STMT -> ASSIGN semi
STMT -> if lparen COND rparen lbrace BLOCK rbrace ELSE
STMT -> while lparen COND rparen lbrace BLOCK rbrace
COND -> COND comp COND1
COND -> COND1
COND1 -> boolstr
ELSE -> else lbrace BLOCK rbrace
ELSE -> epsilon
RETURN -> return RHS semi
CDECL -> class id lbrace ODECL rbrace
ODECL -> VDECL ODECL
ODECL -> FDECL ODECL
ODECL -> epsilon"""

# 39개의 grammar가 들어있는 리스트 생성
grammars = slr_grammars.split('\n')

# table 각 열의 이름 = key
keys = ['vtype', 'id', 'assign', 'literal', 'character', 'boolstr',
        'addsub', 'multdiv', 'lparen', 'rparen', 'num', 'lbrace',
        'rbrace', 'comma', 'type', 'if', 'whlie', 'comp', 'else',
        'return', 'class', '$', 'CODE', 'VDECL', 'ASSIGN', 'RHS',
        'EXPR', 'EXPR1', 'EXPR2', 'FDECL', 'ARG', 'MOREARGS', 'BLOCK',
        'STMT', 'COND', 'COND1', 'ELSE', 'RETURN', 'CDECL', 'ODECL']

# table의 행의 index는 state를 표현
# table의 모든 값을 None으로 초기화
# table에서 값이 존재하는 경우에만 업데이트
terms = {}
for key in keys: terms[key] = None
table = [terms.copy() for _ in range(86)]
table[0].update({'vtype' : 's2', 'VDECL' : 1})
table[1].update({'vtype' : 's6', 'class' : 's7', '$' : 'r3', 'CODE' : 3, 'VDECL' : 1, 'FDECL' : 4, 'CDECL' : 5})
table[2].update({'id' : 's8', 'ASSIGN' : 9})
table[3].update({'$' : 'acc'})
table[4].update({'vtype' : 's6', 'class' : 's7', '$' : 'r3', 'CODE' : 10, 'VDECL' : 1, 'FDECL' : 4, 'CDECL' : 5})
table[5].update({'vtype' : 's6', 'class' : 's7', '$' : 'r3', 'CODE' : 11, 'VDECL' : 1, 'FDECL' : 4, 'CDECL' : 5})
table[6].update({'id' : 's12', 'ASSIGN' : 9})
table[7].update({'id' : 's13'})
table[8].update({'semi' : 's14', 'assign' : 's15'})
table[9].update({'semi' : 's16'})
table[10].update({'$' : 'r1'})
table[11].update({'$' : 'r2'})
table[12].update({'semi' : 's14', 'assign' : 's15', 'lparen' : 's17'})
table[13].update({'lbrace' : 's18'})
table[14].update({'vtype' : 'r4', 'id' : 'r4', 'rbrace' : 'r4', 'if' : 'r4', 'while' : 'r4', 'return' : 'r4', 'class' : 'r4', '$' : 'r4'})
table[15].update({'id' : 's27', 'literal' : 's21', 'character' : 's22', 'boolstr' : 's23', 'lparen' : 's26', 'num' : 's28', 'RHS' : 19, 'EXPR' : 20, 'EXPR1' : 24, 'EXPR2' : 25})
table[16].update({'vtype' : 'r5', 'id' : 'r5', 'rbrace' : 'r5', 'if' : 'r5', 'while' : 'r5', 'return' : 'r5', 'class' : 'r5', '$' : 'r5'})
table[17].update({'vtype' : 's30', 'rparen' : 'r20', 'ARG' : 29, '' : '', '' : '', '' : ''})
table[18].update({'vtype' : 's6', 'rbrace' : 'r38', 'VDECL' : 32, 'FDECL' : 33, 'CDECL' : 31, '' : ''})
table[19].update({'semi' : 'r6'})
table[20].update({'semi' : 'r7', 'addsub' : 's34'})
table[21].update({'semi' : 'r8'})
table[22].update({'semi' : 'r9'})
table[23].update({'semi' : 'r10'})
table[24].update({'semi' : 'r12', 'addsub' : 'r12', 'multdiv' : 's35', 'rparen' : 'r12'})
table[25].update({'semi' : 'r14', 'addsub' : 'r14', 'multdiv' : 'r14', 'rparen' : 'r14'})
table[26].update({'id' : 's27', 'lparen' : 's26', 'num' : 's28', 'EXPR' : 36, 'EXPR1' : 24, 'EXPR2' : 25})
table[27].update({'semi' : 'r16', 'addsub' : 'r16', 'multdiv' : 'r16', 'rparen' : 'r16'})
table[28].update({'semi' : 'r17', 'addsub' : 'r17', 'multdiv' : 'r17', 'rparen' : 'r17'})
table[29].update({'rparen' : 's37'})
table[30].update({'id' : 's38'})
table[31].update({'rbrace' : 's39'})
table[32].update({'vtype' : 's6', 'rbrace' : 'r38', 'VDECL' : 32, 'FDECL' : 33, 'CDECL' : 40})
table[33].update({'vtype' : 's6', 'rbrace' : 'r38', 'VDECL' : 32, 'FDECL' : 33, 'CDECL' : 41})
table[34].update({'id' : 's27', 'lparen' : 's26', 'num' : 's28', 'EXPR1' : 42, 'EXPR2' : 25})
table[35].update({'id' : 's27', 'lparen' : 's26', 'num' : 's28', 'EXPR2' : 43})
table[36].update({'addsub' : 's34', 'rparen' : 's44'})
table[37].update({'lbrace' : 's45'})
table[38].update({'rparen' : 'r22', 'comma' : 's47', 'MOREARGS' : 46})
table[39].update({'vtype' : 'r35', 'class' : 'r35', '$' : 'r35'})
table[40].update({'rbrace' : 'r36'})
table[41].update({'rbrace' : 'r37'})
table[42].update({'assign' : 'r11', 'addsub' : 'r11', 'multdiv' : 's35', 'rparen' : 'r11'})
table[43].update({'assign' : 'r13', 'addsub' : 'r13', 'multdiv' : 'r13', 'rparen' : 'r13'})
table[44].update({'assign' : 'r15', 'addsub' : 'r15', 'multdiv' : 'r15', 'rparen' : 'r15'})
table[45].update({'vtype' : 's2', 'id' : 's54', 'rbrace' : 'r24', 'if' : 's52', 'while' : 's53', 'return' : 'r24', 'VDECL' : 50, 'ASSIGN' : 51, 'BLOCK' : 48, 'STMT' : 49})
table[46].update({'rparen' : 'r19'})
table[47].update({'type' : 's55'})
table[48].update({'return' : 's57', 'RETURN' : 56})
table[49].update({'vtype' : 's2', 'id' : 's54', 'rbrace' : 'r24', 'if' : 's52', 'while' : 's53', 'return' : 'r24', 'VDECL' : 50, 'ASSIGN' : 51, 'BLOCK' : 58, 'STMT' : 49})
table[50].update({'vtype' : 'r25', 'id' : 'r25', 'rbrace' : 'r25', 'if' : 'r25', 'while' : 'r25', 'return' : 'r25'})
table[51].update({'semi' : 's59'})
table[52].update({'lparen' : 's60'})
table[53].update({'lparen' : 's61'})
table[54].update({'assign' : 's15'})
table[55].update({'id' : 's62'})
table[56].update({'rbrace' : 's63'})
table[57].update({'id' : 's27', 'literal' : 's21', 'character' : 's22', 'boolstr' : 's23', 'lparen' : 's26', 'num' : 's28', 'RHS' : 64, 'EXPR' : 20, 'EXPR1' : 24, 'EXPR2' : 25, '' : '', '' : ''})
table[58].update({'rbrace' : 'r23', 'return' : 'r23'})
table[59].update({'vtype' : 'r26', 'id' : 'r26', 'rbrace' : 'r26', 'if' : 'r26', 'while' : 'r26', 'return' : 'r26'})
table[60].update({'boolstr' : 's67', 'COND' : 65, 'COND1' : 66})
table[61].update({'boolstr' : 's67', 'COND' : 68, 'COND1' : 66})
table[62].update({'rparen' : 'r22', 'comma' : 's47', 'MOREARGS' : 69})
table[63].update({'vtype' : 'r18', 'rbrace' : 'r18', 'class' : 'r18', '$' : 'r18'})
table[64].update({'semi' : 's70'})
table[65].update({'rparen' : 's71', 'comp' : 's72'})
table[66].update({'rparen' : 'r30', 'comp' : 'r30'})
table[67].update({'rparen' : 'r31', 'comp' : 'r31'})
table[68].update({'rparen' : 's73', 'comp' : 's72'})
table[69].update({'rparen' : 'r21'})
table[70].update({'rbrace' : 'r34'})
table[71].update({'lbrace' : 's74'})
table[72].update({'boolstr' : 's67', 'COND1' : 75})
table[73].update({'lbrace' : 's76'})
table[74].update({'vtype' : 's2', 'id' : 's54', 'rbrace' : 'r24', 'if' : 's52', 'while' : 's53', 'return' : 'r24', 'VDECL' : 50, 'ASSIGN' : 51, 'BLOCK' : 77, 'STMT' : 49})
table[75].update({'rparen' : 'r29', 'comp' : 'r29'})
table[76].update({'vtype' : 's2', 'id' : 's54', 'rbrace' : 'r24', 'if' : 's52', 'while' : 's53', 'return' : 'r24', 'VDECL' : 50, 'ASSIGN' : 51, 'BLOCK' : 78, 'STMT' : 49})
table[77].update({'rbrace' : 's79'})
table[78].update({'rbrace' : 's80'})
table[79].update({'vtype' : 'r33', 'id' : 'r33', 'rbrace' : 'r33', 'if' : 'r33', 'while' : 'r33', 'else' : 's82', 'return' : 'r33', 'ELSE' : 81})
table[80].update({'vtype' : 'r28', 'id' : 'r28', 'rbrace' : 'r28', 'if' : 'r28', 'while' : 'r28', 'return' : 'r28'})
table[81].update({'vtype' : 'r27', 'id' : 'r27', 'rbrace' : 'r27', 'if' : 'r27', 'while' : 'r27', 'return' : 'r27',})
table[82].update({'lbrace' : 's83'})
table[83].update({'vtype' : 's2', 'id' : 's54', 'rbrace' : 'r24', 'if' : 's52', 'while' : 's53', 'return' : 'r24', 'VDECL' : 50, 'ASSIGN' : 51, 'BLOCK' : 84, 'STMT' : 49})
table[84].update({'rbrace' : 's85'})
table[85].update({'vtype' : 'r32', 'id' : 'r32', 'rbrace' : 'r32', 'if' : 'r32', 'while' : 'r32', 'return' : 'r32'})

class Stack():
    # stack 생성 함수
    def __init__(self):
        self.stack = []
    # stack에 data를 쌓는 함수
    def push(self, data):
        self.stack.append(data)
    # stack 가장 위에 있는 data를 추출하는 함수
    def pop(self):
        pop_object = None
        if self.isEmpty():
            print("Stack is Empty")
        else:
            pop_object = self.stack.pop()
        return pop_object
    # stack 가장 위에 있는 data를 반환하는 함수
    def top(self):
        top_object = None
        if self.isEmpty():
            print("Stack is Empty")
        else:
            top_object = self.stack[-1]
        return top_object
    # stack이 비어있는지 반환하는 함수
    def isEmpty(self):
        is_empty = False
        if len(self.stack) == 0:
            is_empty = True
        return is_empty
    # stack의 사이즈를 반환하는 함수
    def size(self):
        return len(self.stack)
    # stack의 내용을 출력하는 함수
    def printStack(self):
        for item in self.stack:
            print(item, end=' ')
        print()

s1 = Stack()    # state 정보를 나타내는 state Stack
s2 = Stack()    # splitter의 왼쪽을 나타내는 node Stack
s1.push(0)    # 시작 state는 0이므로, 0을 s1에 push

cnt = 0    # input 내에서 splitter의 위치
accept = True    # 최종적으로 bool=True이면 Accept, bool=False이면 Reject
error = False    # error=True이면 코드 수정 필요
root = Node("CODE")    # parse tree의 root node 생성

# Main Parsing Code
while True:
    # Reject
    if table[s1.top()][tokens[cnt]] == None:
        accept = False
        break
    # Shift
    elif table[s1.top()][tokens[cnt]][0] == "s":
        new_node = Node(tokens[cnt])
        s1.push(int(table[s1.top()][tokens[cnt]][1:]))
        s2.push(new_node)
        cnt += 1
    # Reduce & Goto
    elif table[s1.top()][tokens[cnt]][0] == "r":
        index = int(table[s1.top()][tokens[cnt]][1:])
        temp = grammars[index].split(" -> ")
        left = temp[0]; right = temp[1].split()
        new_node = Node(left)
        child = []
        # epsilon을 reduce하는 경우, epsilon 노드 추가
        if right == ["epsilon"]:
            e_node = Node("ε", parent=new_node)
        # epsilon이 아닌 경우, s2에서 노드를 추출
        else:
            for _ in range(len(right)):
                s1.pop()
                child.append(s2.pop())
        # pop()으로 노드를 추출했으므로 순서가 역순
        # 노드를 parent와 연결할 때, 원래 순서대로 바꾸어 연결
        for i in range(len(child)-1, -1, -1):  
            child[i].parent = new_node                      
        s2.push(new_node)
        s1.push(int(table[s1.top()][s2.top().name]))
    # Accept
    elif table[s1.top()][tokens[cnt]] == "acc":
        child = []
        for _ in range(s2.size()): child.append(s2.pop())
        # pop()으로 노드를 추출했으므로 순서가 역순
        # 노드를 parent와 연결할 때, 원래 순서대로 바꾸어 연결      
        for i in range(len(child)-1, -1, -1):
            child[i].parent = root
        break
    # Error
    # None, s, r, acc 외의 값이 테이블에 존재하면 코드 수정이 필요
    else:
        accept = False
        error = True
        break

# tree 출력
if accept == True:
    print("Accept!")
    for pre, _, node in RenderTree(root):
        print(f"{pre}{node.name}")    
# reject된 이유 출력
elif error == False:
    print("Reject!")
    print(f"There is no value in table[{s1.top()}][{s2.top().name}]")
else:
    print("Error!")
    print("You need to edit your code")