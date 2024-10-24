from flask import Flask, render_template, request, redirect, url_for, session
import csv

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure random key

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
                if 'VERO' in answer_field.upper():
                    answer = 'VERO'
                elif 'FALSO' in answer_field.upper():
                    answer = 'FALSO'
                else:
                    print(f"Warning: Couldn't extract answer from line {line_num}: {row}")
                    continue
                qa_list.append({'statement': statement, 'answer': answer})
                print(f"Loaded question {line_num}: {statement} [{answer}]")
            return qa_list
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

filename = "vero-falso-soluzioni.csv"
questions = parse_file(filename)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'answers' not in session:
        # Initialize session variables
        session['answers'] = [None] * len(questions)
        session['score'] = 0

    feedback = None
    question_number = None  # Ensure question_number is initialized
    action = request.args.get('action')

    if request.method == 'POST':
        # Process the answer
        user_answer = request.form.get('answer')
        question_number_str = request.form.get('question_number')
        if question_number_str is None:
            return "Error: Question number is missing.", 400
        try:
            question_number = int(question_number_str)
        except ValueError:
            return "Error: Invalid question number.", 400

        if question_number < 0 or question_number >= len(questions):
            return "Error: Question number out of range.", 400

        correct_answer = questions[question_number]['answer']
        if session['answers'][question_number] is None or isinstance(session['answers'][question_number], str):
            # Update to new data structure
            if user_answer == correct_answer:
                session['answers'][question_number] = {
                    'user_answer': user_answer,
                    'status': 'Correct'
                }
                session['score'] += 1
                feedback = "Correct!"
            else:
                session['answers'][question_number] = {
                    'user_answer': user_answer,
                    'status': 'Incorrect'
                }
                feedback = "Incorrect!"
        else:
            feedback = "You have already answered this question."
    else:
        question_number_str = request.args.get('question_number')
        if question_number_str is not None:
            try:
                question_number = int(question_number_str)
            except ValueError:
                return "Error: Invalid question number.", 400
        else:
            # Default to the first unanswered question
            if None in session['answers']:
                question_number = session['answers'].index(None)
            else:
                # All questions answered, show results
                score = session['score']
                total_questions = len(questions)
                # Reset session variables
                session.clear()
                return render_template('result.html', score=score, total_questions=total_questions)

    # Handle navigation actions
    if action == 'next':
        if question_number < len(questions) - 1:
            question_number += 1
    elif action == 'prev':
        if question_number > 0:
            question_number -= 1

    # Ensure question_number is within valid range
    if question_number is None or question_number < 0 or question_number >= len(questions):
        return "Error: Invalid question number.", 400

    # Retrieve user's previous answer and status if available
    user_answer = None
    status = None
    answer_entry = session['answers'][question_number]
    if answer_entry is not None:
        if isinstance(answer_entry, dict):
            user_answer = answer_entry.get('user_answer')
            status = answer_entry.get('status')
        elif isinstance(answer_entry, str):
            # Handle old data format
            user_answer = None  # We don't have the user's answer
            status = answer_entry  # The status is 'Correct' or 'Incorrect'

    # Display the question
    question = questions[question_number]['statement']
    progress = int(((question_number + 1) / len(questions)) * 100)
    answers = session['answers']
    current_question = question_number  # Ensure current_question is set
    return render_template(
        'quiz.html',
        question=question,
        question_num=question_number + 1,
        total_questions=len(questions),
        progress=progress,
        answers=answers,
        current_question=current_question,
        feedback=feedback,
        user_answer=user_answer,
        status=status
    )

if __name__ == "__main__":
    app.run(debug=True)
