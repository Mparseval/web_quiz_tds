from flask import Flask, render_template, request, redirect, url_for, session
import csv

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a random secret key for production

def parse_file(filename):
    qa_list = []
    try:
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for line_num, row in enumerate(reader, 1):
                if not row or len(row) < 2:
                    print(f"Warning: Couldn't parse line {line_num}: {row}")
                    continue
                answer_field = row[0].strip()
                statement = row[1].strip()
                # Extract 'VERO' or 'FALSO' from the answer field
                if 'VERO' in answer_field.upper():
                    answer = 'VERO'
                elif 'FALSO' in answer_field.upper():
                    answer = 'FALSO'
                else:
                    print(f"Warning: Couldn't extract answer from line {line_num}: {row}")
                    continue
                qa_list.append({'statement': statement, 'answer': answer})

        return qa_list
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

filename = "vero-falso-soluzioni.csv"
questions = parse_file(filename)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'current_question' not in session:
        # Initialize session variables
        session['current_question'] = 0
        session['score'] = 0
        feedback = None
    else:
        feedback = None

    if request.method == 'POST':
        # Process the answer
        user_answer = request.form.get('answer')
        correct_answer = questions[session['current_question']]['answer']
        if user_answer == correct_answer:
            session['score'] += 1
            feedback = "Correct!"
        else:
            feedback = "Incorrect!"
        session['current_question'] += 1

    if session['current_question'] < len(questions):
        question = questions[session['current_question']]['statement']
        progress = int((session['current_question'] / len(questions)) * 100)
        return render_template('quiz.html', question=question, question_num=session['current_question']+1,
                               total_questions=len(questions), feedback=feedback, progress=progress)
    else:
        # Quiz finished
        score = session['score']
        total_questions = len(questions)
        # Reset session variables
        session.pop('current_question', None)
        session.pop('score', None)
        return render_template('result.html', score=score, total_questions=total_questions)

if __name__ == "__main__":
    app.run(debug=True)
