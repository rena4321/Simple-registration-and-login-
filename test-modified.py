import pymysql
import hashlib
import getpass  # 用于安全输入密码

def hash_password(password):
    """使用SHA-256加密密码"""
    return hashlib.sha256(password.encode()).hexdigest()

def get_db_connection():
    """获取数据库连接"""
    try:
        conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='root',
            db='usersdb',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except pymysql.Error as e:
        print(f"数据库连接失败: {e}")
        return None

def register():
    print("用户注册")
    
    user = input("请输入用户名: ").strip()
    if not user:
        print("用户名不能为空")
        return
    
    # 使用getpass隐藏密码输入
    password = getpass.getpass("请输入密码: ")
    if not password:
        print("密码不能为空")
        return
    
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        with conn.cursor() as cursor:
            # 1. 检查用户名是否已存在
            check_sql = "SELECT id FROM users WHERE name = %s"
            cursor.execute(check_sql, (user,))
            if cursor.fetchone():
                print("用户名已存在")
                return
            
            # 2. 插入新用户（使用参数化查询防止SQL注入）
            hashed_password = hash_password(password)
            insert_sql = "INSERT INTO users (name, password) VALUES (%s, %s)"
            cursor.execute(insert_sql, (user, hashed_password))
            conn.commit()
            
            print(f"注册成功，用户名: {user}")
            
    except pymysql.Error as e:
        print(f"注册失败: {e}")
        conn.rollback()
    finally:
        conn.close()

def login():
    print("用户登录")
    
    user = input("请输入用户名: ").strip()
    password = getpass.getpass("请输入密码: ")
    
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        with conn.cursor() as cursor:
            # 使用参数化查询防止SQL注入
            sql = "SELECT * FROM users WHERE name = %s AND password = %s"
            hashed_password = hash_password(password)
            cursor.execute(sql, (user, hashed_password))
            result = cursor.fetchone()
            
            if result:
                print(f"登录成功！欢迎 {result['name']}")
            else:
                print("登录失败，用户名或密码错误")
                
    except pymysql.Error as e:
        print(f"登录失败: {e}")
    finally:
        conn.close()

def run():
    while True:
        print("\n" + "="*30)
        print("1. 注册")
        print("2. 登录")
        print("3. 退出")
        print("="*30)
        
        choice = input("请选择操作 (1-3): ").strip()
        
        if choice == '1':
            register()
        elif choice == '2':
            login()
        elif choice == '3':
            print("再见！")
            break
        else:
            print("输入错误，请重新选择")

if __name__ == '__main__':
    run()
