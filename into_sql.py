#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 14:05:42 2019

@author: Holmes

sqlite>.header on
sqlite>.mode column
"""

import sqlite3

def get_news():
    read_file=open('news.txt','r')
    news_data=read_file.readlines()
    
    news_title=[]
    for title in news_data:
        element=title.split(';')
#        print(element[0])
        news_title.append(element[0])
#    print(news_title)
    read_file.close()
    return news_data, news_title


def create_table(news_data, news_title):

    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    
#    c.execute(''' Drop table COMPANY;''')
    try:
        c.execute('''CREATE TABLE COMPANY(
               Title            varchar(255),
               Link             varchar(255),
               Publish_time      varchar(255),
               Comment          varchar(255),
               Read             varchar(255));
            ''')
        print("Create table successfully, insert new data")
        for line in news_data:
            element=line.split(';')
            c.execute('''Insert into COMPANY(Title, Link, Publish_time, Comment, Read)
                    Values(?, ?, ?, ?, ?)''', (element[0], element[1], element[2], element[3], element[4]))
        c.execute('''select * from COMPANY''')
        table=c.fetchall()
        # print(table)
                    
    except Exception as e:
        print ("Create table failed, table has already exist, try to update data")
        #return False
        for line in news_data:
            element=line.split(';')
            temp=element[0]
#            temp='测试'
            # print(temp)
            c.execute("select * from COMPANY where Title=?", (temp,))
            result = c.fetchone()
#            print(result)
            if result != None:
                # print('Title exist, updating...')
                c.execute('''update COMPANY set
                          Link=?, Publish_time=?, Comment=?, Read=?
                          where Title=?''', (element[1], element[2], element[3], element[4], element[0])
                          )
                
            else:
                # print('Title does not exist, inserting...')
                c.execute('''Insert into COMPANY(Title, Link, Publish_time, Comment, Read)
                    Values(?, ?, ?, ?, ?)''', (element[0], element[1], element[2], element[3], element[4]))
                conn.commit()
    print('Updating/Inserting Done')
        
#            except:
#               # Rollback in case there is any error
#               db.rollback()
                
    conn.commit()
    conn.close()

def main():
    print('Put data into SQL')
    Read_file=get_news()
#    print(Read_file[0])
    create_table(Read_file[0],Read_file[1])

main()