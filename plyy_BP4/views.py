# views.py
from flask import Blueprint, request, session, render_template, redirect, url_for, jsonify
from models import curator_info, curatorlike_status, curator_like, curator_unlike, plyy_like, plyy_unlike, plyylike_status, cu_plyy
from utils import extract_user, user_sign, user_signup, user_sign_aka, current_pw, change_pw, change_nickname
import database as db

logout = Blueprint('logout', __name__)
mypage = Blueprint('mypage', __name__)
mypage_edit = Blueprint('mypage_edit',__name__)
mypage_edit_currentpw = Blueprint('mypage_edit_currentpw',__name__)
mypage_edit_changepw = Blueprint('mypage_edit_changepw', __name__)
mypage_edit_nickname = Blueprint('mypage_edit_nickname',__name__)
login = Blueprint('login', __name__)
signup = Blueprint('signup',__name__)
signup_email = Blueprint('signup_email',__name__)
signup_nickname = Blueprint('signup_nickname',__name__)
signup_final = Blueprint('signup_final',__name__)
curator = Blueprint('curator', __name__)
api_curator = Blueprint('api_curator', __name__)
like_curator = Blueprint('like_curator', __name__)
unlike_curator = Blueprint('unlike_curator', __name__)
like_plyy = Blueprint('like_plyy', __name__)
unlike_plyy = Blueprint('unlike_plyy', __name__)


@login.route('/login', methods=['GET', 'POST'])
def login_view():
    if request.method == 'POST':
        Id = request.form['userid']
        Pw = request.form['userpw']
        user = db.get_query('SELECT id, email, pw, nickname FROM USER WHERE email = ? and pw = ?', (Id, Pw),mul=False)
        if user:
            session['id'] = user['id']
            session['nickname'] = user['nickname']
            return redirect(url_for('main.index'))
        else:
            session['id'] = None
            return render_template('login.html', login_failed=True)
        
    return render_template('login.html', login_failed=False)

@logout.route('/logout', methods=['POST'])
def logout_view():
    session.pop('id', None)
    session.pop('nickname',None)
    return redirect(url_for('main.index'))

@mypage.route('/mypage')
def mypage_view():
    print(session)
    return render_template('mypage.html')

@mypage_edit.route('/edit')
def edit_view():
    return render_template('test_mypage_edit.html')

@mypage_edit_currentpw.route('/api/pw', methods=['POST'])
def mypage_pw():
    data = request.get_json()
    pw = data.get('password')
    
    if not pw:
        return jsonify({'valid': False, 'message': '비밀번호를 입력해 주세요.'}), 400

    user_id = current_pw(session.get('id'), pw)
    
    if user_id:
        return jsonify({'valid': True})
    else:
        return jsonify({'valid': False, 'message': '비밀번호가 올바르지 않습니다.'}), 401

@mypage_edit_changepw.route('/api/change-password', methods=['POST'])
def change_password():
    data = request.get_json()
    new_password = data.get('newPassword')

    if not new_password:
        return jsonify({'success': False, 'message': 'New password is required.'}), 400

    # 현재 사용자의 ID가 세션에 저장되어 있는지 확인
    user_id = session.get('id')
    if not user_id:
        return jsonify({'success': False, 'message': 'User not authenticated.'}), 403

    # 비밀번호 변경
    success = change_pw(user_id, new_password)

    if success:
        return jsonify({'success': True, 'message': 'Password updated successfully.'})
    else:
        return jsonify({'success': False, 'message': 'Failed to update password.'}), 500

@mypage_edit_nickname.route('/api/change-nickname', methods=['POST'])
def edit_nickname():
    data = request.get_json()
    new_nickname = data.get('newNickname')

    if not new_nickname:
        return jsonify({'success': False, 'message': 'New Nickname is required.'}), 400

    # 현재 사용자의 ID가 세션에 저장되어 있는지 확인
    user_id = session.get('id')
    if not user_id:
        return jsonify({'success': False, 'message': 'User not authenticated.'}), 403

    # 비밀번호 변경
    success = change_nickname(user_id, new_nickname)

    if success:
        session['nickname'] = new_nickname
        return jsonify({'success': True, 'message': 'Nickname updated successfully.'})
    else:
        return jsonify({'success': False, 'message': 'Failed to update Nickname.'}), 5
    
@signup.route('/signup')
def signup_view():
    return render_template('signup.html')

@curator.route('/curator/<c_id>')
def curator_view(c_id):
    return render_template('cDetail.html')

@signup_email.route('/api/<email>',methods=['post'])
def signup_email_view(email):
    try:
        status = user_sign(email)
        return jsonify({'exists': status}), 200
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({'exists': False}), 500

@signup_nickname.route('/api/nickname/<nickname>',methods=['post'])
def signup_nickname_view(nickname):
    try:
        status = user_sign_aka(nickname)
        return jsonify({'exists': status}), 200
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({'exists': False}), 500

@signup_final.route('/api/signup',methods=['post'])
def signup_final_view():
    try:
        # 클라이언트로부터 이메일과 비밀번호를 JSON 형식으로 받음
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        nickname = data.get('nickname')
        # user_signup 함수 호출하여 데이터베이스에 사용자 추가
        result = user_signup(email, password, nickname)
        if result:
            user = db.get_query('SELECT id FROM USER WHERE email = ? and pw = ?', (email,password),mul=False)
            session['id'] = user['id']
            session['nickname'] = user['nickname']
            return jsonify({'success': True, 'message': '회원가입이 완료되었습니다!'}), 200
        else:
            return jsonify({'success': False, 'message': '회원가입에 실패했습니다.'}), 500
    
    except Exception as e:
        print(f"오류 발생: {e}")
        return jsonify({'success': False, 'message': '서버 오류가 발생했습니다.'}), 500

@api_curator.route('/plyy/api/curator/<c_id>', methods=['GET'])
def api_curator_view(c_id):
    play_lists = []
    c_info = curator_info(c_id)
    print(c_info)
    c_plyy = cu_plyy(c_id)
    c_isliked = None

    for plyy in c_plyy:
        plyy_data = {
            'pid': plyy[0],
            'ptitle': plyy[1],
            'pimg': plyy[2],
            'pgen': plyy[3],
            'pupdate': plyy[4],
            'pcmt': plyy[5],
            'ptag': plyy[8],
            'pliked': None
        }
        play_lists.append(plyy_data)

    pidlist = [play_lists[i]['pid'] for i in range(len(play_lists))]

    if 'id' in session and session['id']:
        u_id = extract_user(session['id'])
        if u_id:
            c_isliked = curatorlike_status(c_id, u_id)
            p_isliked = plyylike_status(pidlist, u_id)

            for plyy in play_lists:
                plyy['pliked'] = p_isliked.get(plyy['pid'], False)

    return jsonify({
        'curator': {
            'c_info': {
                'c_id': c_info[0],
                'c_name': c_info[1],
                'c_img': c_info[2],
                'c_intro': c_info[3],
                'c_tags': c_info[4],
                'c_plyys': c_info[5],
                'c_likes': c_info[6],
                'c_liked': c_isliked
            },
            'plyy': play_lists
        }
    })

@like_curator.route('/plyy/api/like/<u_id>/<c_id>', methods=['POST'])
def like_curator_view(u_id, c_id):
    u_id = extract_user(u_id)
    success = curator_like(c_id, u_id)
    if success:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False}), 500

@unlike_curator.route('/plyy/api/unlike/<u_id>/<c_id>', methods=['DELETE'])
def unlike_curator_view(u_id, c_id):
    u_id = extract_user(u_id)
    success = curator_unlike(c_id, u_id)
    if success:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False}), 500

@like_plyy.route('/plyy/api/plyylike/<u_id>/<p_id>', methods=['POST'])
def like_plyy_view(u_id, p_id):
    u_id = extract_user(u_id)
    success = plyy_like(p_id, u_id)
    if success:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False}), 500

@unlike_plyy.route('/plyy/api/plyyunlike/<u_id>/<p_id>', methods=['DELETE'])
def unlike_plyy_view(u_id, p_id):
    u_id = extract_user(u_id)
    success = plyy_unlike(p_id, u_id)
    if success:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False}), 500
