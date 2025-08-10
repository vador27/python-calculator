import tkinter as tk
import re
import math

# Create main window
root = tk.Tk()
root.title("Pierre-Olivier's Simple Calculator")
root.geometry("380x550")
root.configure(bg="#F0F0F0")
root.resizable(False, False)

# Grid configuration
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=0)
root.grid_columnconfigure(2, weight=0)
root.grid_columnconfigure(3, weight=1)
for i in range(7):  # Adjusted for extra row of buttons
    root.grid_rowconfigure(i, weight=1)

# Settings
maxChar = 22
app_font = ('Times New Roman', 18)
orangeButtons = ["+", "-", "x", "÷", "=", "⌫"]
grayButtons = ["π", "%", "CE", "^", "DEL", "√"]

# Entry display
entry = tk.Entry(root, width=maxChar, font=(app_font[0], 24), bd=4, relief='ridge', justify='right')
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=20)

# Get current text from entry
def get_current_text():
    return entry.get()

# On button click (numbers and operators)
def on_click(char):
    current_text = get_current_text()
    if current_text.startswith("Error:"):
        entry.delete(0, tk.END)
        current_text = ""
    segments = re.split(r'[\+\-\*/]', current_text)
    last_segment = segments[-1] if segments else ''
    if char.isdigit() or char == '.':
        if len(last_segment) < maxChar - 2 and len(current_text) < maxChar:
            entry.insert(tk.END, str(char))
    else:
        if len(current_text) < maxChar:
            entry.insert(tk.END, str(char))

# Sanitize expression for eval and handle %, ^, x, ÷, and π symbol
def sanitize_expression(expr):
    expr = expr.replace("x", "*").replace("÷", "/")
    expr = expr.replace("^", "**")
    expr = expr.replace("π", str(math.pi))  # Convert π symbol to number here
    # Handle square roots - replace √N with sqrt(N)
    expr = re.sub(r'√(\d+(\.\d*)?)', r'math.sqrt(\1)', expr)
    # Convert N% to (N/100)
    expr = re.sub(r'(\d+(\.\d*)?)%', r'(\1/100)', expr)
    return expr

# Calculation
def calculate():
    current_text = get_current_text()
    if current_text.startswith("Error:"):
        entry.delete(0, tk.END)
        return
    try:
        expression = sanitize_expression(current_text)
        result = eval(expression)
        result_str = str(result)
        if len(result_str) > maxChar:
            entry.delete(0, tk.END)
            entry.insert(0, "Error: Too long!")
        else:
            entry.delete(0, tk.END)
            entry.insert(0, result_str)
    except Exception:
        entry.delete(0, tk.END)
        entry.insert(0, "Error: Invalid")

# Clear all
def reset():
    entry.delete(0, tk.END)

# Backspace
def backspace():
    current_text = get_current_text()
    if current_text.startswith("Error:"):
        entry.delete(0, tk.END)
        return
    entry.delete(len(current_text)-1, tk.END)

# Sign change (±)
def signchange():
    current_text = get_current_text()
    if current_text.startswith("Error:"):
        entry.delete(0, tk.END)
        return

    segments = re.split(r'([\+\-\*/x÷])', current_text)
    if not segments:
        return

    for i in range(len(segments)-1, -1, -1):
        seg = segments[i].strip()
        if seg and not re.match(r'[\+\-\*/x÷]', seg):
            if seg.startswith('-'):
                segments[i] = seg[1:]
            else:
                segments[i] = '-' + seg
            break

    new_text = ''.join(segments)
    entry.delete(0, tk.END)
    entry.insert(0, new_text)

# Insert Pi symbol (π)
def insert_pi():
    current_text = get_current_text()
    if current_text.startswith("Error:"):
        entry.delete(0, tk.END)
        current_text = ""
    if len(current_text) + 1 <= maxChar:
        entry.insert(tk.END, 'π')  # Insert symbol, not number

# Insert square root symbol (√)
def insert_sqrt():
    current_text = get_current_text()
    if current_text.startswith("Error:"):
        entry.delete(0, tk.END)
        current_text = ""
    if len(current_text) + 1 <= maxChar:
        entry.insert(tk.END, '√')  # Insert square root symbol

# Action mapping
button_actions = {
    '=': calculate,
    'CE': reset,
    'DEL': backspace,
    '±': signchange,
    'π': insert_pi,
    '√': insert_sqrt,
}

# Button layout (colspan handled if present)
buttons = [
    ('CE', 1, 0), ('DEL', 1, 1), ('%', 1, 2), ('÷', 1, 3),
    ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('x', 2, 3),
    ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
    ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
    ('0', 5, 0), ('.', 5, 1), ('±', 5, 2), ('=', 5, 3),
    ('π', 6, 0), ('^', 6, 1), ('√', 6, 2),
]

# Button creation
def create_button(text, row, col, colspan=1, width=5, bg="#DDDDDD", fg="#000000"):
    action = button_actions.get(text, lambda x=text: on_click(x))
    btn = tk.Button(root, text=text, width=width, height=2, font=app_font, command=action, bg=bg, fg=fg)
    btn.grid(row=row, column=col, columnspan=colspan, padx=5, pady=5)

# Draw buttons
for item in buttons:
    text = item[0]
    row = item[1]
    col = item[2]
    colspan = item[3] if len(item) > 3 else 1

    if text in orangeButtons:
        create_button(text, row, col, colspan=colspan, bg="#FFCC02", fg="#000000")
    elif text in grayButtons:
        create_button(text, row, col, colspan=colspan, bg="#DDDDDD", fg="#000000")
    else:
        create_button(text, row, col, colspan=colspan, bg="#FAFAFA", fg="#000000")

# Run app
root.mainloop()
