#! /usr/bin/env python
#coding=utf8

import re

code = r"""
create table CNSS1234 {ID string, DIR string,AGE int};
"""

# insert into CNSS values("yype","Bin",20);
# insert into CNSS values("primelee","Bin",20);
# insert into CNSS values("N0th3ty","WEB",20);
# display CNSS;
# delete from CNSS where (ID = "primelee",DIR = "pwn" );
# code = 'display CNSS;'

def start(code):
    words = []

    keywords = ["create","table","insert","into","display","select","where","update","from","set","values","and","all","int","string","delete"]
    KEYWORDS = []
    for i in range(len(keywords)):
        KEYWORDS.append(keywords[i].upper())

    token_list = [
        ('NUM',r'\d+'),
        ('ID',r'[A-Za-z]+[\w_]*'),
        ('SLP',r'\('),
        ('SRP',r'\)'),
        ('LP',r'{'),
        ('STR',r"""('.+?')|(".+?")"""),
        ('RP',r'}'),
        ('COM',r','),
        ('END',r';'),
        ('EQ',r'='),('GET',r'>='),('LET',r'<='),('LT','<'),('RT','>'),
    ]

    token_regx = re.compile('|'.join('(?P<%s>%s)' % pair for pair in token_list))
    match = token_regx.finditer(code)
    len_words = 0
    for each in match:
        kind = each.lastgroup
        value = each.group()
        words.append([kind,'-']);
        if kind=='NUM' or kind == 'STR':
            words[len_words][1] = value
        elif kind == 'ID':
            if value in keywords:
                words[len_words][0] = KEYWORDS[keywords.index(value)]
            else:
                words[len_words][1] = value
        len_words += 1

    return  words

if __name__ == '__main__':
    print start(code)
    