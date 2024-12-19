from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Secret key for session management

# Function to read the Excel file and prepare questions and answers
def read_excel(file_name):
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    df = pd.read_excel(file_path, engine='openpyxl')
    questions = df['Question'].tolist()
    answers = df['Answer'].tolist()
    return list(zip(questions, answers))

qa_pairs = read_excel("Kosa Kata.xlsx")

@app.route('/', methods=['GET'])
def quiz():
    session['correct_count'] = 0  # Initialize correct count
    return redirect(url_for('question', q_index=0))

@app.route('/question/<int:q_index>', methods=['GET', 'POST'])
def question(q_index):
    if request.method == 'POST':
        user_answer = request.form['answer'].strip().lower()
        correct_answer = str(qa_pairs[q_index][1]).strip().lower()
        if user_answer == correct_answer:
            session['correct_count'] += 1
            result = f'Correct, the answer is {qa_pairs[q_index][1]}'
        else:
            result = f'Wrong! The correct answer is: {qa_pairs[q_index][1]}'
        return render_template('result.html', result=result, q_index=q_index, total=len(qa_pairs))

    if q_index < len(qa_pairs):
        question = qa_pairs[q_index][0]
        return render_template('question.html', question=question, q_index=q_index, total=len(qa_pairs))
    else:
        return redirect(url_for('done'))

@app.route('/next/<int:q_index>', methods=['GET'])
def next_question(q_index):
    return redirect(url_for('question', q_index=q_index + 1))

@app.route('/done', methods=['GET'])
def done():
    correct_count = session.get('correct_count', 0)
    total_questions = len(qa_pairs)
    return render_template('done.html', correct_count=correct_count, total_questions=total_questions)

# Pass enumerate to templates
@app.context_processor
def utility_processor():
    return dict(enumerate=enumerate)

if __name__ == "__main__":
    app.run(debug=True)
