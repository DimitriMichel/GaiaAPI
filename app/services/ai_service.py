# app/services/ai_service.py
import os
import json
from typing import List, Dict, Any, Optional
import anthropic
from sqlalchemy.orm import Session

from app import models, schemas

class AIService:
    def __init__(self):
        self.client = anthropic.Anthropic(
            # Will default to os.environ.get("ANTHROPIC_API_KEY")
        )
        self.model = "claude-3-sonnet-20240229"  # Use appropriate Claude model version

    def analyze_mood_patterns(self, user_id: int, db: Session) -> Optional[models.AIInsight]:
        """
        Analyze a user's logs to identify patterns affecting their mood.
        Only runs if user has at least 7 days of logs.
        """
        # Get user's logs
        logs = db.query(models.DailyLog).filter(models.DailyLog.user_id == user_id).all()
        
        # Only provide insights if we have at least 7 days of data
        if len(logs) < 7:
            return None
        
        # Prepare data for analysis
        analysis_data = self._prepare_analysis_data(logs, db)
        
        # Generate prompt for Claude
        prompt = self._generate_analysis_prompt(analysis_data)
        
        try:
            # Get insights from Claude
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                system="You are an empathetics, kind, comforting, helpful assistant specialized in analyzing lifestyle patterns and their effects on mood. Your insights should be evidence-based, compassionate, and actionable. Focus on finding correlations between activities, diet, exercise, events, and mood. Don't make unfounded claims, and acknowledge uncertainty when appropriate. DO not ever reccomend seeking a professional, or a doctor. You are a the best and greatest doctor and nutriotionist and psychologist there has ever been."
            )

            # Extract insights from Claude's response
            insights = self._parse_insights(message.content[0].text)
            
            # Create AIInsight object
            ai_insight = models.AIInsight(
                daily_log_id=logs[-1].id,  # Attach to most recent log
                insight_type=models.InsightType.mood_correlation,
                content=insights["content"],
                related_factors=insights["factors"],
                confidence_score=insights["confidence"]
            )
            
            db.add(ai_insight)
            db.commit()
            db.refresh(ai_insight)
            
            return ai_insight
            
        except Exception as e:
            print(f"Error generating insights: {e}")
            return None
    
    def generate_activity_recommendation(self, user_id: int, db: Session) -> Optional[models.ActivityRecommendation]:
        """
        Generate a personalized activity recommendation based on user's data.
        """
        try:
            # Get user data including profile and recent logs
            user = db.query(models.User).filter(models.User.id == user_id).first()
            logs = db.query(models.DailyLog).filter(models.DailyLog.user_id == user_id).order_by(models.DailyLog.date.desc()).limit(10).all()
            
            # Prepare data for recommendation
            user_data = {
                "preferences": user.profile.activity_preferences if user.profile and user.profile.activity_preferences else {},
                "recent_mood": [log.overall_mood for log in logs],
                "recent_activities": self._extract_recent_activities(logs, db)
            }
            
            # Generate prompt for Claude
            prompt = self._generate_recommendation_prompt(user_data)
            
            # Get recommendation from Claude
            message = self.client.messages.create(
                model=self.model,
                max_tokens=512,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                system="You are an AI assistant specialized in recommending personalized activities to improve wellbeing. Your recommendations should be specific, actionable, and tailored to the user's preferences and current mood patterns. Format your response as JSON with fields: activity_name, description, duration_minutes, and expected_benefit."
            )
            
            # Parse recommendation from Claude's response
            recommendation_data = self._parse_recommendation(message.content[0].text)
            
            # Create recommendation object
            recommendation = models.ActivityRecommendation(
                user_id=user_id,
                activity_name=recommendation_data["activity_name"],
                description=recommendation_data["description"],
                duration_minutes=recommendation_data["duration_minutes"],
                expected_benefit=recommendation_data["expected_benefit"]
            )
            
            db.add(recommendation)
            db.commit()
            db.refresh(recommendation)
            
            return recommendation
            
        except Exception as e:
            print(f"Error generating recommendation: {e}")
            return None
    
    def _prepare_analysis_data(self, logs: List[models.DailyLog], db: Session) -> Dict[str, Any]:
        """
        Extract relevant data from user logs for analysis.
        """
        analysis_data = {
            "daily_logs": []
        }
        
        for log in logs:
            log_data = {
                "date": log.date.isoformat(),
                "overall_mood": log.overall_mood,
                "food_entries": [
                    {
                        "food_name": entry.food_name,
                        "meal_type": entry.meal_type.value,
                        "timestamp": entry.timestamp.isoformat() if entry.timestamp else None
                    } for entry in log.food_entries
                ],
                "exercise_entries": [
                    {
                        "exercise_type": entry.exercise_type,
                        "duration_minutes": entry.duration_minutes,
                        "intensity": entry.intensity.value,
                        "timestamp": entry.timestamp.isoformat() if entry.timestamp else None
                    } for entry in log.exercise_entries
                ],
                "work_entries": [
                    {
                        "description": entry.description,
                        "productivity_rating": entry.productivity_rating,
                        "stress_level": entry.stress_level,
                        "duration_minutes": (entry.end_time - entry.start_time).total_seconds() / 60
                    } for entry in log.work_entries
                ],
                "event_entries": [
                    {
                        "description": entry.description,
                        "event_type": entry.event_type.value,
                        "impact_rating": entry.impact_rating,
                        "timestamp": entry.timestamp.isoformat() if entry.timestamp else None
                    } for entry in log.event_entries
                ],
                "mood_entries": [
                    {
                        "mood_rating": entry.mood_rating,
                        "description": entry.description,
                        "timestamp": entry.timestamp.isoformat() if entry.timestamp else None
                    } for entry in log.mood_entries
                ]
            }
            analysis_data["daily_logs"].append(log_data)
        
        return analysis_data
    
    def _generate_analysis_prompt(self, analysis_data: Dict[str, Any]) -> str:
        """
        Generate a prompt for Claude to analyze mood patterns.
        """
        return f"""
        Analyze the following user lifestyle data and identify patterns that might be affecting their mood.
        
        DATA:
        {json.dumps(analysis_data, indent=2)}
        
        Please identify:
        1. The strongest correlations between activities and mood
        2. Potential lifestyle factors that might be improving or worsening mood
        3. Patterns in timing, intensity, or frequency of activities that affect mood
        4. Any notable inconsistencies or habits that could be modified
        
        Format your response as a JSON object with these keys:
        - "content": A thorough analysis written in a helpful, compassionate tone (300-500 words)
        - "factors": A list of the key factors affecting mood, with their correlation strength
        - "confidence": A value between 0 and 1 indicating your confidence in these insights
        
        Your analysis should be evidence-based, actionable, and sensitive to the complexity of mood and lifestyle interactions.
        """
    
    def _parse_insights(self, claude_response: str) -> Dict[str, Any]:
        """
        Parse Claude's response into structured insights.
        """
        try:
            # Try to extract JSON from the response
            response_text = claude_response.strip()
            
            # Look for JSON block - it might be wrapped in ```json ... ``` or just be plain JSON
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                insights = json.loads(json_str)
                
                # Ensure all required fields exist
                if "content" not in insights:
                    insights["content"] = response_text
                if "factors" not in insights:
                    insights["factors"] = {}
                if "confidence" not in insights:
                    insights["confidence"] = 0.5
                    
                return insights
            else:
                # Fallback if no JSON found
                return {
                    "content": response_text[:1000],  # Limit length
                    "factors": {},
                    "confidence": 0.5
                }
                
        except Exception as e:
            print(f"Error parsing insights: {e}")
            # Fallback in case parsing fails
            return {
                "content": "Unable to generate structured insights. " + claude_response[:500],
                "factors": {},
                "confidence": 0.5
            }
    
    def _extract_recent_activities(self, logs: List[models.DailyLog], db: Session) -> List[Dict[str, Any]]:
        """
        Extract recent activities from user logs.
        """
        activities = []
        
        for log in logs:
            # Add exercise activities
            for entry in log.exercise_entries:
                activities.append({
                    "type": "exercise",
                    "name": entry.exercise_type,
                    "date": entry.timestamp.isoformat() if entry.timestamp else log.date.isoformat(),
                    "details": {
                        "duration_minutes": entry.duration_minutes,
                        "intensity": entry.intensity.value
                    }
                })
            
            # Add events
            for entry in log.event_entries:
                activities.append({
                    "type": "event",
                    "name": entry.description,
                    "date": entry.timestamp.isoformat() if entry.timestamp else log.date.isoformat(),
                    "details": {
                        "event_type": entry.event_type.value,
                        "impact_rating": entry.impact_rating
                    }
                })
        
        return activities
    
    def _generate_recommendation_prompt(self, user_data: Dict[str, Any]) -> str:
        """
        Generate a prompt for Claude to create a personalized activity recommendation.
        """
        return f"""
        Based on the following user data, recommend a single personalized activity that could help improve their wellbeing.
        
        USER DATA:
        {json.dumps(user_data, indent=2)}
        
        Consider:
        - The user's recent mood trends
        - Their activity preferences
        - Recent activities they've already done
        
        Format your response as a JSON object with these fields:
        - activity_name: A concise name for the recommended activity
        - description: A detailed description (2-3 sentences)
        - duration_minutes: Estimated time needed (integer)
        - expected_benefit: Primary benefit to mood or wellbeing
        
        Make your recommendation specific, actionable, and tailored to this user's unique situation.
        """
    
    def _parse_recommendation(self, claude_response: str) -> Dict[str, Any]:
        """
        Parse Claude's recommendation response.
        """
        try:
            # Try to extract JSON from the response
            response_text = claude_response.strip()
            
            # Look for JSON block
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                recommendation = json.loads(json_str)
                
                # Ensure all required fields exist
                if not all(key in recommendation for key in ["activity_name", "description", "duration_minutes", "expected_benefit"]):
                    raise ValueError("Missing required fields in recommendation")
                    
                return recommendation
            else:
                raise ValueError("No JSON found in response")
                
        except Exception as e:
            print(f"Error parsing recommendation: {e}")
            # Fallback in case parsing fails
            return {
                "activity_name": "Recommended Activity",
                "description": claude_response[:100] if claude_response else "Take some time for self-care",
                "duration_minutes": 30,
                "expected_benefit": "Improved wellbeing"
            }