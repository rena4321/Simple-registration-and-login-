import pymysql

def register():
    print("User registration")

    user = input("Please enter user name: ")
    password = input("Please enter password: ")

    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root',password='kyee', db="usersdb")
    cursor = conn.cursor()

    sql = 'insert into users(name, password) values("{}", "{}")'.format(user, password)

    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close

    print("Registration success, username: {}, password: {}".format(user, password))

def login():
    print("User login")

    user = input("Please enter user name: ")
    password = input("Please enter password: ")

    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root',password='kyee', db="usersdb")
    cursor =conn.cursor()

    sql = "select * from users where name='{}' and password='{}'".format(user, password)
    cursor.execute(sql)
    result = cursor.fetchone()

    cursor.close()
    conn.close

    if result:
        print("Registration success", result)
    else:
        print("Registration failed")

def run():
    choice = input("1.Registration; 2.Login")
    if choice == '1':
        register()
    elif choice == '2':
        login()
    else:
        print("Input error")


if __name__ == '__main__':
    run()