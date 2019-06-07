#! /usr/bin/env python
#coding=utf8
class table:
    def __init__(self,ls,name):
        self.name = name
        self.ls = []
        self.col2num = {}
        self.log_cnt = 0;self.col_cnt = 0
        if ls!=[]:
            for each in ls:
                self.ls.append(each)
            for i in range(len(ls[0])):
                pass
                self.col2num.update({ls[0][i][0]:i})
            self.log_cnt += len(ls)-1
            self.col_cnt += len(ls[0])
        else:
            print 'initial failed!'
        
    def set_col(self,col):
        if len(self.ls)!=0:
            self.ls[0] = col
        else:
            self.ls[0].append(col)
    def clear_logs(self):
        self.ls = [self.ls[0]]
    
    def check_req2col_name(self,req):
        # print 'req',req
        req_name = [i[0] for i in req]
        #print self.ls[0]
        col_name = [i[0] for  i in self.ls[0]]
        # print req_name
        # print col_name
        for i in req_name:
            if i not in col_name:
                return False
        return True
    
    def display(self):
        print '-----'*2
        print self.name
        for each in self.ls:
            print each
        print '_____'*2
        return True

    def add_logs(self,logs):
        #[['"primelee"', 20]]
        # Handle exception?
        sig = [True,[]]

        for i in range(len(logs)):
            for j in range(len(logs[i])):
                ty = self.ls[0][j][1]
                if ty =='string':
                    logs[i][j] = logs[i][j][1:len(logs[i][j])-1]

        self.log_cnt += len(logs)
        for each in logs:
            self.ls.append(each)
        return sig

    def find_right_logs(self,req):
        req2 = [[self.col2num[i[0]],i[2]] for i in req]
        for i in range(len(req2)):
            ty = self.ls[0][req2[i][0]][1]
            if ty == 'string':
                req2[i][1] = req2[i][1][1:len(req2[i][1])-1]
        #print 'req2',req2
        pos = []
        ls = self.ls
        log_sz = self.log_cnt
        for i in range(1,1+log_sz):
            ok = True
            for j in req2:
                if ls[i][j[0]] != j[1]:
                    ok = False
            if ok:
                pos.append(i)
        return pos

    def delete_logs(self,req):
        #[['name', '=', '"primelee"'],['age', '=', 20]]
        sig = [True,[]]
        
        if not self.check_req2col_name(req):
            sig = [False,'Request\'s column names error']
            return sig

        pos =self.find_right_logs(req)
        self.log_cnt -= len(pos)

        new_ls = []
        for i in range(1,1+self.log_cnt):
            if i not in pos:
                new_ls.append(self.ls[i])
        self.clear_logs()
        for i in new_ls:
            self.ls.append(i)
        return sig

    def search_logs(self,req):
        sig = [True,[]]
        if not self.check_req2col_name(req):
            sig = [False,'Request\'s column names error']
            return sig

        pos =self.find_right_logs(req)

        for i in pos:
            print self.ls[i]
        return sig

class sheet:
    def __init__(self,name):
        self.name = name
        self.tables = []

    def create_table(self,ls,tb_name):
        tb = table(ls,tb_name)
        self.tables.append(tb)
        return True
    def print_table(self,name):
        sig = [True,[]]
        ok = False
        for i in self.tables:
            if i.name == name:
                i.display()
                ok = True
        if not ok:
            sig = [False,'No such a table']
        return sig

    def grep_table(self,name):
        ok = -1
        for i in range(len(self.tables)):
            if self.tables[i].name == name:
                ok = i
        return  ok

    def add_logs(self,tb_name,logs):
        sig = [True,[]]
        pos = self.grep_table(tb_name)
        if pos == -1:
            sig = [False,'No such a table']
            return sig
        sub_sig = self.tables[pos].add_logs(logs)
        if not sub_sig[0]:
            sig[0] = sub_sig[0];sig[1] = sub_sig[1]
        return sig

    def delete_logs(self,tb_name,logs):
        sig = [True,[]]
        pos = self.grep_table(tb_name)
        if pos == -1:
            sig = [False,'No such a table']
            return sig
        sub_sig = self.tables[pos].delete_logs(logs)
        if not sub_sig[0]:
            sig[0] = sub_sig[0];sig[1] = sub_sig[1]
        return sig

    def search_logs(self,tb_name,logs):
        sig = [True,[]]
        pos = self.grep_table(tb_name)
        if pos == -1:
            sig = [False,'No such a table']
            return sig
        sub_sig = self.tables[pos].search_logs(logs)
        if not sub_sig[0]:
            sig[0] = sub_sig[0];sig[1] = sub_sig[1]
        return sig
    
            
            
    

def test():

    sh = sheet('prime_db')
    sh.create_table([[['ID', 'string'], ['Age', 'int']]],'CNSS')
    sh.add_logs('CNSS',[['"primelee"', 20]])
    sh.search_logs('CNSS',[['ID', '=', '"primelee"']])
    sh.delete_logs('CNSS',[['ID', '=', '"primelee"']])
    sh.search_logs('CNSS',[['ID', '=', '"primelee"']])
    print 'debug'
    sh.print_table('CNSS')
    

    

if __name__ == '__main__':
    test()