from flask import Flask, url_for, render_template, request
import main
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method =='GET':
        return render_template('index.html')
    else:
        groups = main.getGroups(request.form['devInput'])
        if groups == None:
            return 'Not valid key or no groups found'
        return render_template('groups.html', groups=groups)

@app.route('/chatlog', methods=['POST'])
def chatlog():
    groupId = request.form['groupId']
    return 'In Progress'