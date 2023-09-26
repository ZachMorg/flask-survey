from flask import Flask, request, render_template, redirect, flash
from surveys import satisfaction_survey as survey
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "password"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


responses = []

@app.route('/')
def home():
    responses = []
    return render_template('start.html', title=survey.title, info=survey.instructions)


@app.route('/questions/<int:question_id>')
def show_question(question_id):

    if(len(responses)==0):
        return redirect('/')
    if(len(responses)!=question_id):
        flash(f'Invalid question: {question_id}')
        return redirect(f'/questions/{len(question_id)}')

    return render_template('question.html', question=survey.questions[question_id], question_num=question_id)


@app.route('/answer', methods=['POST'])
def check_question():
    answer = request.form['choice']
    responses.append(answer)

    if (len(responses)<len(survey.questions)):
        return redirect(f'/questions/{len(responses)}')
    elif (len(responses)==len(survey.questions)):
        return redirect('/finish')


@app.route('/finish')
def finish():
    return render_template('finished.html')
