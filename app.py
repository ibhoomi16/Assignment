"""
Simple Flask Web Frontend for Project Planner
Run with: python project_planner_web.py
Then open: http://localhost:5000
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Import backend
from assignment import agent, load_history, save_history

load_dotenv()

app = Flask(__name__)

# Store conversation in memory for web session
conversations = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', 'default')
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Get or create conversation history
        if session_id not in conversations:
            conversations[session_id] = load_history()
        
        history = conversations[session_id]
        
        # Add user message
        history.append({"role": "user", "content": user_message})
        
        # Build context
        context = "\n".join(f"{m['role']}: {m['content']}" for m in history[-10:])
        
        # Get AI response
        response = agent.run(context, stream=False)
        reply = response.content if hasattr(response, "content") else str(response)
        
        # Add assistant message
        history.append({"role": "assistant", "content": reply})
        
        # Save history
        save_history(history)
        conversations[session_id] = history
        
        # Check if chart was generated
        chart_exists = os.path.exists("gantt_chart.png")
        
        return jsonify({
            'success': True,
            'reply': reply,
            'chart_available': chart_exists,
            'history': history
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chart')
def get_chart():
    """Serve the generated chart"""
    if os.path.exists("gantt_chart.png"):
        return send_file("gantt_chart.png", mimetype='image/png')
    return jsonify({'error': 'Chart not found'}), 404

@app.route('/api/clear', methods=['POST'])
def clear_history():
    """Clear chat history"""
    try:
        data = request.json
        session_id = data.get('session_id', 'default')
        
        conversations[session_id] = []
        save_history([])
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download')
def download_chart():
    """Download the chart"""
    if os.path.exists("gantt_chart.png"):
        return send_file(
            "gantt_chart.png",
            as_attachment=True,
            download_name=f"gantt_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        )
    return jsonify({'error': 'Chart not found'}), 404

if __name__ == '__main__':
    
    print("\n" + "="*60)
    print(" Starting Project Planner Web Server")
    
    app.run(debug=True, port=51100)