from models import connect
from argon2 import PasswordHasher
from flask import session, redirect, jsonify
conn = connect.connection()
cursor = conn.cursor()
ph = PasswordHasher()
def local_login(data):
    email = data['email']
    passwd = data['password']
    checkLoginquery = f"""SELECT * FROM "User_Schema".Account WHERE email = '{email}' AND type_account = 0"""
    cursor.execute(checkLoginquery)
    conn.commit()
    result = cursor.fetchone()
    if result is None:
        return jsonify({"message":"Your email doesn't have an account!!!",
                        "statusCode":"500"}) ,500
    else:
        try:
          ph.verify(result[3],passwd)
          session['user'] = ({
            "id": result[0],
            "email": result[1]
          })
          return jsonify({"message": "Login Successful!!!",
                          "user": session['user'],
                          "statusCode":"200"}), 200
        except Exception:
          return jsonify({"message": "Your email or password is incorrect :( Try again!",
                          "statusCode":"401"}), 401
        
def local_register(data):
  count_account_query = f"""SELECT COUNT(*) FROM "User_Schema".Account WHERE type_account = 0"""
  cursor.execute(count_account_query)
  conn.commit()
  account_id = cursor.fetchone()[0]
  email = data['email']
  pw = data['password']
  passwd = ph.hash(pw)
  checkEmail_query = f"""SELECT COUNT(*) FROM "User_Schema".Account WHERE email = '{email}' AND type_account = 0"""
  cursor.execute(checkEmail_query)
  conn.commit()
  result = cursor.fetchone()
  if(result[0] == 0):
    register_query = f"""INSERT INTO "User_Schema".Account (account_id, email, password, type_account) VALUES ('{account_id}','{email}', '{passwd}', 0) """
    cursor.execute(register_query)
    conn.commit()
    return jsonify({"message":"Congratulation! Register Successful :)",
                    "statusCode":"200"}), 200
  else:
    return jsonify({"message":"Your email already exists",
                    "statusCode":"500"}), 500
  
  
            
    
    
