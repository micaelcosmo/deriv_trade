import logging
import asyncio
from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Thread

# Import bot components
from main import BotRunner
from logger import BotLogger

# --- Flask & Socket.IO Setup ---
app = Flask(__name__, template_folder='.')
app.config['SECRET_KEY'] = 'secret!'
# Use threading for async support (eventlet not installed)
socketio = SocketIO(app, async_mode='threading')

# --- Real-time Logging Handler ---
class SocketIOHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        # Broadcast log messages to all connected clients
        socketio.emit('log_message', {'data': log_entry})

# Get the root logger from our custom logger class and add the new handler
root_logger = BotLogger.get_logger('root')
socketio_handler = SocketIOHandler()
# Use the same formatter as the console/file handlers
formatter = logging.Formatter(
    fmt="%(asctime)s %(filename)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
socketio_handler.setFormatter(formatter)
root_logger.addHandler(socketio_handler)

# --- Bot Runner Thread ---
def run_bot_async():
    """Function to run the bot's async logic in a separate thread."""
    try:
        # Create a new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Pass the socketio instance to the bot
        bot = BotRunner(socketio=socketio)
        loop.run_until_complete(bot.run())
    except Exception as e:
        root_logger.critical(f"Erro fatal no thread do bot: {e}")

# --- Flask Routes ---
@app.route('/')
def index():
    """Render the main dashboard page."""
    return render_template('index.html')

# --- Socket.IO Events ---
@socketio.on('connect')
def handle_connect():
    """Handle new client connections."""
    root_logger.info('Cliente conectado ao painel.')

@socketio.on('start_bot')
def handle_start_bot():
    """Starts the bot logic in a background thread when requested by the client."""
    root_logger.info("Recebido comando para iniciar o bot...")
    # Run the bot in a separate thread to not block the web server
    thread = Thread(target=run_bot_async)
    thread.daemon = True
    thread.start()

if __name__ == '__main__':
    root_logger.info("Iniciando servidor Flask com Socket.IO.")
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)