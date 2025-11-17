"""
Simple Flask web application for DevOps lab
This app demonstrates basic web functionality with some code quality issues
"""
import os
import random
import time
from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter, Histogram

app = Flask(__name__)
metrics = PrometheusMetrics(app)
visit_counter = Counter('app_visits_total', 'Número total de visitas')
calc_time = Histogram('calculate_duration_seconds', 'Tiempo de ejecución de /calculate')
error_counter = Counter('app_errors_total', 'Número total de errores')
request_latency = Histogram(
    'request_latency_seconds',
    'Latencia de las peticiones',
    ['endpoint']
)

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

@app.errorhandler(Exception)
def handle_exception(e):
    error_counter.inc()
    return jsonify({'error': str(e)}), 500

@app.before_request
def start_timer():
    request.start_time = time.time()
    visit_counter.inc()  # Incrementa métrica Prometheus en cada request

@app.after_request
def record_latency(response):
    # Introduce latencia aleatoria entre 1 y 3 segundos en cada request
    time.sleep(random.uniform(1, 3))
    latency = time.time() - request.start_time
    endpoint_name = request.endpoint if request.endpoint else request.path
    request_latency.labels(endpoint=endpoint_name).observe(latency)
    return response

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
    start = time.time()
    x = int(request.args.get('x', 5))
    y = int(request.args.get('y', 3))
    result = badFunction(x, y)
    # Introduce latencia aleatoria entre 1 y 3 segundos en cada request
    time.sleep(random.uniform(1, 3))
    calc_time.observe(time.time() - start)
    return jsonify({'result': result})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
