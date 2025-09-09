#!/usr/bin/env python3
"""
Check database entries for form submissions
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Beneath_the_blue.settings')
django.setup()

from community.models import Pledge, Idea, Feedback, Question, Answer, Category, Community, Threat, Solution

def check_database():
    print("🌊 Beneath the Blue - Database Check 🌊")
    print("=" * 50)
    
    # Check Pledges
    pledges = Pledge.objects.all()
    print(f"📋 PLEDGES: {pledges.count()} entries")
    for pledge in pledges[:5]:  # Show first 5
        print(f"   - {pledge.name} ({pledge.email}) - {pledge.created_at}")
    
    # Check Ideas
    ideas = Idea.objects.all()
    print(f"💡 IDEAS: {ideas.count()} entries")
    for idea in ideas[:5]:  # Show first 5
        print(f"   - {idea.title} by {idea.name} ({idea.email}) - {idea.created_at}")
    
    # Check Feedback
    feedback = Feedback.objects.all()
    print(f"💭 FEEDBACK: {feedback.count()} entries")
    for fb in feedback[:5]:  # Show first 5
        print(f"   - Rating {fb.rating}/5 ({fb.feedback_type}) - {fb.created_at}")
    
    # Check Quiz Questions
    questions = Question.objects.all()
    print(f"❓ QUIZ QUESTIONS: {questions.count()} entries")
    for question in questions[:3]:  # Show first 3
        print(f"   - {question.text[:50]}...")
    
    # Check Categories and Communities
    categories = Category.objects.all()
    print(f"🏷️  CATEGORIES: {categories.count()} entries")
    for category in categories:
        communities = Community.objects.filter(category=category)
        print(f"   - {category.name}: {communities.count()} communities")
    
    # Check Threats and Solutions
    threats = Threat.objects.all()
    solutions = Solution.objects.all()
    print(f"⚠️  THREATS: {threats.count()} entries")
    print(f"✅ SOLUTIONS: {solutions.count()} entries")
    
    print("\n" + "=" * 50)
    if pledges.count() == 0 and ideas.count() == 0 and feedback.count() == 0:
        print("🔴 No form submissions found in database!")
        print("This means the homepage forms are not storing data properly.")
    else:
        print("✅ Form data is being stored in the database!")

if __name__ == "__main__":
    check_database()
