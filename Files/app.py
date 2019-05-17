from flask import Flask, url_for, render_template, request, session
import main
import json
app = Flask(__name__)
app.secret_key = 'bananas'
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method =='GET':
        return render_template('index.html')
    else:
        groups = main.getGroups(request.form['devInput'])
        if groups == None:
            return 'Not valid key or no groups found'
        session['devToken'] = request.form['devInput']
        return render_template('groups.html', groups=groups)

@app.route('/chatlog', methods=['POST'])

def chatlog():
    devToken = session.get('devToken')
    groupId = request.form['groupId']
    chatlog = main.getChatlog(groupId,devToken)
    return render_template('chatlog.html', chatlog=chatlog)