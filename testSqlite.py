import sqlite3

conn = sqlite3.connect("test.db")
print("打开数据库成功")

c = conn.cursor()
# #建表
# sql = '''
#     create table company
#         (id int primary key not null,
#         name text not null,
#         age int not null,
#         address char(50),
#         salary real);
#
# '''

# sql = '''
#     insert into company(id,name,age,address,salary)
#     values (1,"张三",20,"北京",20000)
# '''

sql = '''
    select id,name,age,address,salary from company
'''

cursor = c.execute(sql)

for row in cursor:
    print("id = ",row[0])
    print("name = ",row[1])
    print("age = ",row[2])
    print("address = ",row[3])
    print("salary = ",row[4])

conn.commit()
conn.close()

print("成功建表")