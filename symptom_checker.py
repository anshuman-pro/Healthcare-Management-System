#!/usr/bin/env python3
"""
HealthCare Symptom Checker - Core Analysis Module
Implements symptom analysis logic, medical knowledge base, and intelligent recommendations
"""

import re
import logging
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import json

# Configure logging
logger = logging.getLogger(__name__)

class SymptomChecker:
    """
    Core symptom analysis engine that processes user input and provides health insights
    """
    
    def __init__(self):
        """Initialize the symptom checker with medical knowledge base"""
        self.medical_knowledge = self._initialize_medical_knowledge()
        self.symptom_patterns = self._initialize_symptom_patterns()
        self.emergency_keywords = self._initialize_emergency_keywords()
        self.condition_database = self._initialize_condition_database()
        
        logger.info("SymptomChecker initialized with medical knowledge base")
    
    def _initialize_medical_knowledge(self) -> Dict:
        """Initialize the medical knowledge base with common conditions and symptoms"""
        return {
            'respiratory': {
                'conditions': ['Common Cold', 'Flu', 'Bronchitis', 'Pneumonia', 'Asthma'],
                'symptoms': ['cough', 'sore throat', 'runny nose', 'congestion', 'shortness of breath', 'wheezing'],
                'severity_factors': ['fever', 'chest pain', 'difficulty breathing']
            },
            'gastrointestinal': {
                'conditions': ['Food Poisoning', 'Gastritis', 'Gastroenteritis', 'Irritable Bowel Syndrome'],
                'symptoms': ['nausea', 'vomiting', 'diarrhea', 'abdominal pain', 'bloating', 'loss of appetite'],
                'severity_factors': ['severe pain', 'blood in stool', 'dehydration']
            },
            'neurological': {
                'conditions': ['Migraine', 'Tension Headache', 'Cluster Headache', 'Concussion'],
                'symptoms': ['headache', 'dizziness', 'nausea', 'sensitivity to light', 'confusion'],
                'severity_factors': ['severe pain', 'loss of consciousness', 'numbness']
            },
            'cardiovascular': {
                'conditions': ['Hypertension', 'Angina', 'Heart Attack', 'Arrhythmia'],
                'symptoms': ['chest pain', 'shortness of breath', 'fatigue', 'dizziness', 'irregular heartbeat'],
                'severity_factors': ['severe chest pain', 'pain radiating to arm', 'sweating']
            },
            'musculoskeletal': {
                'conditions': ['Sprain', 'Strain', 'Arthritis', 'Fracture', 'Muscle Pain'],
                'symptoms': ['pain', 'swelling', 'stiffness', 'limited range of motion', 'bruising'],
                'severity_factors': ['severe pain', 'deformity', 'inability to move']
            },
            'dermatological': {
                'conditions': ['Rash', 'Eczema', 'Psoriasis', 'Allergic Reaction', 'Infection'],
                'symptoms': ['rash', 'itching', 'redness', 'swelling', 'blisters'],
                'severity_factors': ['severe itching', 'fever', 'spreading rash']
            }
        }
    
    def _initialize_symptom_patterns(self) -> Dict[str, List[str]]:
        """Initialize patterns for symptom recognition and categorization"""
        return {
            'fever_patterns': [
                r'\b(?:high|low|mild|moderate|severe)\s+(?:fever|temperature)\b',
                r'\b(?:fever|temperature)\s+(?:above|over|under)\s+\d+',
                r'\b(?:fever|temperature)\s+(?:for|lasting)\s+\d+\s+(?:hours|days|weeks)'
            ],
            'pain_patterns': [
                r'\b(?:sharp|dull|throbbing|aching|stabbing|burning)\s+(?:pain)\b',
                r'\b(?:pain)\s+(?:in|on|around)\s+(?:head|chest|abdomen|back|leg|arm)',
                r'\b(?:severe|moderate|mild)\s+(?:pain)\b'
            ],
            'duration_patterns': [
                r'\b(?:for|lasting|since|over)\s+(\d+)\s+(?:hours?|days?|weeks?|months?)\b',
                r'\b(?:started|began|developed)\s+(?:yesterday|today|last\s+week)\b'
            ]
        }
    
    def _initialize_emergency_keywords(self) -> Dict[str, List[str]]:
        """Initialize emergency symptom keywords for urgent care identification"""
        return {
            'critical': [
                'chest pain', 'difficulty breathing', 'severe bleeding', 'loss of consciousness',
                'numbness', 'paralysis', 'severe head injury', 'severe abdominal pain'
            ],
            'urgent': [
                'high fever', 'severe pain', 'sudden weakness', 'vision changes',
                'severe allergic reaction', 'poisoning', 'suicidal thoughts'
            ],
            'warning': [
                'persistent vomiting', 'severe dehydration', 'unexplained weight loss',
                'persistent cough', 'blood in stool', 'severe headache'
            ]
        }
    
    def _initialize_condition_database(self) -> Dict[str, Dict]:
        """Initialize database of medical conditions with symptoms and treatments"""
        return {
            'Common Cold': {
                'symptoms': ['runny nose', 'congestion', 'sneezing', 'sore throat', 'cough'],
                'duration': '3-7 days',
                'severity': 'mild',
                'treatments': ['rest', 'fluids', 'over-the-counter medications'],
                'when_to_seek_care': 'if symptoms persist beyond 10 days or worsen'
            },
            'Influenza': {
                'symptoms': ['fever', 'body aches', 'fatigue', 'headache', 'cough', 'sore throat'],
                'duration': '1-2 weeks',
                'severity': 'moderate',
                'treatments': ['rest', 'fluids', 'antiviral medications if prescribed'],
                'when_to_seek_care': 'if high fever, difficulty breathing, or severe symptoms'
            },
            'Migraine': {
                'symptoms': ['severe headache', 'nausea', 'sensitivity to light', 'aura'],
                'duration': '4-72 hours',
                'severity': 'moderate to severe',
                'treatments': ['pain medications', 'rest in dark room', 'avoid triggers'],
                'when_to_seek_care': 'if headache is worst ever, with fever or confusion'
            },
            'Gastroenteritis': {
                'symptoms': ['nausea', 'vomiting', 'diarrhea', 'abdominal cramps', 'fever'],
                'duration': '1-3 days',
                'severity': 'mild to moderate',
                'treatments': ['rest', 'clear fluids', 'bland diet', 'rehydration'],
                'when_to_seek_care': 'if severe dehydration, blood in stool, or persistent vomiting'
            }
        }
    
    def analyze_symptoms(self, age: int, gender: str, symptoms: str, 
                        duration: str, severity: str) -> Dict:
        """
        Main method to analyze symptoms and provide health insights
        
        Args:
            age: Patient age
            gender: Patient gender
            symptoms: Description of symptoms
            duration: Duration of symptoms
            severity: Severity level
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            logger.info(f"Analyzing symptoms for {age} year old {gender}")
            
            # Normalize and process symptoms
            normalized_symptoms = self._normalize_symptoms(symptoms.lower())
            
            # Check for emergency symptoms first
            emergency_check = self.check_emergency_symptoms(symptoms)
            
            # Analyze symptom patterns
            symptom_analysis = self._analyze_symptom_patterns(normalized_symptoms, duration, severity)
            
            # Identify possible conditions
            possible_conditions = self._identify_conditions(normalized_symptoms, age, gender)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                possible_conditions, severity, duration, emergency_check
            )
            
            # Create summary
            summary = self._create_summary(possible_conditions, severity, emergency_check)
            
            # Compile results
            results = {
                'summary': summary,
                'possible_conditions': possible_conditions,
                'recommended_actions': recommendations['actions'],
                'emergency_warnings': recommendations['emergency_warnings'],
                'self_care_tips': recommendations['self_care'],
                'when_to_seek_care': recommendations['when_to_seek_care'],
                'confidence_level': self._calculate_confidence(possible_conditions, symptoms),
                'risk_assessment': self._assess_risk(age, severity, emergency_check),
                'follow_up_recommendations': recommendations['follow_up']
            }
            
            logger.info(f"Symptom analysis completed. Found {len(possible_conditions)} possible conditions")
            return results
            
        except Exception as e:
            logger.error(f"Error in symptom analysis: {str(e)}", exc_info=True)
            raise
    
    def _normalize_symptoms(self, symptoms: str) -> List[str]:
        """Normalize and extract individual symptoms from text"""
        # Remove common words and punctuation
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        
        # Split into words and clean
        words = re.findall(r'\b\w+\b', symptoms)
        cleaned_words = [word for word in words if word.lower() not in stop_words and len(word) > 2]
        
        # Group related symptoms
        symptom_groups = []
        current_group = []
        
        for word in cleaned_words:
            if self._is_symptom_word(word):
                if current_group:
                    symptom_groups.append(' '.join(current_group))
                    current_group = []
                current_group = [word]
            else:
                current_group.append(word)
        
        if current_group:
            symptom_groups.append(' '.join(current_group))
        
        return symptom_groups if symptom_groups else cleaned_words
    
    def _is_symptom_word(self, word: str) -> bool:
        """Check if a word is likely a symptom"""
        symptom_indicators = [
            'pain', 'ache', 'fever', 'cough', 'sneeze', 'rash', 'swell', 'nausea',
            'vomit', 'diarrhea', 'headache', 'dizziness', 'fatigue', 'weakness'
        ]
        return any(indicator in word.lower() for indicator in symptom_indicators)
    
    def _analyze_symptom_patterns(self, symptoms: List[str], duration: str, severity: str) -> Dict:
        """Analyze patterns in symptoms for better understanding"""
        analysis = {
            'symptom_count': len(symptoms),
            'duration_category': duration,
            'severity_level': severity,
            'pattern_matches': {}
        }
        
        # Check for fever patterns
        for symptom in symptoms:
            for pattern in self.symptom_patterns['fever_patterns']:
                if re.search(pattern, symptom, re.IGNORECASE):
                    analysis['pattern_matches']['fever'] = True
                    break
        
        # Check for pain patterns
        for symptom in symptoms:
            for pattern in self.symptom_patterns['pain_patterns']:
                if re.search(pattern, symptom, re.IGNORECASE):
                    analysis['pattern_matches']['pain'] = True
                    break
        
        return analysis
    
    def _identify_conditions(self, symptoms: List[str], age: int, gender: str) -> List[str]:
        """Identify possible medical conditions based on symptoms"""
        possible_conditions = []
        symptom_scores = {}
        
        # Score each condition based on symptom matches
        for category, data in self.medical_knowledge.items():
            for condition in data['conditions']:
                score = 0
                for symptom in symptoms:
                    if symptom in data['symptoms']:
                        score += 1
                    # Check for partial matches
                    for known_symptom in data['symptoms']:
                        if symptom in known_symptom or known_symptom in symptom:
                            score += 0.5
                
                if score > 0:
                    symptom_scores[condition] = score
        
        # Sort by score and return top matches
        sorted_conditions = sorted(symptom_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Return conditions with significant symptom matches
        for condition, score in sorted_conditions:
            if score >= 1.0:  # At least one exact symptom match
                possible_conditions.append(condition)
        
        # Limit to top 5 conditions
        return possible_conditions[:5]
    
    def _generate_recommendations(self, conditions: List[str], severity: str, 
                                 duration: str, emergency_check: Dict) -> Dict:
        """Generate personalized health recommendations"""
        recommendations = {
            'actions': [],
            'emergency_warnings': [],
            'self_care': [],
            'when_to_seek_care': [],
            'follow_up': []
        }
        
        # Emergency warnings
        if emergency_check['is_emergency']:
            recommendations['emergency_warnings'].append(
                "⚠️ SEEK IMMEDIATE MEDICAL ATTENTION - These symptoms may require emergency care"
            )
            recommendations['actions'].append("Call emergency services or go to nearest emergency room")
        
        # Self-care recommendations based on conditions
        for condition in conditions:
            if condition in self.condition_database:
                condition_info = self.condition_database[condition]
                recommendations['self_care'].extend(condition_info['treatments'])
                recommendations['when_to_seek_care'].append(condition_info['when_to_seek_care'])
        
        # General recommendations based on severity and duration
        if severity == 'severe':
            recommendations['actions'].append("Consider seeking medical attention today")
        elif severity == 'moderate' and duration in ['4_7_days', '1_2_weeks', 'more_than_2_weeks']:
            recommendations['actions'].append("Schedule an appointment with your healthcare provider")
        
        # Duration-based recommendations
        if duration == 'more_than_2_weeks':
            recommendations['actions'].append("Persistent symptoms may require medical evaluation")
        
        # General self-care tips
        recommendations['self_care'].extend([
            "Get adequate rest",
            "Stay hydrated",
            "Monitor symptoms for changes",
            "Avoid known triggers or irritants"
        ])
        
        # Follow-up recommendations
        recommendations['follow_up'].append("Monitor symptoms and seek care if they worsen")
        if conditions:
            recommendations['follow_up'].append(f"Follow up with healthcare provider about {conditions[0]}")
        
        # Remove duplicates
        for key in recommendations:
            recommendations[key] = list(set(recommendations[key]))
        
        return recommendations
    
    def _create_summary(self, conditions: List[str], severity: str, emergency_check: Dict) -> str:
        """Create a human-readable summary of the analysis"""
        if emergency_check['is_emergency']:
            return "🚨 EMERGENCY: Immediate medical attention required"
        
        if not conditions:
            return "Symptoms analyzed but no specific conditions identified. Consider consulting a healthcare provider."
        
        condition_text = conditions[0] if len(conditions) == 1 else f"{', '.join(conditions[:-1])} and {conditions[-1]}"
        severity_text = severity.capitalize()
        
        return f"Analysis suggests possible {condition_text} with {severity_text} symptoms"
    
    def _calculate_confidence(self, conditions: List[str], symptoms: str) -> str:
        """Calculate confidence level of the analysis"""
        if not conditions:
            return "Low"
        
        symptom_length = len(symptoms.split())
        condition_count = len(conditions)
        
        if symptom_length > 20 and condition_count <= 2:
            return "High"
        elif symptom_length > 10 and condition_count <= 3:
            return "Medium"
        else:
            return "Low"
    
    def _assess_risk(self, age: int, severity: str, emergency_check: Dict) -> str:
        """Assess overall risk level"""
        if emergency_check['is_emergency']:
            return "Critical"
        
        risk_factors = 0
        
        # Age-based risk
        if age < 5 or age > 65:
            risk_factors += 1
        
        # Severity-based risk
        if severity == 'severe':
            risk_factors += 2
        elif severity == 'moderate':
            risk_factors += 1
        
        if risk_factors >= 3:
            return "High"
        elif risk_factors >= 1:
            return "Medium"
        else:
            return "Low"
    
    def check_emergency_symptoms(self, symptoms: str) -> Dict:
        """Check if symptoms require immediate medical attention"""
        symptoms_lower = symptoms.lower()
        emergency_found = False
        urgency_level = "low"
        warning_signs = []
        
        # Check for critical symptoms
        for symptom in self.emergency_keywords['critical']:
            if symptom in symptoms_lower:
                emergency_found = True
                urgency_level = "critical"
                warning_signs.append(f"Critical: {symptom}")
        
        # Check for urgent symptoms
        if not emergency_found:
            for symptom in self.emergency_keywords['urgent']:
                if symptom in symptoms_lower:
                    emergency_found = True
                    urgency_level = "urgent"
                    warning_signs.append(f"Urgent: {symptom}")
        
        # Check for warning signs
        for symptom in self.emergency_keywords['warning']:
            if symptom in symptoms_lower:
                warning_signs.append(f"Warning: {symptom}")
        
        # Determine recommendation
        if urgency_level == "critical":
            recommendation = "Call emergency services immediately or go to nearest emergency room"
        elif urgency_level == "urgent":
            recommendation = "Seek medical attention within 24 hours"
        else:
            recommendation = "Monitor symptoms and seek care if they worsen"
        
        return {
            'is_emergency': emergency_found,
            'urgency_level': urgency_level,
            'warning_signs': warning_signs,
            'recommendation': recommendation
        }
    
    def get_common_symptoms(self) -> List[str]:
        """Get list of common symptoms for reference"""
        all_symptoms = []
        for category_data in self.medical_knowledge.values():
            all_symptoms.extend(category_data['symptoms'])
        return sorted(list(set(all_symptoms)))
    
    def search_conditions(self, query: str) -> List[Dict]:
        """Search for medical conditions by keyword"""
        query_lower = query.lower()
        results = []
        
        for condition_name, condition_data in self.condition_database.items():
            if query_lower in condition_name.lower():
                results.append({
                    'name': condition_name,
                    'symptoms': condition_data['symptoms'],
                    'severity': condition_data['severity']
                })
        
        # Also search in medical knowledge base
        for category, data in self.medical_knowledge.items():
            for condition in data['conditions']:
                if query_lower in condition.lower():
                    results.append({
                        'name': condition,
                        'category': category,
                        'symptoms': data['symptoms']
                    })
        
        return results[:10]  # Limit results
    
    def get_health_tips(self, condition: str = None) -> List[str]:
        """Get general health tips or condition-specific advice"""
        general_tips = [
            "Maintain a healthy diet and regular exercise routine",
            "Get adequate sleep (7-9 hours per night)",
            "Stay hydrated by drinking plenty of water",
            "Practice good hygiene and handwashing",
            "Schedule regular check-ups with your healthcare provider",
            "Avoid smoking and limit alcohol consumption",
            "Manage stress through relaxation techniques"
        ]
        
        if condition and condition in self.condition_database:
            condition_tips = self.condition_database[condition]['treatments']
            return condition_tips + general_tips
        
        return general_tips
