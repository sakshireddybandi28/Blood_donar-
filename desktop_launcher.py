import webview
import threading
from app import app
import time

def start_flask():
    # Run Flask on a fixed port
    app.run(port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    # Start Flask in a background thread
    t = threading.Thread(target=start_flask)
    t.daemon = True
    t.start()

    # Wait a moment for Flask to start
    time.sleep(2)

    # Create a native window pointing to the Flask app
    webview.create_window(
        'LifeStream - Blood Donation & Availability Tracker', 
        'http://127.0.0.1:5000',
        width=1200,
        height=800,
        resizable=True,
        icon='static/images/icon.png'
    )
    
    # Start the GUI
    webview.start()
