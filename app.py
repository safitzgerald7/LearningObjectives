#!/usr/bin/env python3
"""
Web interface for the Learning Objectives Generator
"""

from flask import Flask, request, render_template_string, jsonify
import sys
import os

# Add the current directory to Python path to import our generator
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from learning_objectives_generator import LearningObjectivesGenerator

app = Flask(__name__)

# HTML template for the web interface
HTML_TEMPLATE = '''
<!DOCTYPE html>
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
</html>
'''

@app.route('/')
def index():
    """Main page with the form"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/generate', methods=['POST'])
def generate_objectives():
    """API endpoint to generate learning objectives"""
    try:
        data = request.get_json()
        
        if not data or 'goal' not in data:
            return jsonify({
                'success': False,
                'error': 'No goal provided'
            }), 400
        
        goal = data['goal'].strip()
        
        if not goal:
            return jsonify({
                'success': False,
                'error': 'Goal cannot be empty'
            }), 400
        
        # Generate objectives using our existing generator
        generator = LearningObjectivesGenerator()
        result = generator.generate_learning_objectives(goal)
        
        return jsonify({
            'success': True,
            'result': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

# For deployment (Vercel, Heroku, etc.)
application = app

if __name__ == '__main__':
    print("🎯 Learning Objectives Generator Web App")
    print("=" * 50)
    print("Starting web server...")
    print("Open your browser and go to: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True)