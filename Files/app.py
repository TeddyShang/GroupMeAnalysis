from flask import Flask, url_for, render_template, request, session
import main
import json
from werkzeug.contrib.cache import SimpleCache
app = Flask(__name__)
app.secret_key = 'bananas'
cache = SimpleCache()

@app.route('/', methods=['GET'])
def index():
    if request.method =='GET':
        return render_template('index.html')


@app.route('/groups', methods =['GET', 'POST'])
def groups():
        c = cache.get('userGroups')
        if c is not None:
            return render_template('groups.html', groups=c)
        if request.method == 'POST':
            groups = main.getGroups(request.form['devInput'])
            if groups == None:
                return 'Not valid key or no groups found'
            cache.set('userGroups', groups, timeout = 5 * 60)
            session['devToken'] = request.form['devInput']
            return render_template('groups.html', groups=groups)
        return render_template('index.html')

@app.route('/chatlog', methods=['POST'])
def chatlog():
    devToken = session.get('devToken')
    groupId = request.form['groupId']
    c = cache.get(groupId)
    if c is not None:
        return render_template('chatlog.html', chatlog=c)
    chatlog = main.getChatlog(groupId,devToken)
    cache.set(groupId, chatlog, timeout = 5 * 60)
    return render_template('chatlog.html', chatlog=chatlog)