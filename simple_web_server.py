#!/usr/bin/env python3
"""
Simple web server for the Learning Objectives Generator
Uses only Python standard library - no external dependencies required
"""

import http.server
import socketserver
import json
import urllib.parse
from pathlib import Path
import sys
import os

# Add the current directory to Python path to import our generator
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from learning_objectives_generator import LearningObjectivesGenerator

# HTML template for the web interface
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Learning Objectives Generator</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
            line-height: 1.6;
        }
        
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 10px;
        }
        
        .subtitle {
            text-align: center;
            color: #7f8c8d;
            margin-bottom: 30px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #34495e;
        }
        
        textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
            resize: vertical;
            min-height: 100px;
            box-sizing: border-box;
        }
        
        textarea:focus {
            border-color: #3498db;
            outline: none;
        }
        
        button {
            background-color: #3498db;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        
        button:hover {
            background-color: #2980b9;
        }
        
        button:disabled {
            background-color: #95a5a6;
            cursor: not-allowed;
        }
        
        .results {
            margin-top: 30px;
            padding: 20px;
            background-color: #ecf0f1;
            border-radius: 5px;
            border-left: 4px solid #3498db;
        }
        
        .results h3 {
            color: #2c3e50;
            margin-top: 0;
        }
        
        .goal-info {
            background-color: #e8f5e8;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 15px;
        }
        
        .objectives {
            background-color: white;
            padding: 15px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            white-space: pre-line;
            line-height: 1.5;
        }
        
        .loading {
            text-align: center;
            color: #7f8c8d;
        }
        
        .error {
            background-color: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #dc3545;
        }
        
        .examples {
            margin-top: 20px;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 5px;
        }
        
        .examples h4 {
            margin-top: 0;
            color: #495057;
        }
        
        .example {
            margin: 10px 0;
            padding: 8px;
            background-color: white;
            border-radius: 3px;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        
        .example:hover {
            background-color: #e9ecef;
        }
        
        .bloom-levels {
            margin-top: 20px;
            font-size: 14px;
            color: #6c757d;
        }
        
        .bloom-levels h4 {
            margin-bottom: 10px;
            color: #495057;
        }
        
        .bloom-level {
            margin: 5px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 Learning Objectives Generator</h1>
        <p class="subtitle">Generate clear learning objectives aligned to Bloom's Taxonomy</p>
        
        <form id="objectiveForm">
            <div class="form-group">
                <label for="goal">Enter your course goal:</label>
                <textarea 
                    id="goal" 
                    name="goal" 
                    placeholder="Example: The goal is for learners to know the supplies needed for each emergency procedure"
                    required
                ></textarea>
            </div>
            
            <button type="submit" id="generateBtn">Generate Learning Objectives</button>
        </form>
        
        <div class="examples">
            <h4>📚 Example Goals (click to use):</h4>
            <div class="example" onclick="setGoal('The goal is for learners to know the supplies needed for each emergency procedure')">
                Emergency procedure supplies
            </div>
            <div class="example" onclick="setGoal('Students will design a user interface for a mobile application')">
                UI design for mobile apps
            </div>
            <div class="example" onclick="setGoal('Students will create a marketing plan for a new product')">
                Marketing plan development
            </div>
            <div class="example" onclick="setGoal('Learners will analyze data to identify trends and patterns')">
                Data analysis and pattern recognition
            </div>
        </div>
        
        <div class="bloom-levels">
            <h4>🧠 Bloom's Taxonomy Levels:</h4>
            <div class="bloom-level"><strong>Remember:</strong> Recall facts and basic concepts</div>
            <div class="bloom-level"><strong>Understand:</strong> Explain ideas or concepts</div>
            <div class="bloom-level"><strong>Apply:</strong> Use information in new situations</div>
            <div class="bloom-level"><strong>Analyze:</strong> Draw connections among ideas</div>
            <div class="bloom-level"><strong>Evaluate:</strong> Justify a stand or decision</div>
            <div class="bloom-level"><strong>Create:</strong> Produce new or original work</div>
        </div>
        
        <div id="results" style="display: none;"></div>
    </div>

    <script>
        function setGoal(goalText) {
            document.getElementById('goal').value = goalText;
        }
        
        document.getElementById('objectiveForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const goal = document.getElementById('goal').value.trim();
            const generateBtn = document.getElementById('generateBtn');
            const resultsDiv = document.getElementById('results');
            
            if (!goal) {
                alert('Please enter a course goal.');
                return;
            }
            
            // Show loading state
            generateBtn.disabled = true;
            generateBtn.textContent = 'Generating...';
            resultsDiv.style.display = 'block';
            resultsDiv.innerHTML = '<div class="loading">🔄 Generating learning objectives...</div>';
            
            try {
                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ goal: goal })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    resultsDiv.innerHTML = `
                        <div class="results">
                            <h3>📋 Generated Learning Objectives</h3>
                            <div class="goal-info">
                                <strong>Original Goal:</strong> ${data.result.goal}<br>
                                <strong>Target Bloom's Level:</strong> ${data.result.target_level_name.charAt(0).toUpperCase() + data.result.target_level_name.slice(1)} (Level ${data.result.target_level})
                            </div>
                            <div class="objectives">${data.result.formatted_output}</div>
                        </div>
                    `;
                } else {
                    resultsDiv.innerHTML = `
                        <div class="error">
                            <strong>Error:</strong> ${data.error}
                        </div>
                    `;
                }
            } catch (error) {
                resultsDiv.innerHTML = `
                    <div class="error">
                        <strong>Error:</strong> Failed to generate objectives. Please try again.
                    </div>
                `;
            } finally {
                generateBtn.disabled = false;
                generateBtn.textContent = 'Generate Learning Objectives';
            }
        });
    </script>
</body>
</html>'''

class LearningObjectivesHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP request handler for the learning objectives generator"""
    
    def __init__(self, *args, **kwargs):
        self.generator = LearningObjectivesGenerator()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode('utf-8'))
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = json.dumps({'status': 'healthy'})
            self.wfile.write(response.encode('utf-8'))
        else:
            self.send_error(404, "File not found")
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/api/generate':
            try:
                # Read the request body
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                
                # Parse JSON data
                data = json.loads(post_data.decode('utf-8'))
                
                if 'goal' not in data:
                    self.send_error(400, "No goal provided")
                    return
                
                goal = data['goal'].strip()
                
                if not goal:
                    self.send_error(400, "Goal cannot be empty")
                    return
                
                # Generate objectives
                result = self.generator.generate_learning_objectives(goal)
                
                # Send successful response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                response = json.dumps({
                    'success': True,
                    'result': result
                })
                self.wfile.write(response.encode('utf-8'))
                
            except json.JSONDecodeError:
                self.send_error(400, "Invalid JSON data")
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                response = json.dumps({
                    'success': False,
                    'error': str(e)
                })
                self.wfile.write(response.encode('utf-8'))
        else:
            self.send_error(404, "Endpoint not found")

def main():
    """Start the web server"""
    PORT = 8080
    
    print("🎯 Learning Objectives Generator Web Interface")
    print("=" * 50)
    print("Starting web server...")
    print(f"Open your browser and go to: http://localhost:{PORT}")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        with socketserver.TCPServer(("", PORT), LearningObjectivesHandler) as httpd:
            print(f"Server running on port {PORT}")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"Error starting server: {e}")

if __name__ == "__main__":
    main()