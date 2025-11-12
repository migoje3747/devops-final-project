"""
Simple Flask web application for DevOps lab
This app demonstrates basic web functionality with some code quality issues
"""
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# Global variable (pylint will flag this)
counter = 0

@app.route('/')
def hello_world():
    """Main endpoint that returns a greeting"""
    global counter
    counter += 1
    return jsonify({
        'message': 'Hello from DevOps Lab!',
        'version': '1.0.0',
        'environment': os.environ.get('ENVIRONMENT', 'development'),
        'visits': counter
    })

@app.route('/health')
def health_check():
    """Health check endpoint for load balancer"""
    return jsonify({'status': 'healthy', 'service': 'flask-app'})

@app.route('/info')
def get_info():
    """Returns application information"""
    return jsonify({
        'app_name': 'DevOps Lab App',
        'python_version': '3.11',
        'framework': 'Flask'
    })

# Bad function (has code quality issues for demonstration)
def badFunction(x, y):  # pylint will flag: function name should be snake_case
    """This function has intentional quality issues"""
    z = x + y  # unused variable warning
    if x > 10:
        if y > 10:  # nested if (complexity issue)
            result = x * y
        else:
            result = x + y
    else:
        result = 0
    return result

@app.route('/calculate')
def calculate():
    """Endpoint that uses the bad function"""
    x = int(request.args.get('x', 5))
    y = int(request.args.get('y', 3))
    result = badFunction(x, y)
    return jsonify({'result': result})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)