import json


KEYWORDS = ["var","if","else","parent","elif","for","in","step","while","return","break","this","continue","true","false","null"]
DIGITS = "0123456789"
LETTERS = "qwertzuiopasdfghjklyxcvbnmQWERTZUIOPASDFGHJKLYXCVBNM"
LETTERS_WITH_DIGITS = LETTERS + DIGITS

#### TOKENS ####

T_INTEGER      = "INT"
T_FLOAT        = "FLOAT"
T_STRING       = "STRING"
T_IDENTIFIER   = "IDENTIFIER"
T_KEYWORD      = "KEYWORD"
T_PLUS         = "PLUS"
T_MINUS        = "MINUS"
T_ARROW        = "ARROW"
T_MUL          = "MUL"
T_DIV          = "DIV"
T_ASSIGN       = "ASSIGN"
T_EQUAL        = "EQUAL"
T_NOT_EQUAL    = "NOT_EQUAL"
T_LPAREN       = "LPAREN"
T_RPAREN       = "RPAREN"
T_LSQUARE      = "LSQUARE"
T_RSQUARE      = "RSQUARE"
T_COLON        = "COLON"
T_LBRACKET     = "LBRACKET"
T_RBRACKET     = "RBRACKET"
T_COMMA        = "COMMA"
T_DOT          = "DOT"
T_NEWLINE      = "NEWLINE"
T_ENDOFLINE    = "ENDOFLINE"
T_LESSER       = "LESSER"
T_GREATER      = "GREATER"
T_LESSEREQUAL  = "LESSEREQUAL"
T_GREATEREQUAL = "GREATEREQUAL"


class Token:
	def __init__(self, type_, value=None, pos_start=None, pos_end=None):
		self.type = type_
		self.value = value

		if pos_start:
			self.pos_start = pos_start
			self.pos_end = pos_start+1
			

		if pos_end:
			self.pos_end = pos_end
	
	def __repr__(self):
		if self.value: return f'{self.type}:{self.value}'
		return f'{self.type}'


class Lexer():
    def __init__(self,function,text):
        self.function = function
        self.text = text
        self.pos = 0
        self.current_char = text[0]
        


    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
    
    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char == " " or self.current_char == "\t" or self.current_char == "\n":
                self.advance()
            elif self.current_char == ";" :
                tokens.append(Token(T_NEWLINE,pos_start=self.pos))
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char in LETTERS:
                tokens.append(self.make_identifier())
            elif self.current_char == '"':
                tokens.append(self.make_string())
            elif self.current_char == ":":
                tokens.append(Token(T_COLON,pos_start=self.pos))
                self.advance()
            elif self.current_char == "+":
                tokens.append(Token(T_PLUS,pos_start=self.pos))
                self.advance()
            elif self.current_char == "-":
                tokens.append(self.make_minus_or_arrow())
                self.advance()
            elif self.current_char == "/":
                tokens.append(Token(T_DIV,pos_start=self.pos))
                self.advance()
            elif self.current_char == "*":
                tokens.append(Token(T_MUL,pos_start=self.pos))
                self.advance()
            elif self.current_char == "(":
                tokens.append(Token(T_LPAREN,pos_start=self.pos))
                self.advance()
            elif self.current_char == ")":
                tokens.append(Token(T_RPAREN,pos_start=self.pos))
                self.advance()
            elif self.current_char == "[":
                tokens.append(Token(T_LSQUARE,pos_start=self.pos))
                self.advance()
            elif self.current_char == "]":
                tokens.append(Token(T_RSQUARE,pos_start=self.pos))
                self.advance()
            elif self.current_char == "{":
                tokens.append(Token(T_LBRACKET,pos_start=self.pos))
                self.advance()
            elif self.current_char == "}":
                tokens.append(Token(T_RBRACKET,pos_start=self.pos))
                self.advance()
            elif self.current_char == "!":
                token,error = self.make_not_equals()
                if error: 
                    return [], error
                tokens.append(token)
            elif self.current_char == "=":
                tokens.append(self.make_equals())
            elif self.current_char == "<":
                tokens.append(self.make_less_than())
            elif self.current_char == ">":
                tokens.append(self.make_greater_than())
            elif self.current_char == ".":
                tokens.append(Token(T_DOT,pos_start=self.pos))
                self.advance()
            elif self.current_char == ",":
                tokens.append(Token(T_COMMA,pos_start=self.pos))
                self.advance()
            else:
                pos_start = self.pos
                char = self.current_char
                self.advance()
                return [], Exception("IllegalCharError: at {} char: {}".format(pos_start,char))
            
        tokens.append(Token(T_ENDOFLINE,pos_start=self.pos))
        return tokens,None

    def make_number(self):
        number_string = ""
        dot_count = 0
        pos_start = self.pos

        while self.current_char != None and self.current_char in DIGITS + ".":
            if self.current_char == ".":
                if dot_count == 1: break
                dot_count +=1

            number_string += self.current_char
            self.advance()
        
        if dot_count == 0:
            return Token(T_INTEGER, value=int(number_string),pos_start=pos_start,pos_end=self.pos)
        else:
            return Token(T_FLOAT, value=float(number_string),pos_start=pos_start,pos_end=self.pos)
    
    def make_string(self):
        string = ""
        pos_start = self.pos
        self.advance()

        while self.current_char != None and self.current_char != '"':
            string += self.current_char
            self.advance()
        self.advance()
        return Token(T_STRING,string,pos_start=pos_start,pos_end=self.pos)

    def make_minus_or_arrow(self):
        token_type = T_MINUS
        pos_start = self.pos
        self.advance()
        if self.current_char == ">":
            # self.advance()
            token_type = T_ARROW
        
        return Token(token_type,pos_start=pos_start, pos_end=self.pos)

    def make_identifier(self):
        identifier_string = ""
        pos_start = self.pos

        while self.current_char != None and self.current_char in LETTERS_WITH_DIGITS+"_":
            identifier_string += self.current_char
            self.advance()

        token_type = T_KEYWORD if identifier_string in KEYWORDS else T_IDENTIFIER
        return Token(token_type,identifier_string,pos_start=pos_start,pos_end=self.pos)
        

    def make_not_equals(self):
        pos_start = self.pos
        self.advance()

        if self.current_char == "=":
            self.advance()
            return Token(T_NOT_EQUAL,pos_start=pos_start,pos_end=self.pos)
        self.advance()
        return None, Exception("Expected Character '=' after '!' at {}".format(pos_start+1))
    
    def make_equals(self):
        token_type = T_ASSIGN
        pos_start = self.pos
        self.advance()

        if self.current_char == '=':
            self.advance()
            token_type = T_EQUAL
        return Token(token_type, pos_start=pos_start, pos_end=self.pos)
    
    def make_less_than(self):
        token_type = T_LESSER
        pos_start = self.pos
        self.advance()
        if self.current_char == "=":
            self.advance()
            token_type == T_LESSEREQUAL
        return Token(token_type,pos_start=pos_start,pos_end=self.pos)
        

    def make_greater_than(self):
        token_type = T_GREATER
        pos_start = self.pos
        self.advance()
        if self.current_char == "=":
            self.advance()
            token_type == T_GREATEREQUAL
        return Token(token_type,pos_start=pos_start,pos_end=self.pos)



class NameValuePairNode:
    def __init__(self,name,value_token):
        self.name = name
        self.value_token = value_token
    
    def __repr__(self):
        return f"NameValuePairNode({self.name},{self.value_token})"


class ValueNode:
    def __init__(self,value_token):
        self.value_token = value_token

    def __repr__(self):
        return self.value_token

class BinaryNode:
    def __init__(self,value:bool):
        self.value = value

    def __repr__(self):
        return f"BinaryNode({self.value})"

class NoneNode:
    def __repr__(self):
        return "NoneNode()"

class ObjectNode:
    def __init__(self,name_value_pair_nodes):
        self.name_value_pair_nodes = name_value_pair_nodes

    def __repr__(self):
        arr = []
        for nvp_node in self.name_value_pair_nodes:
            arr.append(nvp_node)
        return f"ObjectNode({arr})"
class ArrayNode:
    def __init__(self,object_nodes):
        self.object_nodes = object_nodes
    
    def __repr__(self):
        return f"ArrayNode({self.object_nodes})"

class StringNode:
    def __init__(self,string):
        self.string = string

    def __repr__(self):
        return f'StringNode("{self.string}")'

class IntegerNode:
    def __init__(self,integer):
        self.integer = integer

    def __repr__(self):
        return f'IntegerNode({self.integer})'

class ListNode:
  def __init__(self, element_nodes):
    self.element_nodes = element_nodes

class VarAccessNode:
    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok

    def __repr__(self):
        return 'VarAccessNode("{}")'.format(self.var_name_tok)

class VarAssignNode:
    def __init__(self, var_name_tok, value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node

    def __repr__(self):
        return 'VarAssignNode("{}",{})'.format(self.var_name_tok,self.value_node)

class BinOpNode:
  def __init__(self, left_node, op_tok, right_node):
    self.left_node = left_node
    self.op_tok = op_tok
    self.right_node = right_node

  def __repr__(self):
    return f'BinOpNode({self.left_node}, {self.op_tok}, {self.right_node})'

class UnaryOpNode:
  def __init__(self, op_tok, node):
    self.op_tok = op_tok
    self.node = node

  def __repr__(self):
    return f'({self.op_tok}, {self.node})'

class IfNode:
  def __init__(self, cases, else_case):
    self.cases = cases
    self.else_case = else_case

class ForNode:
  def __init__(self, var_name_tok, start_value_node, end_value_node, step_value_node, body_node, should_return_null):
    self.var_name_tok = var_name_tok
    self.start_value_node = start_value_node
    self.end_value_node = end_value_node
    self.step_value_node = step_value_node
    self.body_node = body_node
    self.should_return_null = should_return_null

class WhileNode:
    def __init__(self,condition_node, body_node, should_return_null):
        self.condition_node = condition_node
        self.body_node = body_node
        self.should_return_null = should_return_null

class FuncDefNode:
    def __init__(self,body_node):
        self.body_node = body_node
    
    def __repr__(self):
        str_ = "FunctionDefNode("
        for element in self.body_node:
            str_ += str(element) + ","
        str_ = str_[:-1] + ")"
        return str_

class ThisNode:
    def __init__(self,after_identifier):
        self.after_identifier = after_identifier
    def __repr__(self):
        return "ThisNode({})".format(self.after_identifier)

class ChildAccessNode:
    def __init__(self,access_node):
        self.access_node = access_node

    def __repr__(self):
        return "ChildAccessNode({})".format(self.access_node)

class ReturnNode:
    def __init__(self,node_to_return):
        self.node_to_return = node_to_return

    def __repr__(self):
        return 'ReturnNode({})'.format(self.node_to_return)
class ContinueNode:
    def __init__(self):
        pass

class BreakNode:
    def __init__(self):
        pass

class Parser:
    def __init__(self,tokens):
        self.tokens = tokens
        self.token_index = -1
        self.advance()
    
    def advance(self,amount=1):
        self.token_index += amount
        self.current_token = self.tokens[self.token_index]
        return self.current_token

    def reverse(self, amount=1):
        self.token_index -= amount
        self.current_token = self.tokens[self.token_index]
        return self.current_token

    def parse(self):
        while self.current_token.type != T_ENDOFLINE:
            if self.current_token.type == T_LBRACKET:
                return self.create_object_node()
            elif self.current_token.type == T_LSQUARE:
                return self.create_array_node()

            self.advance()

    def create_array_node(self):
        left_square_counter = 0
        array_objects = []
        self.advance()

        while True:
            if self.current_token.type == T_LSQUARE:
                left_square_counter +=1
            elif self.current_token.type == T_RSQUARE:
                if left_square_counter > 0:
                    left_square_counter -= 1
                else:
                    break
            
            elif self.current_token.type == T_LBRACKET:
                
                array_objects.append(self.create_object_node())
            elif self.current_token.type == T_COMMA:
                pass
            else:
                array_objects.append(self.expr())
                self.advance()
            
            self.advance()
        return ArrayNode(array_objects)

    def create_object_node(self):
        left_bracket_counter = 0

        name_value_pair_nodes = []
        self.advance()
        while True:
            if self.current_token.type == T_LBRACKET:
                left_bracket_counter += 1
            elif self.current_token.type == T_RBRACKET:
                if left_bracket_counter > 0:
                    left_bracket_counter -= 1
                else:
                    break
            
            elif self.current_token.type == T_COLON:
                name_value_pair_nodes.append(self.expr())


            self.advance()
        
        return ObjectNode(name_value_pair_nodes)

        
    def func(self):
        self.advance()
        function_body = []
        if self.current_token.type != T_LBRACKET:
            raise Exception('Unexpected Character: Expected "{" at {}'.format(self.token_index))
        else:
            self.advance()
            while self.current_token.type != T_RBRACKET:
                function_body.append(self.atom())
                self.advance()
            return FuncDefNode(function_body)
                

    def atom(self):
        print(self.current_token)
        if self.current_token.type == T_KEYWORD and self.current_token.value == "var":
            self.advance()

            if self.current_token.type != T_IDENTIFIER:
                raise Exception("Unexpected Character: Expected and identifier")
            
            
            identifier = self.current_token.value
            self.advance()
            if self.current_token.type != T_ASSIGN:
                raise Exception('Unexpected Character: Expected "=" at {}'.format(self.token_index))
            
            self.advance()

            value_node = self.fexpr()
            print("value node", value_node)
            return VarAssignNode(identifier,value_node)

        if self.current_token.type == T_KEYWORD and self.current_token.value == "if":
            self.advance()
            if_cases, else_case = self.create_if_inside()
            return IfNode(if_cases,else_case)
            
        if self.current_token.type == T_KEYWORD:
            if self.current_token.value == "return":
                self.advance()
                returned_node = self.atom()
                node = ReturnNode(returned_node)
                if self.current_token.type == T_KEYWORD and self.current_token.value == "this":
                    return self.atom()
                if self.current_token.type != T_NEWLINE:
                    print("current token",self.current_token)
                    raise Exception("Expected ';' after return")

                return node
            if self.current_token.value == "this":
                self.advance()
                if self.current_token.type != T_DOT:
                    if self.current_token.type == T_NEWLINE:
                        return ThisNode([])
                    raise Exception("Expected '.' at {}".format(self.current_token.pos_start))
                self.advance()
                

                if self.current_token.type != T_IDENTIFIER:
                    raise Exception("Expected identifier at {}".format(self.current_token.pos_start))
                self.reverse()

                this_node = ThisNode(self.this_children())
                if self.current_token.type in [T_MINUS,T_PLUS,T_MUL,T_DIV]:
                    op = self.current_token
                    self.advance()
                    this_node = self.add_bin_op(this_node,op,self.current_token)
                    

                return this_node
            
            if self.current_token.value == "true":
                self.advance()
                return BinaryNode(True)
            if self.current_token.value == "false":
                self.advance()
                return BinaryNode(False)
            if self.current_token.value == "null":
                self.advance()
                return NoneNode()

        if self.current_token.type == T_IDENTIFIER:
            identifier = self.current_token.value
            
            self.advance()
            if self.current_token.type == T_ASSIGN:
                self.advance()
                value_node = self.atom()
                return VarAssignNode(identifier,value_node)
            elif self.current_token.type in [T_MUL,T_MINUS,T_PLUS,T_DIV]:
                self.reverse()
                print(self.current_token)
                oparr = self.try_bin_op()
                print(oparr)
                if type(oparr) != list:
                    return oparr
                return oparr[0]
            else:
                self.reverse()
                var_access_node = VarAccessNode(self.current_token.value)
                self.advance()
                return var_access_node
        
        if self.current_token.type == T_INTEGER:
            intnode = IntegerNode(self.current_token.value)
            self.advance()
            return intnode
        self.advance()
        
        return self.atom()

    def create_if_inside(self):
        ifcase = []
        elif_cases = []
        else_case = []
        while self.current_token.type == T_NEWLINE:
            while self.current_token.type == T_KEYWORD and self.current_token.value != "then":
                if self.current_token.type == T_KEYWORD and self.current_token.value in ["true","false"]:
                        pass
                elif self.current_token.type in [T_INTEGER,T_STRING]:
                    pass
                pass




    def this_children(self):
        children = []
        is_dot = False
        while True:
            if self.current_token.type not in [T_DOT,T_LSQUARE]:
                break

            if self.current_token.type == T_DOT:
                is_dot = True
            else:
                is_dot = False
            self.advance()
            
            if is_dot and self.current_token.type != T_IDENTIFIER:
                raise Exception("Expected identifier at {}".format(self.current_token.pos_start))
            if not is_dot and self.current_token.type != T_INTEGER:
                raise Exception("Expected an integer at {}".format(self.current_token.pos_start))
            children.append(ChildAccessNode(self.current_token.value))
            
            

            self.advance()
            if not is_dot:
                if self.current_token.type != T_RSQUARE:
                    raise Exception("Expected ']' at {}".format(self.current_token.pos_start))
                self.advance(1)

        return children
    
    def add_bin_op(self,left,op,right):
        return BinOpNode(left,op,self.try_bin_op())

    def try_bin_op(self):
        tokens_til_end = []
        while True:
            if self.current_token.type not in [T_INTEGER,T_STRING,T_PLUS,T_MINUS,T_MUL,T_DIV,T_IDENTIFIER]:
                break
            tokens_til_end.append(self.current_token)
            self.advance()
        op_counter = 0
        
        for index,token in enumerate(tokens_til_end):
            if token.type in [T_MUL,T_DIV]:
                binop = BinOpNode(self.bin(tokens_til_end[index-1]),token,self.bin(tokens_til_end[index+1]))
                tokens_til_end.pop(index-1)
                tokens_til_end.pop(index-1)
                tokens_til_end.pop(index-1)
                op_counter += 1
                tokens_til_end.insert(index-1,binop)
        
        if op_counter == 0:
            self.reverse()
            binned = self.bin(self.current_token)
            self.advance()
            return binned

        while len(tokens_til_end) != 1:
            for index,token in enumerate(tokens_til_end):
                if type(token) != BinOpNode:
                    if token.type in [T_PLUS,T_MINUS]:
                        binop = BinOpNode(self.bin(tokens_til_end[index-1]),token,self.bin(tokens_til_end[index+1]))
                        tokens_til_end.pop(index-1)
                        tokens_til_end.pop(index-1)
                        tokens_til_end.pop(index-1)
                        tokens_til_end.insert(index-1,binop)
                        
        return tokens_til_end


    def bin(self,tok):
        if type(tok) != Token:
            return tok
        if tok.type == T_INTEGER:
            return IntegerNode(tok.value)
        elif tok.type == T_STRING:
            return StringNode(tok.value)
        elif tok.type == T_IDENTIFIER:
            return VarAccessNode(tok.value)
            

    def fexpr(self):
        
        if self.current_token.type == T_COMMA:
            pass            
        if self.current_token.type == T_MINUS:
            self.try_unary()
            return UnaryOpNode(self.current_token,self.fexpr())
        elif self.current_token.type == T_STRING:
            node = self.try_bin_op()
            return node
        elif self.current_token.type == T_INTEGER:
            node = self.try_bin_op()
            return node
        elif self.current_token.type == T_KEYWORD and self.current_token.value == "this":
            return self.atom()
        elif self.current_token.type == T_KEYWORD and self.current_token.value == "true":
            return BinaryNode(True)
        elif self.current_token.type == T_KEYWORD and self.current_token.value == "false":
            return BinaryNode(False)
        elif self.current_token.type == T_KEYWORD and self.current_token.value == "null":
            return NoneNode()
        elif self.current_token.type == T_LBRACKET:
            return self.create_object_node()
        elif self.current_token.type == T_LSQUARE:
            return self.create_array_node()
        elif self.current_token.type == T_LPAREN:
            self.advance()
            node = self.fexpr()
            self.advance()
            return node
        elif self.current_token.type == T_RPAREN:
            return None
        else:
            raise Exception("Unknown Character")
 
    def expr(self):
        self.current_token
        if self.current_token.type == T_COMMA:
            pass
        elif self.current_token.type == T_ARROW:
            return self.func()
        elif self.current_token.type == T_COLON:
            self.reverse()
            name = StringNode(self.current_token.value)
            self.advance(2)
            value = self.expr()
            return NameValuePairNode(name,value)
        elif self.current_token.type == T_STRING:
            return StringNode(self.current_token.value)
        elif self.current_token.type == T_INTEGER:
            return IntegerNode(self.current_token.value)
        elif self.current_token.type == T_KEYWORD and self.current_token.value == "true":
            return BinaryNode(True)
        elif self.current_token.type == T_KEYWORD and self.current_token.value == "false":
            return BinaryNode(False)
        elif self.current_token.type == T_KEYWORD and self.current_token.value == "null":
            return NoneNode()
        elif self.current_token.type == T_LBRACKET:
            return self.create_object_node()
        elif self.current_token.type == T_LSQUARE:
            return self.create_array_node()





globalVariableTable = []

[
    
]

class Interpreter():
    def __init__(self,node):
        self.node = node

    def execute(self):
        return self.interp(self.node)
    
    def f_interp(self,node,this=None):
        print("node",node)
        return_str = ""

        if type(node) == FuncDefNode:

            for body_element in node.body_node:

                return_str += str(self.f_interp(body_element,this))
            
        if type(node) == VarAssignNode:

            if type(node.value_node) == list:

                globalVariableTable.append([node.var_name_tok,self.f_interp(node.value_node[0],this)])

            else:

                globalVariableTable.append([node.var_name_tok,self.f_interp(node.value_node,this)])
            print("a",node,self.f_interp(node.value_node,this))
            return ""
        
        if type(node) == BinOpNode:

            left = self.f_interp(node.left_node,this)
            right = self.f_interp(node.right_node,this)
            print(left,right)

            if node.op_tok.type == T_PLUS:
                if type(left) == str or type(right) == str:
                    print("one of them is string")
                    try:
                        left = int(left)
                        right = int(right)
                        return left + right
                    except Exception:
                        print("except")
                        left = str(left)
                        print(node.left_node)
                        if type(node.left_node) == ThisNode:
                            left = left[1:-1]
                        if type(node.right_node) == ThisNode:
                            left = left[1:-1]
                        right = str(right)
                        print(left,right)
                        return '\"' + str(left + right) + '\"'
                else:
                    return left + right
            
            elif node.op_tok.type == T_MINUS:
                if type(left) == str or type(right == str):
                    raise Exception("Can't subtract str")
                else:
                    return left - right
            
            elif node.op_tok.type == T_DIV:
                if right == 0:
                    raise Exception("Division by 0 not allowed")
                if type(left) == str or type(right == str):
                    raise Exception("Can't div str")
                else:
                    return left / right
            
            elif node.op_tok.type == T_MUL:
                if type(left) == str or type(right == str):
                    try:
                        left = int(left)
                        right = int(right)
                        return left * right
                    except Exception:
                        raise Exception("Can't multiply str")
                else:
                    return left * right
            
            else:
                raise Exception("Operation Failure")
       
        if type(node) == IntegerNode:
            return node.integer

        if type(node) == StringNode:
            return str(node.string)

        if type(node) == ReturnNode:
            returning = self.f_interp(node.node_to_return,this)
            return returning
        
        if type(node) == NoneNode:
            return "null"
        
        if type(node) == ThisNode:
            thisObj = json.loads(str(this[:-1])+'}')

            for child in node.after_identifier:
                thisObj = thisObj[child.access_node]
            print(type(thisObj))
            if type(thisObj) == str:
                print("this is str")
                return '"'+thisObj+'"'
            elif type(thisObj) == int:
                return thisObj
            print(thisObj)
            return json.dumps(thisObj)
        
        if type(node) == VarAccessNode:
            for var_tuple in globalVariableTable:
                if var_tuple[0] == node.var_name_tok:
                    return var_tuple[1]
            raise Exception("Variable not assigned")

        if type(node) == BinaryNode:
            if node.value == True:
                return "true"
            elif node.value == False:
                return "false"
        
        return return_str

    def interp(self,node,current_str=None):
        str = ""
        
        if type(node) == ObjectNode:
            str += "{"
            for nvp_node in node.name_value_pair_nodes:
                str += self.interp(nvp_node,str)
            str = str[:-1]
            str += "}"
        elif type(node) == ArrayNode:
            str += "["
            for index, object_node in enumerate(node.object_nodes):
                str += self.interp(object_node)
                if index+1 != len(node.object_nodes):
                    str+=","
            # str = str[:-1]
            str += "]"
        elif type(node) == NameValuePairNode:
            str += '{}:{},'.format(self.interp(node.name),self.interp(node.value_token,current_str))
        elif type(node) == StringNode:
            str += '\"{}\"'.format(node.string)
        elif type(node) == IntegerNode:
            str += "{}".format(node.integer)
        elif type(node) == BinaryNode:
            if node.value == True:
                str += "true"
            else:
                str += "false"
        elif type(node) == NoneNode:
            str += "null"
        elif type(node) == FuncDefNode:
            globalVariableTable.clear()
            str += "{}".format(self.f_interp(node,current_str))
            
        return str
    

def execute(file_path):
    with open(file_path,"r") as jsonx_file:
        my_str = jsonx_file.read()
        lexer = Lexer("",my_str)
        tokens,error = lexer.make_tokens()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter(ast)
        jsontxt = interpreter.execute()

        # print("EXECUTE: ",jsontxt)
        # jsonObj = json.loads(jsontxt)

        json_file_path = get_json_file_name(file_path)

        with open(json_file_path, "w+") as json_file:
            json_file.write(jsontxt)

def get_json_file_name(file_path):
    file_name = file_path[:file_path.rfind(".")]
    return file_name + ".json"
