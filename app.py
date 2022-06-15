from flask import Flask, request, render_template, redirect, flash
from surveys import satisfaction_survey as survey

responses = []

app = Flask(__name__)

@app.route('/')
def show_surveys():
    """Show surveys"""

    return render_template("survey_start.html", survey=survey)

@app.route('/begin', methods=["POST"])
def begin_survey():
    """Begin survey"""

    return redirect("/questions/0")

@app.route('/questions/<int:qid>')
def show_question(qid):
    """Display the question"""

    if (responses is None):
        #no responses -> redirect to home page
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        #if survey is completed -> redirect to completion page
        return redirect("/completed")
    
    if (len(responses) != qid):
        #if the question id in url is not equal to amount of responses -> redirect to correct question
        flash("Invalid question")
        return redirect(f"/questions/{len(responses)}")

    return render_template("question.html", qid=qid, question=survey.questions[qid])

@app.route('/answer', methods=["POST"])
def handle_question():
    """Get user answer and redirect"""

    choice = request.form['answer']
    responses.append(choice)

    if len(responses) == len(survey.questions):
        return redirect("/completed")

    return redirect(f"/questions/{len(responses)}")

@app.route('/completed')
def end_survey():
    """Display completion page"""

    return render_template("completion.html")
