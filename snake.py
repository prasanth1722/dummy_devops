import pygame
import random
import os
from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
import json

# Initialize pygame in headless mode
os.environ['SDL_VIDEODRIVER'] = 'dummy'
pygame.init()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Game Constants
WIDTH = 600
HEIGHT = 400
SNAKE_BLOCK = 10
SNAKE_SPEED = 15

# Game State
snake = []
food = []
current_direction = "RIGHT"
game_over = False
clients = set()

def init_game():
    global snake, food, current_direction, game_over
    snake = [[WIDTH//2, HEIGHT//2]]
    food = [
        random.randrange(0, WIDTH-SNAKE_BLOCK, SNAKE_BLOCK),
        random.randrange(0, HEIGHT-SNAKE_BLOCK, SNAKE_BLOCK)
    ]
    current_direction = "RIGHT"
    game_over = False

def game_loop():
    global snake, food, current_direction, game_over
    
    while True:
        if not clients:  # Pause game when no players
            pygame.time.wait(100)
            continue
            
        if game_over:
            pygame.time.wait(100)
            continue
            
        # Move snake
        head = snake[0].copy()
        if current_direction == "LEFT":
            head[0] -= SNAKE_BLOCK
        elif current_direction == "RIGHT":
            head[0] += SNAKE_BLOCK
        elif current_direction == "UP":
            head[1] -= SNAKE_BLOCK
        elif current_direction == "DOWN":
            head[1] += SNAKE_BLOCK
        
        # Check collisions
        if (head[0] >= WIDTH or head[0] < 0 or 
            head[1] >= HEIGHT or head[1] < 0 or
            head in snake):
            game_over = True
            continue
            
        snake.insert(0, head)
        
        # Check food
        if head == food:
            food = [
                random.randrange(0, WIDTH-SNAKE_BLOCK, SNAKE_BLOCK),
                random.randrange(0, HEIGHT-SNAKE_BLOCK, SNAKE_BLOCK)
            ]
        else:
            snake.pop()
        
        pygame.time.delay(int(1000/SNAKE_SPEED))

# Initialize game
init_game()
threading.Thread(target=game_loop, daemon=True).start()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    clients.add(request.sid)
    if len(clients) == 1:  # First player resets game
        init_game()

@socketio.on('disconnect')
def handle_disconnect():
    clients.discard(request.sid)

@socketio.on('keypress')
def handle_keypress(data):
    global current_direction, game_over
    
    key = data.get('key')
    
    if key == ' ' and game_over:
        init_game()
        return
        
    if game_over:
        return
        
    key_mapping = {
        'ArrowLeft': 'LEFT',
        'ArrowRight': 'RIGHT',
        'ArrowUp': 'UP',
        'ArrowDown': 'DOWN'
    }
    
    new_dir = key_mapping.get(key)
    if new_dir and (
        (new_dir == "LEFT" and current_direction != "RIGHT") or
        (new_dir == "RIGHT" and current_direction != "LEFT") or
        (new_dir == "UP" and current_direction != "DOWN") or
        (new_dir == "DOWN" and current_direction != "UP")):
        current_direction = new_dir

def broadcast_state():
    while True:
        if clients:
            state = {
                "snake": snake,
                "food": food,
                "game_over": game_over,
                "score": len(snake) - 1
            }
            socketio.emit('game_state', state)
        socketio.sleep(0.1)

threading.Thread(target=broadcast_state, daemon=True).start()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    # Critical settings for Cloud Run:
    socketio.run(app,
                host='0.0.0.0',
                port=port,
                allow_unsafe_werkzeug=True,  # Required for Cloud Run
                debug=False,
                use_reloader=False)
