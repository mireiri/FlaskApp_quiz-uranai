from flask import (Flask, render_template, session,
                   redirect, url_for, request, flash)
import os
from quiz import quiz
from fortune_telling import fortune_telling


#FLASKのインスタンス化
app = Flask(__name__)

#sessionを扱うためにsecret_keyを設定
key = os.urandom(21)
app.secret_key = key

#ログインパスワードを設定
LOGIN_PW = 'RX-105'

#indexページ
@app.route('/')
def index():
    if not session.get('login'):
        return redirect(url_for('login'))
    else:
        return render_template('index.html')

#ログインページ
@app.route('/login')
def login():
    return render_template('login.html')

#ログイン認証
@app.route('/loginauth', methods=['POST'])
def loginauth():
    login_pw = request.form['login_pw']

    if login_pw == LOGIN_PW:
        session['login'] = True
    else:
        session['login'] = False

    if session['login']:
        return redirect(url_for('index'))
    else:
        flash('もう一度正しく入力してください')
        return redirect(url_for('login'))

#ログアウト
@app.route('/logout')
def logout():
    session.pop('login', None)
    return redirect(url_for('index'))

#クイズゲーム
@app.route('/quiz_game')
def quiz_game():
    selected_qa = quiz()
    num = [i for i in range(1, 6)]
    question = []
    answer = []
    for i in selected_qa:
        question.append(i[0])
        answer.append(i[1])
    session['answer'] = answer
    return render_template('question.html', data=zip(num, question))

@app.route('/answercheck', methods=['POST'])
def answercheck():
    score = 0
    answer = session.get('answer')
    user_answer = request.form.getlist('user_answer')
    for i, j in zip(user_answer, answer):
        if i == j:
            score += 20
    return render_template('result.html', score=score,
                            result_data=zip(answer, user_answer))

#占いゲーム
@app.route('/uranai')
def uranai():
    result, msg, who = fortune_telling()
    return render_template('uranai_result.html',
                            result=result, msg=msg, who=who)


#アプリケーションの起動
if __name__ == '__main__':
    app.run(debug=True)