from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey 

app = Flask(__name__)
app.config['SECRET_KEY'] = "my-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


debug = DebugToolbarExtension(app)


@app.route('/')
# returns home html
def start_homepage():
    return render_template("survey_home.html", survey = survey)

@app.route('/survey-begins', methods = ['POST']) 
def begin_survey():
# when survey begins, reset the responses back to zero
    session["responses"] = []
    return redirect("/questions/0")

@app.route('/answer', methods = ['POST'])
def responding():
    selection = request.form['answer']
    
    response = session["responses"]
    response.append(selection)
    session["responses"] = response 

# if the length of the responses list is equal to the amount of survey questions, redirect user to the "/complete" link
# else redirect the user to a the link /questions/the-length-of-responses
# example: if the user has answered 1 question, it'll send the user to /questions/1
    
    if (len(response) == len(survey.questions)):
        return redirect('/complete')

    else:
        return redirect(f'/questions/{len(response)}')

@app.route('/questions/<int:qnum>')
def quest_redir(qnum):
    response = session.get("responses")

# if there is no response, redirect user back to home page
    if (response is None):
        return redirect('/')

# if the number of responses is equal to the number of survery questions, redirect user to the completion page
    if (len(response) == len(survey.questions)):
        return redirect('/complete')

# if the number of responses does not equal the page number, flash wrong question number message
# and redirect user back to the proper page
    if (len(response) != qnum):
        flash (f"Wrong question number: {qnum}.")
        return redirect(f"/questions/{len(response)}")

    question = survey.questions[qnum]
    return render_template("questions.html", question_num = qnum, question = question)

    @app.route('/complete')
    # when the survey is completed, send to complete thank you message
    def completed_survey():
        return render_template("complete.html")

        # I keep getting an error when trying to route to my "complete" page and I'm not sure why


