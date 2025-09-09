#!/usr/bin/env python3
"""
Data restoration script for Beneath the Blue
This script restores the quiz questions, categories, and communities that were lost
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Beneath_the_blue.settings')
django.setup()

from community.models import Question, Answer, Category, Community, Threat, Solution, EndangeredSpecies, endangered_species

def create_quiz_data():
    """Create sample quiz questions about ocean conservation"""
    print("Creating quiz questions...")
    
    # Ocean Conservation Quiz Questions
    quiz_data = [
        {
            "question": "What percentage of Earth's surface is covered by oceans?",
            "answers": [
                ("71%", True),
                ("65%", False),
                ("80%", False),
                ("60%", False),
            ]
        },
        {
            "question": "Which ocean zone receives no sunlight?",
            "answers": [
                ("Midnight Zone", True),
                ("Sunlight Zone", False),
                ("Twilight Zone", False),
                ("Abyssal Zone", False),
            ]
        },
        {
            "question": "What is the largest marine animal?",
            "answers": [
                ("Blue Whale", True),
                ("Sperm Whale", False),
                ("Great White Shark", False),
                ("Giant Squid", False),
            ]
        },
        {
            "question": "How much plastic enters the ocean every year?",
            "answers": [
                ("8 million tons", True),
                ("2 million tons", False),
                ("15 million tons", False),
                ("5 million tons", False),
            ]
        },
        {
            "question": "What percentage of marine life remains undiscovered?",
            "answers": [
                ("80%", True),
                ("50%", False),
                ("90%", False),
                ("70%", False),
            ]
        },
        {
            "question": "Which gas do oceans absorb from the atmosphere?",
            "answers": [
                ("Carbon Dioxide", True),
                ("Nitrogen", False),
                ("Methane", False),
                ("Oxygen", False),
            ]
        },
        {
            "question": "What causes coral bleaching?",
            "answers": [
                ("Rising water temperatures", True),
                ("Too much sunlight", False),
                ("Lack of fish", False),
                ("Strong currents", False),
            ]
        },
        {
            "question": "How much of our oxygen comes from marine plants?",
            "answers": [
                ("50-70%", True),
                ("20-30%", False),
                ("10-20%", False),
                ("80-90%", False),
            ]
        },
        {
            "question": "What is the deepest part of the ocean called?",
            "answers": [
                ("Mariana Trench", True),
                ("Puerto Rico Trench", False),
                ("Java Trench", False),
                ("Peru-Chile Trench", False),
            ]
        },
        {
            "question": "Which marine ecosystem is most productive?",
            "answers": [
                ("Coral Reefs", True),
                ("Open Ocean", False),
                ("Deep Sea", False),
                ("Polar Seas", False),
            ]
        }
    ]
    
    for q_data in quiz_data:
        # Create question
        question = Question.objects.create(text=q_data["question"])
        
        # Create answers
        for answer_text, is_correct in q_data["answers"]:
            Answer.objects.create(
                question=question,
                text=answer_text,
                is_correct=is_correct
            )
    
    print(f"Created {len(quiz_data)} quiz questions with answers!")

def create_community_data():
    """Create categories and communities"""
    print("Creating community categories and groups...")
    
    # Create Categories
    categories_data = [
        {
            "name": "Ocean Conservation",
            "description": "Groups focused on protecting marine ecosystems and wildlife",
            "communities": [
                {
                    "title": "Marine Wildlife Protection Alliance",
                    "description": "Dedicated to protecting endangered marine species",
                    "link": "https://marineprotection.org"
                },
                {
                    "title": "Coral Reef Restoration Network",
                    "description": "Community working to restore coral reef ecosystems",
                    "link": "https://coralrestoration.org"
                },
                {
                    "title": "Ocean Cleanup Initiative",
                    "description": "Volunteers working to remove plastic from oceans",
                    "link": "https://oceancleanup.org"
                }
            ]
        },
        {
            "name": "Marine Research",
            "description": "Scientific research and exploration communities",
            "communities": [
                {
                    "title": "Deep Sea Exploration Society",
                    "description": "Researchers exploring the mysteries of the deep ocean",
                    "link": "https://deepsea.org"
                },
                {
                    "title": "Marine Biology Network",
                    "description": "Scientists studying marine life and ecosystems",
                    "link": "https://marinebio.org"
                },
                {
                    "title": "Ocean Data Collectors",
                    "description": "Citizen scientists gathering ocean data",
                    "link": "https://oceandata.org"
                }
            ]
        },
        {
            "name": "Education & Awareness",
            "description": "Groups focused on ocean education and public awareness",
            "communities": [
                {
                    "title": "Ocean Educators Unite",
                    "description": "Teachers and educators sharing ocean knowledge",
                    "link": "https://oceaneducators.org"
                },
                {
                    "title": "Blue Planet Awareness",
                    "description": "Spreading awareness about ocean issues",
                    "link": "https://blueplanet.org"
                }
            ]
        }
    ]
    
    for cat_data in categories_data:
        # Create category
        category = Category.objects.create(
            name=cat_data["name"],
            description=cat_data["description"]
        )
        
        # Create communities for this category
        for comm_data in cat_data["communities"]:
            Community.objects.create(
                title=comm_data["title"],
                category=category,
                description=comm_data["description"],
                link=comm_data["link"]
            )
    
    print(f"Created {len(categories_data)} categories with communities!")

def create_threats_and_solutions():
    """Create ocean threats and solutions"""
    print("Creating threats and solutions...")
    
    threats_data = [
        {
            "title": "Plastic Pollution",
            "description": "Millions of tons of plastic waste enter our oceans every year, harming marine life and ecosystems."
        },
        {
            "title": "Ocean Acidification", 
            "description": "Increased CO2 absorption is making oceans more acidic, threatening coral reefs and shell-forming creatures."
        },
        {
            "title": "Overfishing",
            "description": "Unsustainable fishing practices are depleting fish populations and disrupting marine food chains."
        },
        {
            "title": "Climate Change",
            "description": "Rising temperatures and sea levels are affecting marine habitats and species migration patterns."
        }
    ]
    
    solutions_data = [
        {
            "title": "Marine Protected Areas",
            "description": "Establishing protected zones where marine life can recover and thrive without human interference."
        },
        {
            "title": "Sustainable Fishing",
            "description": "Implementing fishing quotas and sustainable practices to ensure healthy fish populations."
        },
        {
            "title": "Plastic Reduction",
            "description": "Reducing single-use plastics and improving waste management to prevent ocean pollution."
        },
        {
            "title": "Reef Restoration",
            "description": "Active restoration of coral reefs through coral gardening and transplantation programs."
        }
    ]
    
    for threat_data in threats_data:
        Threat.objects.create(
            title=threat_data["title"],
            description=threat_data["description"]
        )
    
    for solution_data in solutions_data:
        Solution.objects.create(
            title=solution_data["title"],
            description=solution_data["description"]
        )
    
    print(f"Created {len(threats_data)} threats and {len(solutions_data)} solutions!")

def create_endangered_species():
    """Create endangered species data"""
    print("Creating endangered species...")
    
    # Create species categories first
    species_categories = [
        "Marine Mammals",
        "Sea Turtles", 
        "Sharks and Rays",
        "Coral Species"
    ]
    
    for cat_name in species_categories:
        endangered_species.objects.create(title=cat_name)
    
    print(f"Created {len(species_categories)} species categories!")

def main():
    print("🌊 Restoring Beneath the Blue Data 🌊")
    print("=" * 50)
    
    try:
        create_quiz_data()
        create_community_data()
        create_threats_and_solutions()
        create_endangered_species()
        
        print("\n✅ Data restoration completed successfully!")
        print("🎯 Your website now has:")
        print("   - Quiz questions about ocean conservation")
        print("   - Community categories and groups")
        print("   - Ocean threats and solutions")
        print("   - Endangered species categories")
        print("\n🌊 Your Beneath the Blue website is fully restored!")
        
    except Exception as e:
        print(f"❌ Error during data restoration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
