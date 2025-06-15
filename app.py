from flask import Flask, render_template, request, redirect, send_file
import csv
import os
import uuid
from fpdf import FPDF

app = Flask(__name__)
CSV_FILE = 'mess_data.csv'
FIELDS = ['id', 'name', 'roll', 'room', 'food']

# Utility functions
def load_data():
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, 'r', newline='', encoding='utf-8') as file:
        return list(csv.DictReader(file))

def save_data(data):
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(data)

# Routes
@app.route('/')
def index():
    search = request.args.get('search', '').lower()
    students = load_data()
    if search:
        students = [s for s in students if search in s['name'].lower() or search in s['roll']]
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = load_data()
        new_student = {
            'id': str(uuid.uuid4()),
            'name': request.form['name'],
            'roll': request.form['roll'],
            'room': request.form['room'],
            'food': request.form['food']
        }
        data.append(new_student)
        save_data(data)
        return redirect('/')
    return render_template('add_edit.html', student={}, action='Add')

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    data = load_data()
    student = next((s for s in data if s['id'] == id), None)
    if not student:
        return "Student not found", 404
    if request.method == 'POST':
        student['name'] = request.form['name']
        student['roll'] = request.form['roll']
        student['room'] = request.form['room']
        student['food'] = request.form['food']
        save_data(data)
        return redirect('/')
    return render_template('add_edit.html', student=student, action='Edit')

@app.route('/delete/<id>')
def delete(id):
    data = load_data()
    data = [s for s in data if s['id'] != id]
    save_data(data)
    return redirect('/')

@app.route('/export_pdf')
def export_pdf():
    students = load_data()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Mess Student List", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(40, 10, "Name", 1)
    pdf.cell(30, 10, "Roll", 1)
    pdf.cell(40, 10, "Room", 1)
    pdf.cell(40, 10, "Food", 1)
    pdf.ln()
    for s in students:
        pdf.cell(40, 10, s['name'], 1)
        pdf.cell(30, 10, s['roll'], 1)
        pdf.cell(40, 10, s['room'], 1)
        pdf.cell(40, 10, s['food'], 1)
        pdf.ln()
    path = "student_list.pdf"
    pdf.output(path)
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
