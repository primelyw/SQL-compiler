#! /usr/bin/env python
#coding=utf8


# S -> CREATE_TABLE | ADD_LOG | SEARCH_LOG | DELETE_LOG| UPDATE_LOG


display_stream = [['DISPLAY','-'],['ID', 'CNSS'],['END','-']]
add_stream = [['INSERT','-'],['INTO','-'],['ID','CNSS'],['VALUES','-'],['SLP','-'],['STR','primelee'],['COM','-'],['STR','pwn'],['SRP','-'],['END','-']]
create_stream = [['CREATE','-'],['TABLE','-'],['ID','CNSS'],['LP','-'],['ID','ID'],['STRING','-'],['COM','-'],['ID','DIR'],['STRING','-'],['RP','-'],['END','-']]
delte_stream = [['DELETE','-'],['FROM','-'],['ID','CNSS'],['WHERE','-'],['SLP','-'],['ID','ID'],['EQ','-'],['STR','primelee'],['COM','-'],['ID','DIR'],['EQ','-'],['STR','pwn'],['SRP','-'],['END','-']]
search_stream = [['SELECT','-'],['FROM','-'],['ID','CNSS'],['WHERE','-'],['SLP','-'],['ID','ID'],['EQ','-'],['STR','primelee'],['COM','-'],['ID','DIR'],['EQ','-'],['STR','pwn'],['SRP','-'],['END','-']]
token_stream =search_stream+display_stream+create_stream

err_dict = {
    'END':'semicomma',
    'CREATE':'keywords \'create\'',
    'TABLE':'keywords \'table\'',
    'SLP':"symbol '('",
    'SRP':"symbol ')'",
    'LP':"symbol '{'",
    "RP":"symbol '}'",
    'COM':"symbol ','",
    'INSERT':"keywords 'insert'",
    'INTO':"keywords 'into'",
    'VALUES':"keywords 'values'",
    'DELETE':"keyword 'delete",
    'FROM':"keyword 'from'",
    'WHERE':"keyword 'where",
    'EQ':'symbol ='
}


def get_next_tok(cur):
    if cur >= len(token_stream)-1:
        return ['None','-'],cur+1
    else:
        return token_stream[cur+1],cur+1


def handle_error(sig,msg,cur):
    sig[0] = False
    sig[2] = msg
    s = token_stream[cur:]
    pos = 0
    while True:
        if pos >= len(s) or s[pos]==['END','-']: break
        pos += 1
    cur += pos
    sig[3] = cur
    return sig



def check_son(opt,sig,sub_sig):
    #opt: 0->no param pass; 1-> pass param
    sig[3] = sub_sig[3]
    if sub_sig[0]==False:
        #sig = sub_sig 迷
        sig[2] = sub_sig[2]
        sig[0] = sub_sig[0]
        return False
        # if opt==True:
        #     sig[1].append(sub_sig[1])
    else:
        return True
        

def get_NON_type(ty,cur):
    sig = [True,[],'No error',-1]
    tok,cur = get_next_tok(cur)

    if tok[0] == ty:
        sig[3] = cur
        return sig
    else:
        return handle_error(sig,'Expected a ' +err_dict[ty],cur)

def get_identifier(cur):
    sig = [True,[],'No error',-1]
    tok,cur = get_next_tok(cur)
    
    if tok[0]=='ID':
        sig[1].append(tok[1])
        sig[3] = cur
    else:
        return handle_error(sig,'Expected an identifier',cur)
    return sig






def display_table(cur):
    sig = [True,[],'No error',-1]
    sub_sig = [True,[],'No error',-1]

    sub_sig = get_identifier(cur)
    if check_son(True,sig,sub_sig)==False:return sig
    for i in sub_sig[1]:
        sig[1].append(i)

    #print sig
    cur = sig[3]
    sub_sig = get_NON_type('END',cur)
    if check_son(False,sig,sub_sig)==False: return sig
    cur = sig[3]
    return sig

def get_data_type(cur):
    pass
    sig = [True,[],'No error',-1]
    tok,cur = get_next_tok(cur)

    if tok[0] == 'INT' or tok[0] == 'STRING':
        if tok[0] == 'INT':
            sig[1].append('int')
        elif tok[0] == 'STRING':
            sig[1].append('string')
        sig[3] = cur
        return sig
    else:
        return handle_error(sig,'Expected a data type (int or string)',cur)


def get_col_unit(cur):
    sig = [True,[],'No error',-1]
    sub_sig =  [True,[],'No error',-1]

    sub_sig = get_identifier(cur)
    if check_son(True,sig,sub_sig)==False:return sig
    for i in sub_sig[1]:
        sig[1].append(i)

    cur = sig[3]
    sub_sig = get_data_type(cur)
    if check_son(True,sig,sub_sig)==False:return sig
    for i in sub_sig[1]:
        sig[1].append(i)
    cur = sig[3]
    return sig


def get_col_list(cur):
    pass
    sig = [True,[],'No error',-1]
    sub_sig =  [True,[],'No error',-1]

    sub_sig = get_col_unit(cur)
    if check_son(True,sig,sub_sig)==False:return sig
    sig[1].append(sub_sig[1])
    cur = sig[3]

    tok,cur = get_next_tok(cur)
    if tok[0] != 'COM':
        sig[3] = cur-1
        return sig
    else:
        sub_sig = get_col_list(cur)
        if check_son(True,sig,sub_sig)==False:return sig
        for i in sub_sig[1]:
            sig[1].append(i)
        return sig

    


def create_table(cur):
    sig = [True,[],'No error',-1]
    sub_sig = [True,[],'No error',-1]

    sub_sig = get_NON_type('TABLE',cur)
    if check_son(False,sig,sub_sig)==False:return sig
    cur = sig[3]

    sub_sig = get_identifier(cur)
    if check_son(False,sig,sub_sig)==False:return sig
    for i in sub_sig[1]:
        sig[1].append(i)

    cur = sig[3]
    sub_sig = get_NON_type('LP',cur)
    if check_son(False,sig,sub_sig)==False:return sig
    
    cur = sig[3]
    sub_sig = get_col_list(cur)
    if check_son(False,sig,sub_sig)==False:return sig
    sig[1].append(sub_sig[1])


    cur = sig[3]
    sub_sig = get_NON_type('RP',cur)
    if check_son(False,sig,sub_sig)==False:return sig
    cur = sig[3]

    sub_sig = get_NON_type('END',cur)
    if check_son(False,sig,sub_sig)==False: return sig
    return sig

def get_value_unit(cur):
    sig = [True,[],'No error',-1]
    tok,cur = get_next_tok(cur)

    if tok[0] == 'NUM' or tok[0] == 'STR':
        if tok[0] =='NUM':
            sig[1].append(int(tok[1]))
        elif tok[0] == 'STR':
            sig[1].append(tok[1])
        sig[3] = cur
        return sig
    else:
        return handle_error(sig,'Expected a data type const value (int or string)',cur)

def get_value_list(cur):
    sig = [True,[],'No error',-1]
    sub_sig =  [True,[],'No error',-1]

    sub_sig = get_value_unit(cur)
    if check_son(True,sig,sub_sig)==False:return sig
    for i in sub_sig[1]:
        sig[1].append(i)
    cur = sig[3]

    tok,cur = get_next_tok(cur)
    if tok[0] != 'COM':
        sig[3] = cur-1
        return sig
    else:
        sub_sig = get_value_list(cur)
        if check_son(True,sig,sub_sig)==False:return sig
        for i in sub_sig[1]:
            sig[1].append(i)
        return sig

def add_log(cur):
    sig = [True,[],'No error',-1]
    sub_sig = [True,[],'No error',-1]

    sub_sig = get_NON_type('INTO',cur)
    if check_son(False,sig,sub_sig)==False:return sig
    cur = sig[3]

    sub_sig = get_identifier(cur)
    if check_son(False,sig,sub_sig)==False:return sig
    for i in sub_sig[1]:
        sig[1].append(i)
    cur = sig[3]

    sub_sig = get_NON_type('VALUES',cur)
    if check_son(False,sig,sub_sig)==False:return sig
    cur = sig[3]

    sub_sig = get_NON_type('SLP',cur)
    if check_son(False,sig,sub_sig)==False:return sig
    cur = sig[3]

    sub_sig = get_value_list(cur)
    if check_son(False,sig,sub_sig)==False:return sig
    sig[1].append(sub_sig[1])


    cur = sig[3]
    sub_sig = get_NON_type('SRP',cur)
    if check_son(False,sig,sub_sig)==False:return sig
    cur = sig[3]

    sub_sig = get_NON_type('END',cur)
    if check_son(False,sig,sub_sig)==False: return sig
    return sig


def get_find_unit(cur):
    sig = [True,[],'No error',-1]
    sub_sig = [True,[],'No error',-1]

    sub_sig = get_identifier(cur)
    if check_son(False,sig,sub_sig)==False:return sig
    for i in sub_sig[1]:
        sig[1].append(i)
    cur = sig[3]

    sub_sig = get_NON_type('EQ',cur)
    if check_son(False,sig,sub_sig)==False:return sig
    sig[1].append('=')
    cur = sig[3]

    sub_sig = get_value_unit(cur)
    if check_son(False,sig,sub_sig)==False:return sig
    for i in sub_sig[1]:
        sig[1].append(i)
    cur = sig[3]
    return sig
    

def get_find_list(cur):
    pass
    sig = [True,[],'No error',-1]
    sub_sig =  [True,[],'No error',-1]

    sub_sig = get_find_unit(cur)
    #print type(sub_sig)
    if check_son(True,sig,sub_sig)==False:return sig
    sig[1].append(sub_sig[1])
    cur = sig[3]

    tok,cur = get_next_tok(cur)
    if tok[0] != 'COM':
        sig[3] = cur-1
        return sig
    else:
        sub_sig = get_find_list(cur)
        if check_son(True,sig,sub_sig)==False:return sig
        for i in sub_sig[1]:
            sig[1].append(i)
        return sig
    
    

def delete_log(cur):
    #DELETE FROM table_name WHERE [condition];
    sig = [True,[],'No error',-1]
    sub_sig = [True,[],'No error',-1]

    sub_sig = get_NON_type('FROM',cur)
    if check_son(False,sig,sub_sig)==False:return sig
    cur = sig[3]

    sub_sig = get_identifier(cur)
    if check_son(False,sig,sub_sig)==False:return sig
    for i in sub_sig[1]:
        sig[1].append(i)
    cur = sig[3]

    sub_sig = get_NON_type('WHERE',cur)
    if check_son(False,sig,sub_sig)==False:return sig
    cur = sig[3]

    sub_sig = get_NON_type('SLP',cur)
    if check_son(False,sig,sub_sig)==False:return sig
    cur = sig[3]

    sub_sig = get_find_list(cur)
    
    if check_son(False,sig,sub_sig)==False:return sig
    sig[1].append(sub_sig[1])


    cur = sig[3]
    sub_sig = get_NON_type('SRP',cur)
    if check_son(False,sig,sub_sig)==False:return sig
    cur = sig[3]

    sub_sig = get_NON_type('END',cur)
    if check_son(False,sig,sub_sig)==False: return sig

    return sig

def search_log(cur):
    #SELECT FROM COMPANY WHERE ( AGE = 25, SALARY = 65000 );
    sig = [True,[],'No error',-1]
    sub_sig = [True,[],'No error',-1]

    sub_sig = get_NON_type('FROM',cur)
    if check_son(False,sig,sub_sig)==False:return sig
    cur = sig[3]

    sub_sig = get_identifier(cur)
    if check_son(False,sig,sub_sig)==False:return sig
    for i in sub_sig[1]:
        sig[1].append(i)
    cur = sig[3]

    sub_sig = get_NON_type('WHERE',cur)
    if check_son(False,sig,sub_sig)==False:return sig
    cur = sig[3]

    sub_sig = get_NON_type('SLP',cur)
    if check_son(False,sig,sub_sig)==False:return sig
    cur = sig[3]

    sub_sig = get_find_list(cur)
    
    if check_son(False,sig,sub_sig)==False:return sig
    sig[1].append(sub_sig[1])


    cur = sig[3]
    sub_sig = get_NON_type('SRP',cur)
    if check_son(False,sig,sub_sig)==False:return sig
    cur = sig[3]

    sub_sig = get_NON_type('END',cur)
    if check_son(False,sig,sub_sig)==False: return sig

    return sig



def start():
    command_ret = []
    cur = -1
    stream_len = len(token_stream)
    while True:
        #function returns sig(success,command,error_msg,next_cur)
        tok,cur = get_next_tok(cur)
        final_sig = ['NONE']
        if tok[0]=='None' :break
        tok = tok[0]
        sig = [True,[],'None error',-1]
        if tok=='CREATE':
            sig = create_table(cur)
            final_sig[0] = 'create table'

        elif tok=='DISPLAY':
            sig = display_table(cur)
            final_sig[0] = 'display table'
        elif tok=='INSERT':
            sig = add_log(cur)
            final_sig[0] = 'add log'
        elif tok == 'DELETE':
            sig = delete_log(cur)
            final_sig[0] = 'delete log'
        elif tok == 'SELECT':
            sig = search_log(cur)
            final_sig[0] = 'search log'

        elif tok == 'UPDATE':
            sig = update_log(cur)
            final_sig[0] = 'update log'

        elif tok == 'END':
            sig[3] = cur

        else:
            sig = handle_error(sig,'Invalid command',cur)
            
        cur = sig[3]
        #print sig
        if sig[0]==False:
            #print sig[2]
            final_sig[0] = 'ERROR'
            final_sig.append(sig[2])
        else:
            final_sig.append(sig[1])
            pass
            #print final_sig
        #print sig
        if final_sig[0] != 'NONE':
            command_ret.append(final_sig)
    return command_ret
    
    #print 'done'


if __name__ == '__main__':
    start()
