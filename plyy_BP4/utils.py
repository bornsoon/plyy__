import database as db

def extract_user(id):
    u_id = db.get_query('SELECT id FROM USER WHERE id = ?', (id,),mul=False)

    return u_id['id'] if u_id else None

def user_sign(email):
    try:
        return bool(db.get_query('SELECT 1 FROM USER WHERE email = ?', (email,), mul=False))
    except Exception as e:
        print(f"Error occurred: {e}")
        return False
    
def user_sign_aka(nickname):
    try:
        return bool(db.get_query('SELECT 1 FROM USER WHERE nickname = ?', (nickname,), mul=False))
    except Exception as e:
        print(f"Error occurred: {e}")
        return False
    
def user_signup(email,pw,nickname):
    try:
        # 새로운 사용자 추가
        db.insert_query("INSERT INTO USER (email,pw,nickname) VALUES(?,?,?)", (email,pw,nickname))
        return True
    except Exception as e:
        print(f"회원가입 처리 중 오류 발생: {e}")
        db.roll()
        return False
    

def current_pw(id, pw):
    # 비밀번호 조회
    user = db.get_query('SELECT id, pw FROM USER WHERE id = ?', (id,), mul=False)
    if user and user['pw'] == pw:
        return id
    return None

def change_pw(id,pw):
    query = 'UPDATE USER SET pw = ? WHERE id = ?'
    params = (pw, id)
    try:
        db.update_query(query, params)
        return True
    except Exception as e:
        print(f"Error updating password: {e}")
        return False
    
def change_nickname(id,nickname):
    query = 'UPDATE USER SET nickname = ? WHERE id = ?'
    params = (nickname, id)
    try:
        db.update_query(query, params)
        return True
    except Exception as e:
        print(f"Error updating password: {e}")
        return False