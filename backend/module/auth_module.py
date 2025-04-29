from flask import redirect, session
from models import connect

conn = connect.connection()
cursor = conn.cursor()
def checkSNLogin(data, type):
    id = data['id']
    email = data['email']
    checkLoginquery = f"""SELECT COUNT(*) FROM "User_Schema".Account WHERE email = '{email}' AND type_account = '{type}'"""
    cursor.execute(checkLoginquery)
    conn.commit()
    result = cursor.fetchone()
    
    if(result[0] > 0):
        session['user'] = ({
            "id": id,
            "email": email
        })
        return redirect("http://localhost:5173/home")
    else:
        return registerSN(data, type)

def registerSN(data, type):
    id = data['id']
    email = data['email']
    username = data['name']
    Registerquery = f"""INSERT INTO "User_Schema".Account (account_id, email, name, type_account) VALUES ('{id}', '{email}', '{username}', '{type}')"""
    try:
        cursor.execute(Registerquery)
        conn.commit()
        session['user'] = ({
            "id": id,
            "email": email
        })
        return redirect("http://localhost:5173/home")
    except Exception as e:
        conn.rollback()
        print(str(e))
        return "Lỗi khi đăng ký tài khoản", 500  
    