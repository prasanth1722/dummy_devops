import pygame
import random
import os
from flask import Flask, Response, request
import json

# Initialize pygame in headless mode
os.environ['SDL_VIDEODRIVER'] = 'dummy'
pygame.init()

app = Flask(__name__)

# Game Constants
WIDTH = 600
HEIGHT = 400
SNAKE_BLOCK = 10
SNAKE_SPEED = 15

# Game State
game_state = {
    "snake": [[WIDTH/2, HEIGHT/2]],
    "food": [random.randrange(0, WIDTH-SNAKE_BLOCK, SNAKE_BLOCK), 
             random.randrange(0, HEIGHT-SNAKE_BLOCK, SNAKE_BLOCK)],
    "direction": "RIGHT",
    "game_over": False
}

@app.route('/')
def game_ui():
    """Simple HTML UI for the game"""
    return """
    <html>
    <body>
    <h1>Snake Game</h1>
    <div id="game"></div>
    <script>
    function updateGame() {
        fetch('/state').then(r => r.json()).then(data => {
            document.getElementById('game').innerHTML = 
                `Score: ${data.snake.length}<br>
                ${data.game_over ? 'GAME OVER' : ''}`;
        });
        setTimeout(updateGame, 100);
    }
    document.onkeydown = (e) => {
        fetch('/move', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({key: e.key})
        });
    };
    updateGame();
    </script>
    </body>
    </html>
    """

@app.route('/state')
def get_state():
    """Return current game state"""
    return json.dumps(game_state)

@app.route('/move', methods=['POST'])
def handle_move():
    """Process keyboard input"""
    global game_state
    if game_state["game_over"]:
        return "Game Over"
    
    key = request.json.get('key', '')
    
    # Update direction
    if key == "ArrowLeft" and game_state["direction"] != "RIGHT":
        game_state["direction"] = "LEFT"
    elif key == "ArrowRight" and game_state["direction"] != "LEFT":
        game_state["direction"] = "RIGHT"
    elif key == "ArrowUp" and game_state["direction"] != "DOWN":
        game_state["direction"] = "UP"
    elif key == "ArrowDown" and game_state["direction"] != "UP":
        game_state["direction"] = "DOWN"
    elif key == " " and game_state["game_over"]:  # Space to restart
        reset_game()
    
    return "OK"

def reset_game():
    """Reset game state"""
    global game_state
    game_state = {
        "snake": [[WIDTH/2, HEIGHT/2]],
        "food": [random.randrange(0, WIDTH-SNAKE_BLOCK, SNAKE_BLOCK), 
                 random.randrange(0, HEIGHT-SNAKE_BLOCK, SNAKE_BLOCK)],
        "direction": "RIGHT",
        "game_over": False
    }

def update_game():
    """Update game logic"""
    global game_state
    
    if game_state["game_over"]:
        return
    
    head = game_state["snake"][0].copy()
    
    # Move snake
    if game_state["direction"] == "LEFT":
        head[0] -= SNAKE_BLOCK
    elif game_state["direction"] == "RIGHT":
        head[0] += SNAKE_BLOCK
    elif game_state["direction"] == "UP":
        head[1] -= SNAKE_BLOCK
    elif game_state["direction"] == "DOWN":
        head[1] += SNAKE_BLOCK
    
    # Check collisions
    if (head[0] >= WIDTH or head[0] < 0 or 
        head[1] >= HEIGHT or head[1] < 0 or
        head in game_state["snake"]):
        game_state["game_over"] = True
        return
    
    game_state["snake"].insert(0, head)
    
    # Check food
    if head == game_state["food"]:
        game_state["food"] = [
            random.randrange(0, WIDTH-SNAKE_BLOCK, SNAKE_BLOCK),
            random.randrange(0, HEIGHT-SNAKE_BLOCK, SNAKE_BLOCK)
        ]
    else:
        game_state["snake"].pop()

# Background game updater
import threading
def game_loop():
    import time
    while True:
        update_game()
        time.sleep(1/SNAKE_SPEED)

threading.Thread(target=game_loop, daemon=True).start()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
