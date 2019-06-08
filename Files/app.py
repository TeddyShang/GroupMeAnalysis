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
        token = request.args.get('access_token')
        if token is None:
            return render_template('index.html')
        else:
            session['devToken'] = token
            return redirect(url_for('groups'))

@app.route('/groups', methods =['GET'])
def groups():
    token = session.get('devToken')
    c = cache.get(token)
    if c is not None and token is not None:
        return render_template('groups.html', groups=c)
    groups = main.getGroups(session.get('devToken'))
    if groups == None:
        return render_template('error.html', error='No groups found. Please login again')
    cache.set(token, groups, timeout = 5 * 60)
    return render_template('groups.html', groups=groups)


@app.route('/chatlog', methods=['POST'])
def chatlog():
    devToken = session.get('devToken')
    if devToken is None:
        return render_template('error.html', error='Error: Please login again')
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
    if devToken is None:
        return render_template('error.html', error='Error: Please login again')
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
    if devToken is None:
        return render_template('error.html', error='Error: Please login again')
    groupId = request.form['groupId']
    c = cache.get(groupId)
    m = main.getMemberInformation(groupId, devToken)
    if c is not None:
        ##calculate stats with cached log
        stats, gTotals = main.getStats(c)
        ##pass stats and memberInfo for share processing
        ms,lr,lg,sl = main.getShare(stats, m)
        ##pass chatlog to get timeline
        allTime, timeOfDay = main.getTimeline(c)
        return render_template('viz.html', stats=stats, memberInfo = m, gTotals=gTotals, chatlog = c, ms = ms,
                               lg=lg, lr = lr, sl = sl, allTime = allTime, timeOfDay = timeOfDay)
    ##otherwise get chatlog and get stats with it
    
    chatlog = main.getChatlog(groupId,devToken)
    cache.set(groupId, chatlog, timeout = 5 * 60)
    stats, gTotals = main.getStats(chatlog)

    main.getTimeline(chatlog)
    ##pass stats and memberInfo for share processing
    ms,lr,lg,sl = main.getShare(stats, m)
    ##pass chatlog to get timeline
    allTime, timeOfDay = main.getTimeline(chatlog)
    return render_template('viz.html', stats=stats, memberInfo = m, gTotals=gTotals, chatlog = c, ms = ms,
                               lg=lg, lr = lr, sl = sl, allTime = allTime, timeOfDay = timeOfDay)

@app.route('/info', methods=['GET'])
def info():
    return render_template('info.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')