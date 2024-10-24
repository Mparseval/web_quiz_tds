

# True or False Quiz Web Application

A simple web-based True or False quiz application built with Flask. Users can answer a series of true or false questions and receive immediate feedback.

## Features

- Interactive quiz with instant feedback.
- Progress bar to track quiz completion.
- Colored messages indicating correct or incorrect answers.
- Reads questions from a CSV file.

## Quick Start Guide

### Prerequisites

- **Python 3.6+**
- **pip** package manager
- **Git** (optional, for cloning the repository)

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/true-false-quiz.git
   cd true-false-quiz
   ```

   *Alternatively, download the ZIP file from GitHub and extract it.*

2. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python -m venv venv
   ```

   Activate the virtual environment:

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure the CSV File is in Place**

   Make sure `vero-falso-soluzioni.csv` (your quiz questions file) is in the project root directory.

### Running the Application

```bash
python app.py
```

Open your web browser and navigate to [http://localhost:5000](http://localhost:5000) to start the quiz.

## Project Structure

```
true-false-quiz/
├── app.py
├── requirements.txt
├── vero-falso-soluzioni.csv
├── templates/
│   ├── index.html
│   ├── quiz.html
│   └── result.html
└── static/
    └── styles.css
```

## Customization

- **Edit Questions**

  Modify `vero-falso-soluzioni.csv` to add or change quiz questions. Format:

  ```
  Answer;Question
  VERO;The sky is blue.
  FALSO;The Earth is flat.
  ```

- **Change Styles**

  Update `static/styles.css` to customize the application's appearance.

- **Set a Secret Key**

  Replace `'your_secret_key'` in `app.py` with a secure random string for production use:

  ```python
  app.secret_key = 'your_new_secret_key'
  ```

## Dependencies

- **Flask**

  Install via `pip install flask` or use the provided `requirements.txt`.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

This project is open-source and available under the [MIT License](LICENSE).

---

Enjoy the quiz!

If you have any questions or need assistance, please reach out.