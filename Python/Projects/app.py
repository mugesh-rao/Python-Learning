from flask import Flask, render_template, jsonify, request, session
import random

app = Flask(__name__)
app.secret_key = 'my_secret_key'  # Required for session management

# Predefined list of words for the game
WORDS = ["python", "flask", "hangman", "developer", "coding"]

# Function to start a new game
def start_new_game():
    word = random.choice(WORDS)
    session['word'] = word
    session['guessed_letters'] = []
    session['attempts_left'] = 7
    return word

# Helper to get the current state of the word with hidden letters
def get_word_display():
    word = session['word']
    guessed_letters = session['guessed_letters']
    return ''.join([letter if letter in guessed_letters else '_' for letter in word])

@app.route('/')
def index():
    start_new_game()  # Start a new game session
    return render_template('index.html')

@app.route('/new_game', methods=['POST'])
def new_game():
    word = start_new_game()
    return jsonify({
        "word_display": get_word_display(),
        "attempts_left": session['attempts_left']
    })

@app.route('/guess', methods=['POST'])
def guess():
    guess_letter = request.json.get('letter', '').lower()
    if not guess_letter or len(guess_letter) != 1 or not guess_letter.isalpha():
        return jsonify({"error": "Invalid input."}), 400
    
    word = session['word']
    guessed_letters = session['guessed_letters']
    
    if guess_letter in guessed_letters:
        return jsonify({"error": "Already guessed."}), 400
    
    guessed_letters.append(guess_letter)
    session['guessed_letters'] = guessed_letters
    
    if guess_letter not in word:
        session['attempts_left'] -= 1
    
    word_display = get_word_display()
    attempts_left = session['attempts_left']
    game_status = "ongoing"
    
    if "_" not in word_display:
        game_status = "win"
    elif attempts_left <= 0:
        game_status = "lose"
    
    return jsonify({
        "word_display": word_display,
        "attempts_left": attempts_left,
        "game_status": game_status
    })

if __name__ == '__main__':
    app.run(debug=True)
