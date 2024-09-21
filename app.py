from flask import Flask, render_template_string, request

app = Flask(__name__)

# Function to calculate required Midterm and Final grades
def calculate_required_grades(prelim_grade):
    passing_grade = 75.0
    dean_lister_grade = 90.0
    prelim_weight = 0.20
    midterm_weight = 0.30
    final_weight = 0.50

    # Calculate how much of the grade is still needed after the prelim grade
    remaining_grade = passing_grade - (prelim_weight * prelim_grade)

    # Calculate the required midterm and final grades
    required_midterm_grade = remaining_grade / (midterm_weight + final_weight)
    required_final_grade = remaining_grade / (final_weight + midterm_weight)

    # Calculate required midterm and final grades for Dean's Lister
    dean_midterm_grade = (dean_lister_grade - (prelim_weight * prelim_grade)) / (midterm_weight + final_weight)
    dean_final_grade = (dean_lister_grade - (prelim_weight * prelim_grade)) / (final_weight + midterm_weight)

    return required_midterm_grade, required_final_grade, dean_midterm_grade, dean_final_grade

@app.route('/', methods=['GET', 'POST'])
def index():
    # Define the HTML template for the app
    html_template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Grade Calculator</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f0f0f0; padding: 20px; }
            h1 { text-align: center; color: #333; }
            form { max-width: 400px; margin: 0 auto; padding: 20px; background-color: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); }
            label, input, button { display: block; width: 100%; margin-bottom: 15px; }
            input { padding: 10px; font-size: 16px; }
            button { background-color: #4CAF50; color: white; padding: 10px; font-size: 16px; border: none; cursor: pointer; }
            button:hover { background-color: #45a049; }
            .message { margin-top: 20px; text-align: center; font-size: 18px; color: green; }
            .error { margin-top: 20px; text-align: center; font-size: 18px; color: red; }
        </style>
    </head>
    <body>
        <h1>Grade Calculator</h1>
        <form method="POST">
            <label for="prelim_grade">Enter your Prelim grade (0-100):</label>
            <input type="text" id="prelim_grade" name="prelim_grade" required placeholder="Prelim Grade">
            <button type="submit">Calculate</button>
        </form>

        {% if message %}
            <p class="message">{{ message }}</p>
        {% endif %}
        {% if dean_message %}
            <p class="message">{{ dean_message }}</p>
        {% endif %}
        {% if error %}
            <p class="error">{{ error }}</p>
        {% endif %}
    </body>
    </html>
    '''
    
    if request.method == 'POST':
        try:
            # Get and validate the prelim grade input
            prelim_grade = float(request.form['prelim_grade'])
            if prelim_grade < 0 or prelim_grade > 100:
                return render_template_string(html_template, error='Grade must be between 0 and 100.')

            # Calculate required Midterm and Final grades
            required_midterm_grade, required_final_grade, dean_midterm_grade, dean_final_grade = calculate_required_grades(prelim_grade)

            # Check if it's possible to pass
            if required_midterm_grade > 100 or required_final_grade > 100:
                return render_template_string(html_template, message='It is not possible to pass with the current Prelim grade.', error=None)
            else:
                # Check if the student is eligible for Dean's Lister
                if dean_midterm_grade <= 100 and dean_final_grade <= 100:
                    dean_message = f'To qualify for Dean\'s Lister, you need at least {dean_midterm_grade:.2f} in Midterm and {dean_final_grade:.2f} in Final.'
                else:
                    dean_message = 'It is not possible to qualify for Dean\'s Lister with the current Prelim grade.'

                return render_template_string(html_template,
                                              message=f'To pass, you need at least {required_midterm_grade:.2f} in Midterm and {required_final_grade:.2f} in Final.',
                                              dean_message=dean_message,
                                              error=None)

        except ValueError:
            # Handle invalid input (non-numeric values)
            return render_template_string(html_template, error='Please enter a valid number for the Prelim grade.')

    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(debug=True)
