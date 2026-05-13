from flask import Blueprint, render_template, request, jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/contact', methods=['POST'])
def contact():
    # Simple mock contact handling
    data = request.form
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')
    
    print(f"New Message from {name} ({email}): {message}")
    
    return jsonify({"status": "success", "message": "¡Gracias por contactarme! Te responderé pronto."})

@main_bp.route('/quote', methods=['POST'])
def quote():
    # Mock quote handling
    data = request.get_json()
    services = data.get('services', [])
    complexity = data.get('complexity', 'Medium')
    estimated_total = data.get('total', 0)
    
    print(f"New Quote Request: Services: {services}, Complexity: {complexity}, Total: ${estimated_total}")
    
    return jsonify({"status": "success", "message": "Cotización recibida. Me pondré en contacto para discutir los detalles."})
