#! /usr/bin/env python
#coding=utf8

from compiler import lexer2,ast
from fileio import fileio as io

#sample code;
#create table classmates{name string, age int};
#display classmates;
#insert into classmates values("primelee",20);
#insert into classmates values("yype",20);
#insert into classmates values("bella",20);
#delete from classmates where(name = "yype");
#select from classmates where(name = "primelee")


def read_commands():
    command = ''
    sub_command = raw_input('>> ')
    while True:
        if sub_command == '':
            break
        if sub_command.split()[-1:][0][-1:]!=';':
            command += sub_command
            sub_command = raw_input('.. ')
        else:
            command += sub_command
            break
    return command

def get_payload(com):
    tok_s = lexer2.start(com)
    ast.token_stream = tok_s
    res = ast.start()
    return res

def option(sh,req):
    def print_msg(err_msg,ok_msg,ok):
        if not ok:
            print err_msg
        else:
            print ok_msg


    if req[0] == 'ERROR':
        print req[1]
        return True
    tb_name = req[1][0]
    #pay = req[1][1]
    opt = req[0]
    #print opt,tb_name#pay
    if opt=='display table':
        #handle no such a table?
        sig = sh.print_table(tb_name)
        if not sig[0]:
            print sig[1]
        
    else:
        payload = req[1][1]
        #print 'payload',payload
        if opt == 'create table':
            sh.create_table([payload],tb_name)
            print 'Create table sussfully!'
            
        elif opt == 'add log':
            sig = sh.add_logs(tb_name,[payload])
            if not sig[0]:print sig[1]
            else:
                print 'Add log sussfully!'
            
        elif opt == 'search log':
            sig = sh.search_logs(tb_name,payload)
            if not sig[0]:print sig[1]
            else:
                print 'Search log sussfully!'
            
        elif opt == 'delete log':
            sig = sh.delete_logs(tb_name,payload)
            if not sig[0]:print sig[1]
            else:
                print 'Delete log sussfully!'
    



def main():
    sh = io.sheet('prime')
    while True:
        com = read_commands()
        if com == 'quit();':
            break
        elif com == 'export tables;':
            fname = raw_input('.. file name to export >> ')
            print repr(fname)
            sh.export_tables(fname)
            continue
        elif com == 'import tables;':
            fname = raw_input('.. file name to import from >> ')
            sh.import_tables(fname)
            continue

        payload = get_payload(com)
        #print 'payload ',payload
        for each in payload:
           
            option(sh,each)
        #print sh.tables[0].name

if __name__ == '__main__':
    main()

#create table cnss {id string, age int ,direction string}; 
#display cnss;
# insert into cnss values('yype',20,'bin');
# insert into cnss values('primelee',20,'bin');
#select from cnss where(age = 20); 
        
    