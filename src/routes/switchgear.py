from flask import Blueprint, jsonify, request
import math
import json
from src.models.user import db
from src.models.switchgear import (
    Manufacturer, StartingMethod, Contactor, OverloadRelay, Motor
)

switchgear_bp = Blueprint('switchgear', __name__)

# Motor Selection Algorithm
def calculate_full_load_current(power_kw, voltage, power_factor=0.8, efficiency=0.9, phases=3):
    """Calculate Full Load Current using three-phase power formula"""
    power_watts = power_kw * 1000
    sqrt_3 = math.sqrt(3)
    flc = power_watts / (sqrt_3 * voltage * power_factor * efficiency)
    return round(flc, 2)

def get_compatible_starting_methods(motor_power_hp):
    """Return list of compatible starting methods based on motor power"""
    compatible_methods = []
    
    methods = StartingMethod.query.all()
    for method in methods:
        if (method.min_power_hp <= motor_power_hp <= method.max_power_hp):
            compatible_methods.append(method.to_dict())
    
    return compatible_methods

def select_best_contactor(min_current_rating, min_voltage_rating):
    """Query database for the most cost-effective contactor meeting requirements"""
    contactor = Contactor.query.filter(
        Contactor.current_rating >= min_current_rating,
        Contactor.voltage_rating >= min_voltage_rating
    ).order_by(Contactor.current_rating.asc(), Contactor.price.asc()).first()
    
    return contactor

def select_overload_relay(flc, contactor_frame_size):
    """Select overload relay with range covering FLC ± 20%"""
    lower_limit = flc * 0.8
    upper_limit = flc * 1.2
    
    # Query for suitable overload relays
    relays = OverloadRelay.query.filter(
        OverloadRelay.current_range_min <= lower_limit,
        OverloadRelay.current_range_max >= upper_limit
    ).order_by(OverloadRelay.price.asc()).all()
    
    # Filter by compatible frame size
    for relay in relays:
        compatible_frames = json.loads(relay.compatible_contactor_frames) if relay.compatible_contactor_frames else []
        if contactor_frame_size in compatible_frames or not compatible_frames:
            return relay
    
    # If no exact match, find closest range
    closest_relay = OverloadRelay.query.filter(
        OverloadRelay.current_range_min <= flc,
        OverloadRelay.current_range_max >= flc
    ).order_by(OverloadRelay.price.asc()).first()
    
    return closest_relay

def generate_contactors_for_starting_method(starting_method, circuit_breaker_rating, voltage):
    """Generate contactor recommendations based on starting method"""
    contactor_rating = circuit_breaker_rating
    
    if starting_method == 'DOL':
        main_contactor = select_best_contactor(contactor_rating, voltage)
        if not main_contactor:
            return None
            
        return {
            'main_contactor': main_contactor.to_dict(),
            'quantity': 1,
            'total_cost': main_contactor.price
        }
    
    elif starting_method == 'Star-Delta':
        main_contactor = select_best_contactor(contactor_rating, voltage)
        if not main_contactor:
            return None
            
        # Star and Delta contactors can be smaller (typically 58% of main)
        star_delta_rating = contactor_rating * 0.58
        star_contactor = select_best_contactor(star_delta_rating, voltage)
        delta_contactor = select_best_contactor(star_delta_rating, voltage)
        
        if not star_contactor or not delta_contactor:
            return None
            
        total_cost = main_contactor.price + star_contactor.price + delta_contactor.price
        
        return {
            'main_contactor': main_contactor.to_dict(),
            'star_contactor': star_contactor.to_dict(),
            'delta_contactor': delta_contactor.to_dict(),
            'quantity': 3,
            'total_cost': total_cost
        }
    
    elif starting_method in ['Soft Starter', 'VFD']:
        bypass_contactor = select_best_contactor(contactor_rating, voltage)
        if not bypass_contactor:
            return None
            
        return {
            'bypass_contactor': bypass_contactor.to_dict(),
            'quantity': 1,
            'total_cost': bypass_contactor.price
        }
    
    return None

def generate_component_list(contactors, overload_relay, starting_method):
    """Generate detailed component list with quantities and prices"""
    components = []
    
    if starting_method == 'DOL':
        components.append({
            'component': 'Main Contactor',
            'model': contactors['main_contactor']['model'],
            'manufacturer': contactors['main_contactor']['manufacturer'],
            'quantity': 1,
            'unit_price': contactors['main_contactor']['price'],
            'total_price': contactors['main_contactor']['price']
        })
    
    elif starting_method == 'Star-Delta':
        components.extend([
            {
                'component': 'Main Contactor',
                'model': contactors['main_contactor']['model'],
                'manufacturer': contactors['main_contactor']['manufacturer'],
                'quantity': 1,
                'unit_price': contactors['main_contactor']['price'],
                'total_price': contactors['main_contactor']['price']
            },
            {
                'component': 'Star Contactor',
                'model': contactors['star_contactor']['model'],
                'manufacturer': contactors['star_contactor']['manufacturer'],
                'quantity': 1,
                'unit_price': contactors['star_contactor']['price'],
                'total_price': contactors['star_contactor']['price']
            },
            {
                'component': 'Delta Contactor',
                'model': contactors['delta_contactor']['model'],
                'manufacturer': contactors['delta_contactor']['manufacturer'],
                'quantity': 1,
                'unit_price': contactors['delta_contactor']['price'],
                'total_price': contactors['delta_contactor']['price']
            }
        ])
    
    elif starting_method in ['Soft Starter', 'VFD']:
        component_name = 'Bypass Contactor' if starting_method == 'Soft Starter' else 'Input Contactor'
        components.append({
            'component': component_name,
            'model': contactors['bypass_contactor']['model'],
            'manufacturer': contactors['bypass_contactor']['manufacturer'],
            'quantity': 1,
            'unit_price': contactors['bypass_contactor']['price'],
            'total_price': contactors['bypass_contactor']['price']
        })
    
    # Add overload relay
    if overload_relay:
        components.append({
            'component': 'Overload Relay',
            'model': overload_relay.model,
            'manufacturer': overload_relay.manufacturer,
            'quantity': 1,
            'unit_price': overload_relay.price,
            'total_price': overload_relay.price
        })
    
    return components

# API Endpoints

@switchgear_bp.route('/calculate', methods=['POST', 'OPTIONS'])
def calculate_recommendation():
    """Main endpoint for motor switchgear selection calculation"""
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        data = request.json
        
        # Validate input
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract and validate motor specifications
        motor_power_hp = data.get('motor_power_hp')
        motor_power_kw = data.get('motor_power_kw')
        voltage = data.get('voltage', 415)
        frequency = data.get('frequency', 50)
        starting_method = data.get('starting_method')
        power_factor = data.get('power_factor', 0.8)
        efficiency = data.get('efficiency', 0.9)
        
        # Convert between HP and kW if needed
        if motor_power_hp and not motor_power_kw:
            motor_power_kw = motor_power_hp * 0.746
        elif motor_power_kw and not motor_power_hp:
            motor_power_hp = motor_power_kw / 0.746
        elif not motor_power_hp and not motor_power_kw:
            return jsonify({'error': 'Motor power must be specified in HP or kW'}), 400
        
        if not starting_method:
            return jsonify({'error': 'Starting method must be specified'}), 400
        
        # Check starting method compatibility
        compatible_methods = get_compatible_starting_methods(motor_power_hp)
        compatible_method_names = [method['name'] for method in compatible_methods]
        
        if starting_method not in compatible_method_names:
            return jsonify({
                'error': f"Starting method '{starting_method}' not suitable for {motor_power_hp} HP motor",
                'compatible_methods': compatible_methods
            }), 400
        
        # Calculate Full Load Current
        flc = calculate_full_load_current(motor_power_kw, voltage, power_factor, efficiency)
        
        # Calculate circuit breaker rating (FLC × 1.5)
        circuit_breaker_rating = round(flc * 1.5, 2)
        
        # Select contactors based on starting method
        contactors = generate_contactors_for_starting_method(starting_method, circuit_breaker_rating, voltage)
        
        if not contactors:
            return jsonify({'error': 'No suitable contactors found for the specified requirements'}), 404
        
        # Select overload relay
        main_contactor = (contactors.get('main_contactor') or 
                         contactors.get('bypass_contactor') or 
                         contactors.get('input_contactor'))
        
        if main_contactor:
            overload_relay = select_overload_relay(flc, main_contactor.get('frame_size', ''))
        else:
            overload_relay = None
        
        # Calculate total cost
        total_cost = contactors['total_cost']
        if overload_relay:
            total_cost += overload_relay.price
        
        # Generate component list
        component_list = generate_component_list(contactors, overload_relay, starting_method)
        
        # Generate recommendation response
        recommendation = {
            'motor_specifications': {
                'power_hp': round(motor_power_hp, 1),
                'power_kw': round(motor_power_kw, 2),
                'voltage': voltage,
                'frequency': frequency,
                'full_load_current': flc,
                'power_factor': power_factor,
                'efficiency': efficiency
            },
            'starting_method': starting_method,
            'circuit_breaker_rating': circuit_breaker_rating,
            'contactors': contactors,
            'overload_relay': overload_relay.to_dict() if overload_relay else None,
            'total_cost': round(total_cost, 2),
            'component_list': component_list,
            'compatible_starting_methods': compatible_methods
        }
        
        return jsonify(recommendation), 200
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@switchgear_bp.route('/starting-methods', methods=['GET'])
def get_starting_methods():
    """Get all available starting methods"""
    methods = StartingMethod.query.all()
    return jsonify([method.to_dict() for method in methods])

@switchgear_bp.route('/starting-methods/<float:power_hp>', methods=['GET'])
def get_compatible_starting_methods_for_power(power_hp):
    """Get compatible starting methods for a specific motor power"""
    compatible_methods = get_compatible_starting_methods(power_hp)
    return jsonify(compatible_methods)

@switchgear_bp.route('/contactors', methods=['GET'])
def get_contactors():
    """Get all contactors with optional filtering"""
    min_current = request.args.get('min_current', type=float)
    max_current = request.args.get('max_current', type=float)
    voltage = request.args.get('voltage', type=int)
    manufacturer = request.args.get('manufacturer')
    
    query = Contactor.query
    
    if min_current:
        query = query.filter(Contactor.current_rating >= min_current)
    if max_current:
        query = query.filter(Contactor.current_rating <= max_current)
    if voltage:
        query = query.filter(Contactor.voltage_rating >= voltage)
    if manufacturer:
        query = query.filter(Contactor.manufacturer.ilike(f'%{manufacturer}%'))
    
    contactors = query.order_by(Contactor.current_rating.asc()).all()
    return jsonify([contactor.to_dict() for contactor in contactors])

@switchgear_bp.route('/overload-relays', methods=['GET'])
def get_overload_relays():
    """Get all overload relays with optional filtering"""
    min_current = request.args.get('min_current', type=float)
    max_current = request.args.get('max_current', type=float)
    manufacturer = request.args.get('manufacturer')
    
    query = OverloadRelay.query
    
    if min_current:
        query = query.filter(OverloadRelay.current_range_min <= min_current)
    if max_current:
        query = query.filter(OverloadRelay.current_range_max >= max_current)
    if manufacturer:
        query = query.filter(OverloadRelay.manufacturer.ilike(f'%{manufacturer}%'))
    
    relays = query.order_by(OverloadRelay.current_range_min.asc()).all()
    return jsonify([relay.to_dict() for relay in relays])

@switchgear_bp.route('/manufacturers', methods=['GET'])
def get_manufacturers():
    """Get all manufacturers"""
    manufacturers = Manufacturer.query.all()
    return jsonify([manufacturer.to_dict() for manufacturer in manufacturers])

@switchgear_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Motor Switchgear Selection API',
        'version': '1.0.0'
    })

