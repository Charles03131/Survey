from flask import Flask, request, render_template, redirect, flash, session,url_for
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey


RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "ASECRET"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route("/")
def show_start():
    """survey type and directions"""

    return render_template('start.html',survey=survey)


@app.route("/begin", methods=["POST"])
def start():
    """clear session of responses"""
    session[RESPONSES_KEY]=[]

    return redirect("/questions/0")

@app.route("/answer",methods=["POST"])
def answer_question():
    """save response and redirect to next question"""

    #get answer selection
    choice=request.form['answer']

    #add response to the session
    responses=session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY]=responses

    if(len(responses)==len(survey.questions)):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")





@app.route("/questions/<int:qid>")
def show_question(qid):
    """display current question"""
    responses=session.get(RESPONSES_KEY)

    if(responses is None):
        return redirect("/")
    if(len(responses)==len(survey.questions)):
        #all the questions have been answered. Thank the user. 
        return redirect("/complete")
    if(len(responses) != qid):
        #trying to acces questions out of order
        flash(f"Invalid question id:{qid}.")
        return redirect(f"/questions/{len(responses)}")
    question=survey.questions[qid]
    return render_template("question.html",question_num=qid,question=question)

@app.route('/complete')
def survey_complete():
    """survey complete , show completion page"""
    return render_template("complete.html")
    
