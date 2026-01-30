"""Simple web server for Railway deployment"""
import os
from flask import Flask, jsonify, request
from datetime import datetime
from collector import PropertyCollector
from scorer import DistressScorer
from emailer import Emailer
from config import DISTRESS_THRESHOLD

app = Flask(__name__)
collector = PropertyCollector()
scorer = DistressScorer()
emailer = Emailer()

@app.route('/')
def index():
    return jsonify({
        'status': 'running',
        'service': 'Distressed Seller MVP',
        'endpoints': {
            '/api/health': 'Health check',
            '/api/scan': 'Run property scan',
            '/api/leads': 'Get leads (min_score optional)',
            '/api/email': 'Send outreach email'
        }
    })

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})

@app.route('/api/scan', methods=['POST'])
def scan():
    """Run property scan and return scored leads"""
    try:
        properties = collector.batch_collect(max_per_zip=10)
        scored = scorer.score_all(properties)
        return jsonify({'count': len(scored), 'leads': scored[:50]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/leads')
def leads():
    """Get leads above threshold"""
    min_score = int(request.args.get('min_score', DISTRESS_THRESHOLD))
    # In production, fetch from database
    return jsonify({'min_score': min_score, 'leads': []})

@app.route('/api/email', methods=['POST'])
def send_email():
    """Send outreach email"""
    data = request.json
    success = emailer.send_outreach(
        data.get('to'),
        data.get('lead'),
        data.get('template', 'initial')
    )
    return jsonify({'success': success})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)