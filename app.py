from flask import Flask, flash, session, request, redirect, render_template, url_for

from db.data_layer import create_project, get_all_projects, get_project, update_project, delete_project
from db.data_layer import create_task, get_all_tasks, update_task, delete_task, get_task

app = Flask(__name__)


@app.route("/")
def index():
    projects = get_all_projects()
    return render_template('index.html', projects = projects)



@app.route("/create_project", methods=["POST"])
def createproject():
    title = request.form.get("title")
    create_project(title)
    return redirect("/")

@app.route('/update/<project_id>', methods=["GET", "POST"])
def update(project_id):
    if request.method == 'POST':
        title = request.form.get("title")
        update_project(project_id, title)
        return title
    else:
        data = get_project(project_id)
        return render_template('page_update.html', data = data)

@app.route("/delete/<id>")
def delete(id):
    delete_project(id)
    return redirect("/")


## task things
@app.route("/view_project/<id>")
def view_project(id):
    project = get_project(id)
    tasks = get_all_tasks(id)
    return render_template('page_update.html', tasks = tasks, project = project)


@app.route("/create_task/<id_project>", methods=["POST"])
def createtask(id_project):
    description = request.form.get("description")
    create_task(id_project, description)
    return redirect("/view_project/{}".format(id_project))

@app.route('/updatetask/<task_id>', methods=["GET", "POST"])
def updatetask(task_id):
    if request.method == 'POST':
        description = request.form.get("description")
        project_id = request.form.get("project_id")
        update_task(task_id, description)
        return redirect("/view_project/{}".format(project_id))
    else:
        task = get_task(task_id)
        return render_template('page_update.html', task = task)

@app.route("/deletetask/<task_id>/<project_id>")
def deletetask(task_id, project_id):
    delete_task(task_id)
    return redirect("/view_project/{}".format(project_id))

app.run(debug=True)