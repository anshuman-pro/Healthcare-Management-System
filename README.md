# HealthCare Symptom Checker Portal

A comprehensive, AI-powered healthcare symptom checker portal that provides intelligent health insights and recommendations based on user-reported symptoms. Built with modern web technologies and powered by Python backend with machine learning capabilities.

## 🏥 Project Overview

The HealthCare Symptom Checker Portal is designed to help users understand their symptoms and receive personalized health recommendations. While not a substitute for professional medical advice, it serves as a valuable tool for initial symptom assessment and health education.

### Key Features

- **Intelligent Symptom Analysis**: AI-powered symptom processing and condition identification
- **Emergency Detection**: Automatic identification of symptoms requiring immediate medical attention
- **Personalized Recommendations**: Tailored health advice based on age, gender, and symptom severity
- **Responsive Design**: Modern, mobile-friendly user interface
- **Real-time Processing**: Instant analysis and results delivery
- **Comprehensive Medical Database**: Extensive knowledge base covering multiple medical categories

## 🏗️ Architecture

### Frontend
- **HTML5**: Semantic markup with accessibility features
- **CSS3**: Modern styling with responsive design and animations
- **JavaScript (ES6+)**: Interactive functionality and API communication

### Backend
- **Python 3.8+**: Core application logic
- **Flask**: Web framework for API endpoints
- **Machine Learning**: Symptom analysis and pattern recognition
- **Medical Knowledge Base**: Comprehensive condition and symptom database

### Data Flow
```
User Input → Frontend Validation → Backend API → Symptom Analysis → Results Display
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Node.js (optional, for development tools)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/healthcare-symptom-checker.git
   cd healthcare-symptom-checker
   ```

2. **Set up Python environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the backend server**
   ```bash
   python app.py
   ```

5. **Open the frontend**
   - Navigate to `index.html` in your web browser
   - Or serve it using a local web server

### Alternative Setup with Python HTTP Server

```bash
# Start Python HTTP server for frontend
python -m http.server 8000

# Start Flask backend (in another terminal)
python app.py
```

Then open `http://localhost:8000` in your browser.

## 📖 Usage Guide

### 1. Symptom Input

1. **Fill in personal information**:
   - Age (1-120 years)
   - Gender (Male/Female/Other)

2. **Describe your symptoms**:
   - Provide detailed description (minimum 10 characters)
   - Include location, intensity, and any triggers

3. **Specify duration**:
   - Less than 24 hours
   - 1-3 days
   - 4-7 days
   - 1-2 weeks
   - More than 2 weeks

4. **Rate severity**:
   - Mild: Noticeable but not interfering with daily activities
   - Moderate: Somewhat interfering with daily activities
   - Severe: Significantly interfering with daily activities

### 2. Analysis Results

The system provides:

- **Summary**: Overview of analysis findings
- **Possible Conditions**: Identified medical conditions
- **Recommended Actions**: Immediate steps to take
- **Emergency Warnings**: Critical symptoms requiring urgent care
- **Self-Care Tips**: Home treatment recommendations
- **When to Seek Care**: Guidelines for medical consultation

### 3. Result Actions

- **Save Results**: Store analysis for future reference
- **Check New Symptoms**: Reset form for new analysis
- **Export**: Download results as PDF (future feature)

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Flask Configuration
FLASK_DEBUG=True
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

# Database Configuration (if using database)
DATABASE_URL=postgresql://user:password@localhost/healthcare_db

# API Keys (for external services)
OPENAI_API_KEY=your_openai_api_key
MEDICAL_API_KEY=your_medical_api_key

# Security
SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_key
```

### Backend Configuration

Modify `app.py` for custom settings:

```python
# CORS origins
CORS(app, origins=["http://localhost:3000", "https://yourdomain.com"])

# Logging level
logging.basicConfig(level=logging.INFO)

# Server configuration
app.run(host='0.0.0.0', port=5000, debug=True)
```

## 🧠 Symptom Analysis Engine

### How It Works

1. **Text Processing**: Natural language processing of symptom descriptions
2. **Pattern Recognition**: Identification of symptom patterns and combinations
3. **Medical Knowledge Base**: Matching symptoms against comprehensive medical database
4. **Risk Assessment**: Evaluation of urgency and risk factors
5. **Recommendation Generation**: Personalized health advice and actions

### Medical Categories Covered

- **Respiratory**: Cold, flu, bronchitis, pneumonia, asthma
- **Gastrointestinal**: Food poisoning, gastritis, gastroenteritis, IBS
- **Neurological**: Migraines, headaches, dizziness, confusion
- **Cardiovascular**: Chest pain, shortness of breath, irregular heartbeat
- **Musculoskeletal**: Pain, swelling, stiffness, limited mobility
- **Dermatological**: Rashes, itching, redness, infections

### Emergency Detection

The system automatically identifies symptoms requiring immediate medical attention:

- **Critical**: Chest pain, difficulty breathing, severe bleeding
- **Urgent**: High fever, severe pain, sudden weakness
- **Warning**: Persistent symptoms, unexplained changes

## 🔒 Security & Privacy

### Data Protection

- **No Personal Storage**: Symptom data is not permanently stored
- **Local Processing**: Analysis performed locally when possible
- **Encrypted Communication**: HTTPS for all data transmission
- **Access Control**: Rate limiting and request validation

### Medical Disclaimer

⚠️ **Important**: This tool is for informational purposes only and should not replace professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare providers for medical concerns.

## 🧪 Testing

### Backend Testing

```bash
# Install test dependencies
pip install pytest pytest-flask

# Run tests
pytest

# Run with coverage
pytest --cov=app --cov=symptom_checker
```

### Frontend Testing

```bash
# Manual testing
# Open browser developer tools and check console for errors

# Automated testing (future implementation)
npm test
```

## 📊 API Documentation

### Endpoints

#### POST `/api/analyze`
Main symptom analysis endpoint.

**Request Body:**
```json
{
  "age": 30,
  "gender": "female",
  "symptoms": "I have been experiencing headache and nausea for the past 2 days",
  "duration": "1_3_days",
  "severity": "moderate"
}
```

**Response:**
```json
{
  "analysis_id": "analysis_20241201_143022",
  "timestamp": "2024-12-01T14:30:22.123456",
  "summary": "Analysis suggests possible Migraine with Moderate symptoms",
  "possible_conditions": ["Migraine", "Tension Headache"],
  "recommended_actions": ["Consider seeking medical attention today"],
  "emergency_warnings": [],
  "confidence_level": "Medium",
  "risk_assessment": "Medium"
}
```

#### GET `/api/health`
Health check endpoint for monitoring.

#### GET `/api/symptoms/common`
Get list of common symptoms.

#### GET `/api/conditions/search?q=query`
Search medical conditions by keyword.

#### POST `/api/emergency/check`
Check if symptoms require emergency care.

## 🚀 Deployment

### Production Deployment

1. **Set up production server**
   ```bash
   # Install production dependencies
   pip install gunicorn waitress
   
   # Set environment variables
   export FLASK_DEBUG=False
   export FLASK_HOST=0.0.0.0
   export FLASK_PORT=5000
   ```

2. **Use production WSGI server**
   ```bash
   # With Gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   
   # With Waitress (Windows)
   waitress-serve --host=0.0.0.0 --port=5000 app:app
   ```

3. **Set up reverse proxy (Nginx/Apache)**
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 🔮 Future Enhancements

### Planned Features

- **Machine Learning Integration**: Enhanced symptom analysis with neural networks
- **Image Analysis**: Support for photo-based symptom assessment
- **Multi-language Support**: Internationalization for global users
- **Mobile App**: Native iOS and Android applications
- **Telemedicine Integration**: Direct connection to healthcare providers
- **Health Records**: Secure storage and management of health data
- **Predictive Analytics**: Trend analysis and health predictions

### AI Improvements

- **Natural Language Understanding**: Better symptom interpretation
- **Context Awareness**: Understanding symptom relationships
- **Learning System**: Continuous improvement from user feedback
- **Personalization**: User-specific health insights and recommendations

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### Code Style

- **Python**: Follow PEP 8 guidelines
- **JavaScript**: Use ES6+ features and consistent formatting
- **CSS**: Follow BEM methodology for class naming
- **HTML**: Semantic markup with accessibility considerations

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Getting Help

- **Documentation**: Check this README and inline code comments
- **Issues**: Report bugs and feature requests on GitHub
- **Discussions**: Join community discussions for questions and ideas

### Contact

- **Email**: support@healthcare-checker.com
- **GitHub**: [Project Issues](https://github.com/yourusername/healthcare-symptom-checker/issues)
- **Documentation**: [Wiki](https://github.com/yourusername/healthcare-symptom-checker/wiki)

## 🙏 Acknowledgments

- Medical professionals who provided domain expertise
- Open-source community for tools and libraries
- Users who provided feedback and testing
- Healthcare organizations for best practices and guidelines

---

**Remember**: This tool is designed to complement, not replace, professional medical care. Always consult with qualified healthcare providers for medical concerns.

**Last Updated**: December 2024
**Version**: 1.0.0
