#!/usr/bin/env python3
"""
HealthCare Symptom Checker - Flask Backend Application
Main application file that handles HTTP requests and serves the symptom analysis API
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import logging
import os
from datetime import datetime
import json
from symptom_checker import SymptomChecker

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for frontend integration
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:5000", "http://localhost:5000"])

# Initialize symptom checker
symptom_checker = SymptomChecker()

@app.route('/')
def index():
    """Serve the main application page"""
    return render_template('index.html')

@app.route('/api/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'HealthCare Symptom Checker API',
        'version': '1.0.0'
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_symptoms():
    """
    Main endpoint for symptom analysis
    
    Expected JSON payload:
    {
        "age": int,
        "gender": str,
        "symptoms": str,
        "duration": str,
        "severity": str
    }
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No data provided',
                'message': 'Please provide symptom data in JSON format'
            }), 400
        
        # Validate required fields
        required_fields = ['age', 'gender', 'symptoms', 'duration', 'severity']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'error': 'Missing required fields',
                'missing_fields': missing_fields,
                'message': f'Please provide: {", ".join(missing_fields)}'
            }), 400
        
        # Validate data types and values
        validation_errors = validate_symptom_data(data)
        if validation_errors:
            return jsonify({
                'error': 'Validation failed',
                'validation_errors': validation_errors
            }), 400
        
        # Log the analysis request
        logger.info(f"Analyzing symptoms for {data['age']} year old {data['gender']}")
        logger.info(f"Symptoms: {data['symptoms'][:100]}...")
        
        # Perform symptom analysis
        analysis_result = symptom_checker.analyze_symptoms(
            age=data['age'],
            gender=data['gender'],
            symptoms=data['symptoms'],
            duration=data['duration'],
            severity=data['severity']
        )
        
        # Add metadata to response
        response_data = {
            'analysis_id': f"analysis_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            'timestamp': datetime.utcnow().isoformat(),
            'input_data': {
                'age': data['age'],
                'gender': data['gender'],
                'symptoms': data['symptoms'],
                'duration': data['duration'],
                'severity': data['severity']
            },
            **analysis_result
        }
        
        # Log successful analysis
        logger.info(f"Analysis completed successfully. ID: {response_data['analysis_id']}")
        
        return jsonify(response_data), 200
        
    except Exception as e:
        logger.error(f"Error during symptom analysis: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'Internal server error',
            'message': 'An error occurred while analyzing symptoms. Please try again.',
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@app.route('/api/symptoms/common', methods=['GET'])
def get_common_symptoms():
    """Get list of common symptoms for reference"""
    try:
        common_symptoms = symptom_checker.get_common_symptoms()
        return jsonify({
            'common_symptoms': common_symptoms,
            'count': len(common_symptoms)
        }), 200
    except Exception as e:
        logger.error(f"Error fetching common symptoms: {str(e)}")
        return jsonify({
            'error': 'Failed to fetch common symptoms'
        }), 500

@app.route('/api/conditions/search', methods=['GET'])
def search_conditions():
    """Search for medical conditions by keyword"""
    try:
        query = request.args.get('q', '').strip()
        
        if not query or len(query) < 2:
            return jsonify({
                'error': 'Invalid search query',
                'message': 'Search query must be at least 2 characters long'
            }), 400
        
        results = symptom_checker.search_conditions(query)
        
        return jsonify({
            'query': query,
            'results': results,
            'count': len(results)
        }), 200
        
    except Exception as e:
        logger.error(f"Error searching conditions: {str(e)}")
        return jsonify({
            'error': 'Failed to search conditions'
        }), 500

@app.route('/api/emergency/check', methods=['POST'])
def check_emergency():
    """Check if symptoms require immediate medical attention"""
    try:
        data = request.get_json()
        
        if not data or 'symptoms' not in data:
            return jsonify({
                'error': 'No symptoms provided'
            }), 400
        
        emergency_check = symptom_checker.check_emergency_symptoms(data['symptoms'])
        
        return jsonify({
            'is_emergency': emergency_check['is_emergency'],
            'urgency_level': emergency_check['urgency_level'],
            'warning_signs': emergency_check['warning_signs'],
            'recommendation': emergency_check['recommendation']
        }), 200
        
    except Exception as e:
        logger.error(f"Error checking emergency symptoms: {str(e)}")
        return jsonify({
            'error': 'Failed to check emergency symptoms'
        }), 500

@app.route('/api/analytics/summary', methods=['GET'])
def get_analytics_summary():
    """Get analytics summary (for admin/monitoring purposes)"""
    try:
        # This would typically connect to a database
        # For now, return mock data
        summary = {
            'total_analyses': 0,
            'analyses_today': 0,
            'most_common_symptoms': [],
            'average_response_time': '0.5s',
            'system_status': 'operational'
        }
        
        return jsonify(summary), 200
        
    except Exception as e:
        logger.error(f"Error fetching analytics: {str(e)}")
        return jsonify({
            'error': 'Failed to fetch analytics'
        }), 500

def validate_symptom_data(data):
    """
    Validate the symptom data received from the frontend
    
    Args:
        data (dict): The symptom data to validate
        
    Returns:
        list: List of validation errors (empty if valid)
    """
    errors = []
    
    # Validate age
    try:
        age = int(data['age'])
        if age < 1 or age > 120:
            errors.append("Age must be between 1 and 120")
    except (ValueError, TypeError):
        errors.append("Age must be a valid number")
    
    # Validate gender
    valid_genders = ['male', 'female', 'other']
    if data['gender'] not in valid_genders:
        errors.append(f"Gender must be one of: {', '.join(valid_genders)}")
    
    # Validate symptoms
    symptoms = str(data['symptoms']).strip()
    if len(symptoms) < 10:
        errors.append("Symptoms description must be at least 10 characters long")
    if len(symptoms) > 1000:
        errors.append("Symptoms description must be less than 1000 characters")
    
    # Validate duration
    valid_durations = [
        'less_than_24h', '1_3_days', '4_7_days', 
        '1_2_weeks', 'more_than_2_weeks'
    ]
    if data['duration'] not in valid_durations:
        errors.append(f"Duration must be one of: {', '.join(valid_durations)}")
    
    # Validate severity
    valid_severities = ['mild', 'moderate', 'severe']
    if data['severity'] not in valid_severities:
        errors.append(f"Severity must be one of: {', '.join(valid_severities)}")
    
    return errors

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'The requested endpoint does not exist',
        'available_endpoints': [
            '/api/health',
            '/api/analyze',
            '/api/symptoms/common',
            '/api/conditions/search',
            '/api/emergency/check',
            '/api/analytics/summary'
        ]
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        'error': 'Method not allowed',
        'message': 'The HTTP method is not supported for this endpoint'
    }), 405

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred. Please try again later.'
    }), 500

if __name__ == '__main__':
    # Configuration
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    
    logger.info(f"Starting HealthCare Symptom Checker API server...")
    logger.info(f"Debug mode: {debug_mode}")
    logger.info(f"Host: {host}")
    logger.info(f"Port: {port}")
    
    try:
        app.run(
            host=host,
            port=port,
            debug=debug_mode,
            threaded=True
        )
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        raise
