from flask import Flask, request, render_template, redirect, flash, session
from surveys import satisfaction_survey as survey
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "password"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESPONSES_KEY = 'responses'


@app.route('/')
def home():

    return render_template('start.html', title=survey.title, info=survey.instructions)


@app.route('/start', methods=['POST'])
def start():

    session[RESPONSES_KEY] = []
    return redirect('/questions/0')


@app.route('/questions/<int:question_id>')
def show_question(question_id):

    responses = session.get(RESPONSES_KEY)

    if(responses is None):
        return redirect('/')
    if(len(responses) != question_id):
        flash(f'Invalid question: {question_id}')
        return redirect(f'/questions/{len(question_id)}')

    return render_template('question.html', question=survey.questions[question_id], question_num=question_id)


@app.route('/answer', methods=['POST'])
def check_question():

    answer = request.form['choice']

    responses = session[RESPONSES_KEY]
    responses.append(answer)
    session[RESPONSES_KEY] = responses

    if (len(responses)<len(survey.questions)):
        return redirect(f'/questions/{len(responses)}')
    elif (len(responses)==len(survey.questions)):
        return redirect('/finish')


@app.route('/finish')
def finish():
    return render_template('finished.html')
