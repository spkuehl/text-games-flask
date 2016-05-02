#!/usr/bin/env python

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on available packages.
from models import *

game = Game(1)

async_mode = None

if async_mode is None:
    try:
        import eventlet
        async_mode = 'eventlet'
    except ImportError:
        pass

    if async_mode is None:
        try:
            from gevent import monkey
            async_mode = 'gevent'
        except ImportError:
            pass

    if async_mode is None:
        async_mode = 'threading'

    print('async_mode is ' + async_mode)

# monkey patching is necessary because this application uses a background
# thread
if async_mode == 'eventlet':
    import eventlet
    eventlet.monkey_patch()
elif async_mode == 'gevent':
    from gevent import monkey
    monkey.patch_all()

import time
from threading import Thread
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        time.sleep(10)
        count += 1
        socketio.emit('my response',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/test')


@app.route('/')
def index():
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.daemon = True
        thread.start()
    return render_template('index.html')


@socketio.on('my event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.on('end round', namespace='/test')
def end_round():
    global game
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {
            'data': str(list(game.rounds[-1].entries.values())),
            'count': session['receive_count']},
        broadcast=True)
    game.end_round()

@socketio.on('end game', namespace='/test')
def end_game():
    global game
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
        {
            'data': str(list(game.end_game())),
            'count': session['receive_count']},
        broadcast=True)


@socketio.on('join', namespace='/test')
def join(message):
    global game
    game.add_player(message['room'])
    # session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': str(game.players),
          'count': len(game.players.values())})


@socketio.on('vote', namespace='/test')
def vote(message):
    global game
    game.rounds[-1].add_vote(int(message['vote']))
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'Vote received',
          'count': session['receive_count']})


@socketio.on('submit definition', namespace='/test')
def definition(message):
    player = game.players[int(message['player_id'])].player

    game.rounds[-1].add_entry(player, message['definition'])
    emit('my response', {'data': message['definition'],
                         'count': session['receive_count']})


@socketio.on('my room event', namespace='/test')
def send_room_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']},
         room=message['room'])


@socketio.on('disconnect request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()


@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


@socketio.on('new round', namespace='/test')
def new_round():
    global game
    game.new_round()
    emit('my response', {
        'data': game.rounds[-1].prompt.word,
        'count': session['receive_count']})

@socketio.on('start voting', namespace='/test')
def start_voting():
    global game
    options = str(game.rounds[-1].options)
    emit('my response', {
        'data': options,
        'count': session['receive_count']})


# @socketio.on('join game', namespace='/game')
# def join_game(message):





if __name__ == '__main__':
    socketio.run(app, debug=True)
