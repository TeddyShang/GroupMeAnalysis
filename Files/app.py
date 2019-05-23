from flask import Flask, url_for, render_template, request, session, redirect
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


@app.route('/groups', methods =['GET'])
def groups():
    c = cache.get('userGroups')
    if c is not None:
        return render_template('groups.html', groups=c)
    groups = main.getGroups(session.get('devToken'))
    if groups == None:
        return render_template('error.html', error='No groups found. Please login again')
    cache.set('userGroups', groups, timeout = 5 * 60)
    return render_template('groups.html', groups=groups)

@app.route('/groupsPost', methods =['POST'])
def groupsPost():
    groups = main.getGroups(request.form['devInput'])
    if groups == None:
         return render_template('error.html', error='Not valid key or no groups found')
    cache.set('userGroups', groups, timeout = 5 * 60)
    session['devToken'] = request.form['devInput']
    return redirect(url_for('groups'))


@app.route('/chatlog', methods=['POST'])
def chatlog():
    devToken = session.get('devToken')
    groupId = request.form['groupId']
    c = cache.get(groupId)
    m = main.getMemberInformation(groupId, devToken)
    if c is not None:
        return render_template('chatlog.html', chatlog=c, memberInfo = m)
    chatlog = main.getChatlog(groupId,devToken)
    cache.set(groupId, chatlog, timeout = 5 * 60)
    return render_template('chatlog.html', chatlog=chatlog, memberInfo = m)

## we get the chatlog and then manipulate it to get statistics
## simple user: [MessagesSent, Likes Received, Likes Given, Self Likes]
## simple group aggregate: total messages, average likes, total likes
## advanced user: average likes, average adjusted, +/- of group average, total likes
@app.route('/stats', methods=['POST'])
def stats():
    devToken = session.get('devToken')
    groupId = request.form['groupId']
    c = cache.get(groupId)
    m = main.getMemberInformation(groupId, devToken)
    if c is not None:
        ##calculate stats with cached log
        stats, gTotals = main.getStats(c)
        return render_template('stats.html', stats=stats, memberInfo = m, gTotals=gTotals)
    ##otherwise get chatlog and get stats with it
    chatlog = main.getChatlog(groupId,devToken)
    cache.set(groupId, chatlog, timeout = 5 * 60)
    stats, gTotals = main.getStats(chatlog)
    return render_template('stats.html', stats=stats, memberInfo = m, gTotals=gTotals)


#we pass the same information from /stats
@app.route('/viz', methods=['POST'])
def viz():
    devToken = session.get('devToken')
    groupId = request.form['groupId']
    c = cache.get(groupId)
    m = main.getMemberInformation(groupId, devToken)
    if c is not None:
        ##calculate stats with cached log
        stats, gTotals = main.getStats(c)
        ##pass stats and memberInfo for processing
        ms,lr,lg,sl = main.getShare(stats, m)
        return render_template('viz.html', stats=stats, memberInfo = m, gTotals=gTotals, chatlog = c, ms = ms,
                               lg=lg, lr = lr, sl = sl)
    ##otherwise get chatlog and get stats with it
    chatlog = main.getChatlog(groupId,devToken)
    cache.set(groupId, chatlog, timeout = 5 * 60)
    stats, gTotals = main.getStats(chatlog)
    ##pass stats and memberInfo for processing
    ms,lr,lg,sl = main.getShare(stats, m)
    return render_template('viz.html', stats=stats, memberInfo = m, gTotals=gTotals, chatlog = c, ms = ms,
                               lg=lg, lr = lr, sl = sl)