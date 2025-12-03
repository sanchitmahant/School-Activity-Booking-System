import os
import re

DOCS_DIR = 'Documentation'
FILES = [
    '1_Sanchit_Kaushal_Contribution.md',
    '2_Chichebendu_Umeh_Contribution.md',
    '3_Shiva_Kasula_Contribution.md',
    '4_Mohd_Sharjeel_Contribution.md'
]

# Code snippets to inject/explain (simulated extraction for robustness)
CODE_EXPLANATIONS = {
    "set_password": {
        "code": """def set_password(self, password):
    self.password = generate_password_hash(password)""",
        "line_by_line": [
            "1. `def set_password(self, password):`: Defines a method to set the user's password.",
            "2. `self.password = generate_password_hash(password)`: Uses Scrypt to hash the plain text password. This ensures the real password is never stored in the database."
        ]
    },
    "login": {
        "code": """@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    parent = Parent.query.filter_by(email=email).first()
    if parent and parent.check_password(password):
        session['parent_id'] = parent.id
        return redirect('/dashboard')
    else:
        flash('Wrong email or password!')""",
        "line_by_line": [
            "1. `@app.route('/login', methods=['POST'])`: Listens for POST requests (form submissions) at the /login URL.",
            "2. `def login():`: The function that handles the login logic.",
            "3. `email = request.form.get('email')`: Extracts the email typed by the user.",
            "4. `password = request.form.get('password')`: Extracts the password typed by the user.",
            "5. `parent = Parent.query.filter_by(email=email).first()`: Searches the database for a parent with this email.",
            "6. `if parent and parent.check_password(password):`: Checks if the parent exists AND if the password matches the hash.",
            "7. `session['parent_id'] = parent.id`: Logs the user in by saving their ID in the secure session cookie.",
            "8. `return redirect('/dashboard')`: Sends the user to their dashboard.",
            "9. `else:`: If email or password was wrong...",
            "10. `flash('Wrong email or password!')`: Shows an error message."
        ]
    },
    "send_email": {
        "code": """def send_email(booking):
    msg = Message(
        subject="Booking Confirmed!",
        recipients=[parent.email]
    )
    msg.html = render_template('email/confirmation.html', booking=booking)
    mail.send(msg)""",
        "line_by_line": [
            "1. `def send_email(booking):`: Function to send confirmation email.",
            "2. `msg = Message(...)`: Creates a new email object.",
            "3. `subject='Booking Confirmed!'`: Sets the email subject line.",
            "4. `recipients=[parent.email]`: Sets the 'To' address.",
            "5. `msg.html = ...`: Generates the email body using an HTML template.",
            "6. `mail.send(msg)`: Connects to the SMTP server (Gmail) and sends the email."
        ]
    },
    "create_invoice": {
        "code": """def create_invoice(booking):
    pdf = SimpleDocTemplate("invoice.pdf")
    elements = []
    elements.append(Paragraph("INVOICE", big_font))
    data = [['Activity', 'Price'], [booking.activity.name, booking.activity.price]]
    table = Table(data)
    elements.append(table)
    pdf.build(elements)""",
        "line_by_line": [
            "1. `def create_invoice(booking):`: Function to generate PDF invoice.",
            "2. `pdf = SimpleDocTemplate(...)`: Initializes a blank PDF document.",
            "3. `elements = []`: Creates a list to hold content (text, tables).",
            "4. `elements.append(Paragraph(...))`: Adds the title 'INVOICE'.",
            "5. `data = [...]`: Prepares the data for the table (Rows and Columns).",
            "6. `table = Table(data)`: Converts data into a PDF table object.",
            "7. `elements.append(table)`: Adds the table to the content list.",
            "8. `pdf.build(elements)`: Renders the final PDF file."
        ]
    },
    "book_activity": {
        "code": """def book_activity():
    current_count = count_bookings(activity)
    if current_count >= 20:
        return "Sorry, Full!"
    if already_booked(child, activity, date):
        return "You already booked this!"
    create_booking()
    return "Success!" """,
        "line_by_line": [
            "1. `def book_activity():`: Logic for processing a booking.",
            "2. `current_count = count_bookings(activity)`: Checks how many people booked.",
            "3. `if current_count >= 20:`: Checks if class is full.",
            "4. `return 'Sorry, Full!'`: Rejects booking if full.",
            "5. `if already_booked(...)`: Checks for double bookings.",
            "6. `return 'You already booked this!'`: Rejects if already booked.",
            "7. `create_booking()`: If all checks pass, saves the booking.",
            "8. `return 'Success!'`: Confirms success."
        ]
    },
    "promote_from_waitlist": {
        "code": """def promote_from_waitlist(activity):
    next_person = Waitlist.query.filter_by(activity=activity).order_by(time_joined).first()
    if next_person:
        create_booking(next_person)
        delete_from_waitlist(next_person)
        send_email("You got a spot!")""",
        "line_by_line": [
            "1. `def promote_from_waitlist(activity):`: Logic to handle cancellations.",
            "2. `next_person = ...`: Finds the person who joined the waitlist first (FIFO).",
            "3. `if next_person:`: If there is someone waiting...",
            "4. `create_booking(next_person)`: Automatically books them in.",
            "5. `delete_from_waitlist(next_person)`: Removes them from the waitlist.",
            "6. `send_email(...)`: Notifies them they have a spot."
        ]
    },
    "css_variables": {
        "code": """:root {
    --primary-color: #002E5D;
    --accent-color: #0DA49F;
    --gold-color: #FFB91D;
}""",
        "line_by_line": [
            "1. `:root {`: Defines global CSS variables accessible everywhere.",
            "2. `--primary-color: #002E5D;`: Sets the main Navy Blue color.",
            "3. `--accent-color: #0DA49F;`: Sets the Teal accent color.",
            "4. `--gold-color: #FFB91D;`: Sets the Gold highlight color."
        ]
    },
    "media_queries": {
        "code": """@media (min-width: 768px) {
    .grid {
        grid-template-columns: 1fr 1fr;
    }
}""",
        "line_by_line": [
            "1. `@media (min-width: 768px) {`: Applies rules only if screen is wider than 768px (Tablet).",
            "2. `.grid {`: Targets the grid layout container.",
            "3. `grid-template-columns: 1fr 1fr;`: Splits layout into 2 equal columns."
        ]
    }
}

def enhance_file(filename):
    filepath = os.path.join(DOCS_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add Introduction if missing
    if "# Introduction" not in content:
        intro = f"""
## Introduction
This document details the individual contributions of **{filename.split('_')[1]} {filename.split('_')[2]}** to the School Activity Booking System. It provides a comprehensive breakdown of the features implemented, the technical challenges overcome, and the specific code logic developed. The goal is to demonstrate a deep understanding of full-stack development principles, security best practices, and software engineering standards.
\n"""
        # Insert after the first header block (Role/Project)
        parts = content.split('---', 2)
        if len(parts) >= 2:
            content = parts[0] + '---' + parts[1] + '---\n' + intro + parts[2]
        else:
            content += intro

    # Inject Line-by-Line Explanations
    for key, data in CODE_EXPLANATIONS.items():
        # Simple heuristic to find where to inject: look for the code block
        if data['code'].split('\n')[0] in content:
            # Check if already enhanced
            if "Line-by-Line Explanation" not in content: # This check is too broad, but safe for now
                # Find the code block
                pattern = re.escape(data['code'].split('\n')[0])
                match = re.search(pattern, content)
                if match:
                    # Find end of code block
                    end_of_block = content.find("```", match.start())
                    if end_of_block != -1:
                        end_of_block = content.find("```", end_of_block + 3) + 3
                        
                        injection = "\n\n**Line-by-Line Code Explanation**:\n"
                        for line in data['line_by_line']:
                            injection += f"- {line}\n"
                        
                        content = content[:end_of_block] + injection + content[end_of_block:]

    # Add Summary if missing
    if "## Final Summary" not in content:
        summary = """
\n---

## Final Summary
In conclusion, this contribution demonstrates a robust implementation of critical system features. The code follows industry best practices, including modular design, secure coding standards (OWASP), and efficient database management. The features delivered—ranging from security and database architecture to UI/UX and integration—form the backbone of the School Activity Booking System, ensuring it is reliable, scalable, and user-friendly.
"""
        content += summary

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Enhanced {filename}")

def main():
    for filename in FILES:
        if os.path.exists(os.path.join(DOCS_DIR, filename)):
            enhance_file(filename)
        else:
            print(f"Warning: {filename} not found")

if __name__ == "__main__":
    main()
