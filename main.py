from flask import (Flask,
                   render_template,
                   request,
                   make_response,
                   redirect
                   )
import json
import models
from models import Student

app = Flask('app')


@app.route('/')
def index():
    models.initialize()
    return render_template("index.html",)


@app.route('/register', methods=['POST', 'GET'])
def register():
    data = dict(request.form.items())
    if data.get('id', None):
        Student.create(
            id=data.get('id',1),
            title=data.get('title', 'python class was hard today'),
            date=data.get('Date', 12/7/9),
            
        )
    return render_template("register_student.html")


@app.route('/students ')
def students():
    models.initialize()
    students = models.Student.select()
    return render_template("entries.html", students=students)


@app.route('/entries/edit/<id>', methods=['POST', 'GET'])
def edit_student(id="1"):
    student = Student.select().where(Student.id==id).first()
    data = dict(request.form.items())
    if data.get('id', None):
        student.id = data.get('id', student.id)
        student.Title = data.get('Title', student.Title)
        student.Datewritten = data.get('Datewritten', student.Datewritten)
        student.save()
        return redirect('/entries')
    context = {'student': student}
    return render_template('edit.html', **context)

@app.route('/welcome', methods=['POST'])
def welcome():
    data = dict(request.form.items())
    name = str(data.get('name', 'Guest'))
    email = str(data.get('email', 'no@email.com'))
    course = str(data.get('course', 'Not provided'))
    context = {'name':name, 'email':email, 'course': course}
    response = make_response(render_template("welcome.html", **context))
    response.set_cookie('register_app',json.dumps(context))
    return response

@app.route('/edit')
def edit():
    data = request.cookies.get('register_app')
    context = json.loads(data)
    response = make_response(render_template("edit.html", **context))
    return response


app.run(debug=True, host='0.0.0.0', port=8080)