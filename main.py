# main.py - INTELLIGENT LEARNING ROADMAP GENERATOR WITH REAL PROJECTS
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os, requests, json, uuid
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = FastAPI(
    title="Intelligent Learning Roadmap Generator Pro",
    description="AI-powered learning path generator with real projects and resources",
    version="3.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EnhancedUserInput(BaseModel):
    goal: str
    proficiency: str
    time_commitment: str
    learning_style: List[str]
    specific_interests: Optional[str] = None
    challenges: Optional[str] = None

class ProgressUpdate(BaseModel):
    roadmap_id: str
    week_completed: int
    project_done: bool
    notes: Optional[str] = None

progress_db = {}

# REAL PROJECT TEMPLATES WITH GITHUB LINKS
REAL_PROJECTS = {
    "python": [
        {
            "title": "Build a Personal Finance Tracker",
            "description": "Create a command-line app to track expenses and income",
            "github_template": "https://github.com/trekhleb/learn-python",
            "skills": ["File I/O", "Data Structures", "Basic Algorithms"],
            "demo_url": "https://replit.com/@python/finance-tracker"
        },
        {
            "title": "Web Scraper for News Articles",
            "description": "Scrape news websites and save articles to a database",
            "github_template": "https://github.com/scrapinghub/python-web-scraper",
            "skills": ["Web Scraping", "HTML Parsing", "Database"],
            "demo_url": "https://replit.com/@python/web-scraper"
        }
    ],
    "web": [
        {
            "title": "Todo List Application",
            "description": "Build a full-stack todo app with user authentication",
            "github_template": "https://github.com/spring-projects/spring-petclinic",
            "skills": ["HTML/CSS", "JavaScript", "Backend API"],
            "demo_url": "https://todomvc.com"
        },
        {
            "title": "Weather Dashboard",
            "description": "Create a dashboard showing weather from multiple cities",
            "github_template": "https://github.com/public-apis/public-apis",
            "skills": ["API Integration", "Frontend", "Data Visualization"],
            "demo_url": "https://openweathermap.org/api"
        }
    ],
    "data": [
        {
            "title": "COVID-19 Data Analysis",
            "description": "Analyze COVID-19 trends and create visualizations",
            "github_template": "https://github.com/owid/covid-19-data",
            "skills": ["Data Analysis", "Visualization", "Pandas"],
            "demo_url": "https://ourworldindata.org/coronavirus"
        },
        {
            "title": "Customer Segmentation",
            "description": "Use clustering algorithms to segment customers",
            "github_template": "https://github.com/scikit-learn/scikit-learn",
            "skills": ["Machine Learning", "Clustering", "Analysis"],
            "demo_url": "https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_digits.html"
        }
    ]
}

# REAL RESOURCES THAT WORK
REAL_RESOURCES = {
    "python": [
        {"type": "Video", "title": "Python for Beginners - Full Course", "url": "https://www.youtube.com/watch?v=_uQrJ0TkZlc", "platform": "YouTube", "channel": "Programming with Mosh"},
        {"type": "Course", "title": "Python for Everybody", "url": "https://www.coursera.org/specializations/python", "platform": "Coursera", "free": True},
        {"type": "Article", "title": "Python Official Tutorial", "url": "https://docs.python.org/3/tutorial/", "source": "Python.org"},
        {"type": "Project", "title": "100 Days of Code: Python", "url": "https://github.com/100DaysOfCode-Python", "platform": "GitHub"}
    ],
    "web": [
        {"type": "Video", "title": "HTML & CSS Full Course", "url": "https://www.youtube.com/watch?v=mU6anWqZJcc", "platform": "YouTube", "channel": "freeCodeCamp"},
        {"type": "Course", "title": "The Odin Project", "url": "https://www.theodinproject.com/", "platform": "Odin Project", "free": True},
        {"type": "Article", "title": "MDN Web Docs", "url": "https://developer.mozilla.org/en-US/", "source": "Mozilla"},
        {"type": "Project", "title": "Frontend Mentor Challenges", "url": "https://www.frontendmentor.io/", "platform": "Frontend Mentor"}
    ],
    "data": [
        {"type": "Video", "title": "Data Science Full Course", "url": "https://www.youtube.com/watch?v=ua-CiDNNj30", "platform": "YouTube", "channel": "edureka!"},
        {"type": "Course", "title": "Data Science with Python", "url": "https://www.kaggle.com/learn/python", "platform": "Kaggle", "free": True},
        {"type": "Article", "title": "Towards Data Science", "url": "https://towardsdatascience.com/", "source": "Medium"},
        {"type": "Project", "title": "Kaggle Competitions", "url": "https://www.kaggle.com/competitions", "platform": "Kaggle"}
    ]
}

@app.get("/")
def root():
    return {
        "application": "Intelligent Learning Roadmap Generator Pro",
        "version": "3.0",
        "status": "active",
        "features": ["Real projects", "Working resources", "Progress tracking", "Visual timeline"]
    }

@app.post("/generate-roadmap")
def generate_roadmap(user_input: EnhancedUserInput):
    """Generate roadmap with REAL working resources and projects"""
    
    # Detect topic for relevant resources
    topic = detect_topic(user_input.goal.lower())
    
    try:
        # Get AI-generated structure
        roadmap_structure = get_ai_roadmap_structure(user_input)
        
        # Enhance with real resources and projects
        roadmap = enhance_with_real_content(roadmap_structure, topic, user_input)
        
        # Add metadata
        roadmap["roadmap_id"] = str(uuid.uuid4())[:8]
        roadmap["generated_at"] = datetime.now().isoformat()
        roadmap["topic"] = topic
        
        # Store
        progress_db[roadmap["roadmap_id"]] = {
            "roadmap": roadmap,
            "progress": {"completed_weeks": [], "completed_projects": []},
            "created_at": roadmap["generated_at"]
        }
        
        return roadmap
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return create_fallback_roadmap(user_input, topic)

def detect_topic(goal: str) -> str:
    """Detect the main topic from user goal"""
    goal_lower = goal.lower()
    if any(word in goal_lower for word in ["python", "programming", "coding", "software"]):
        return "python"
    elif any(word in goal_lower for word in ["web", "frontend", "backend", "fullstack", "html", "css", "javascript"]):
        return "web"
    elif any(word in goal_lower for word in ["data", "machine learning", "ai", "analysis", "visualization"]):
        return "data"
    else:
        return "general"

def get_ai_roadmap_structure(user_input: EnhancedUserInput) -> dict:
    """Get basic roadmap structure from AI"""
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return create_basic_structure(user_input)
    
    system_prompt = """Return ONLY JSON. Structure:
    {
        "title": "Title",
        "overview": "Overview",
        "weekly_themes": ["Theme 1", "Theme 2", "Theme 3", "Theme 4"],
        "weekly_focus": ["Focus 1", "Focus 2", "Focus 3", "Focus 4"],
        "weekly_objectives": [["Obj1", "Obj2"], ["Obj3", "Obj4"], ["Obj5", "Obj6"], ["Obj7", "Obj8"]]
    }"""
    
    user_prompt = f"""
    Create a {len(user_input.learning_style)}-week learning roadmap for:
    Goal: {user_input.goal}
    Level: {user_input.proficiency}
    Time: {user_input.time_commitment}
    Styles: {', '.join(user_input.learning_style)}
    
    Return only the JSON structure above.
    """
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "meta-llama/llama-3.1-8b-instruct",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 1000,
                "response_format": {"type": "json_object"}
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return json.loads(result["choices"][0]["message"]["content"])
    
    except:
        pass
    
    return create_basic_structure(user_input)

def create_basic_structure(user_input: EnhancedUserInput) -> dict:
    """Create basic roadmap structure"""
    weeks = 4
    return {
        "title": f"Learn {user_input.goal} - {user_input.proficiency} Roadmap",
        "overview": f"A {weeks}-week journey to master {user_input.goal} through hands-on projects and real resources.",
        "weekly_themes": [
            "Foundation & Setup",
            "Core Concepts", 
            "Advanced Techniques",
            "Real Projects"
        ],
        "weekly_focus": [
            "Learn basics and set up environment",
            "Master fundamental concepts",
            "Explore advanced features",
            "Build complete applications"
        ],
        "weekly_objectives": [
            ["Install tools", "Learn syntax", "First program"],
            ["Practice concepts", "Debug issues", "Small projects"],
            ["Advanced features", "Optimization", "Testing"],
            ["Portfolio project", "Deployment", "Documentation"]
        ]
    }

def enhance_with_real_content(structure: dict, topic: str, user_input: EnhancedUserInput) -> dict:
    """Enhance AI structure with real content"""
    
    # Get real resources for this topic
    topic_resources = REAL_RESOURCES.get(topic, REAL_RESOURCES["python"])
    topic_projects = REAL_PROJECTS.get(topic, REAL_PROJECTS["python"])
    
    # Build weekly plan with REAL resources
    weekly_plan = []
    for i in range(min(4, len(structure["weekly_themes"]))):
        week_num = i + 1
        
        # Select appropriate resources
        week_resources = []
        if i == 0:  # Week 1 - Basics
            week_resources = [r for r in topic_resources if r["type"] in ["Video", "Course"]][:2]
        elif i == 1:  # Week 2 - Intermediate
            week_resources = [r for r in topic_resources if r["type"] in ["Article", "Course"]][:2]
        else:  # Week 3-4 - Advanced
            week_resources = [r for r in topic_resources if r["type"] in ["Project", "Video"]][:2]
        
        # Add project
        project_index = min(i, len(topic_projects) - 1)
        week_project = topic_projects[project_index] if topic_projects else {
            "title": f"Week {week_num} Project",
            "description": "Hands-on project to apply what you learned",
            "github_template": "https://github.com/",
            "skills": ["Problem Solving", "Coding", "Debugging"]
        }
        
        weekly_plan.append({
            "week": week_num,
            "theme": structure["weekly_themes"][i],
            "focus": structure["weekly_focus"][i],
            "objectives": structure["weekly_objectives"][i],
            "time_estimate": f"{10 + i*5}-{15 + i*5} hours",
            "resources": week_resources,
            "project": week_project
        })
    
    return {
        "title": structure["title"],
        "overview": structure["overview"],
        "prerequisites": {
            "knowledge": ["Basic computer skills", "Internet access"],
            "tools": ["Computer", "Code editor", "Git"]
        },
        "weekly_plan": weekly_plan,
        "milestone_projects": topic_projects[:3],
        "success_tips": [
            "Code every day, even for 30 minutes",
            "Build projects that interest you",
            "Join communities for support",
            "Document your learning journey",
            "Teach others what you learn"
        ],
        "community_recommendations": [
            "Discord: Learn Together",
            "Reddit: r/learnprogramming", 
            "GitHub: Open Source",
            "Dev.to Community"
        ],
        "visual_timeline": generate_timeline_data(weekly_plan)
    }

def generate_timeline_data(weekly_plan: list) -> list:
    """Generate data for visual timeline"""
    timeline = []
    for week in weekly_plan:
        timeline.append({
            "week": week["week"],
            "theme": week["theme"],
            "milestones": week["objectives"],
            "project": week["project"]["title"]
        })
    return timeline

def create_fallback_roadmap(user_input: EnhancedUserInput, topic: str) -> dict:
    """Create a complete roadmap with real content as fallback"""
    
    topic_resources = REAL_RESOURCES.get(topic, REAL_RESOURCES["python"])
    topic_projects = REAL_PROJECTS.get(topic, REAL_PROJECTS["python"])
    
    roadmap_id = str(uuid.uuid4())[:8]
    
    return {
        "roadmap_id": roadmap_id,
        "title": f"Hands-On {user_input.goal} Learning Roadmap",
        "overview": f"A practical {user_input.time_commitment} journey to master {user_input.goal} through real projects and working resources.",
        "prerequisites": {
            "knowledge": ["Basic computer literacy", "Problem-solving mindset"],
            "tools": ["Computer with internet", "Modern browser", "Code editor"]
        },
        "weekly_plan": [
            {
                "week": 1,
                "theme": "Getting Started & Fundamentals",
                "focus": "Learn the basics and set up your development environment",
                "objectives": ["Install necessary tools", "Learn basic syntax", "Complete first project"],
                "time_estimate": "10-15 hours",
                "resources": topic_resources[:2],
                "project": topic_projects[0] if topic_projects else {
                    "title": "Hello World Project",
                    "description": "Create your first working application",
                    "github_template": "https://github.com/",
                    "skills": ["Setup", "Basic Syntax", "Debugging"]
                }
            },
            {
                "week": 2,
                "theme": "Core Concepts & Practice",
                "focus": "Master fundamental concepts through hands-on exercises",
                "objectives": ["Practice key concepts", "Build small applications", "Learn debugging"],
                "time_estimate": "15-20 hours",
                "resources": topic_resources[2:4],
                "project": topic_projects[1] if len(topic_projects) > 1 else {
                    "title": "Practical Application",
                    "description": "Build a functional application solving a real problem",
                    "github_template": "https://github.com/",
                    "skills": ["Problem Solving", "Implementation", "Testing"]
                }
            },
            {
                "week": 3,
                "theme": "Advanced Techniques",
                "focus": "Learn advanced features and optimization techniques",
                "objectives": ["Implement advanced features", "Optimize performance", "Learn testing"],
                "time_estimate": "20-25 hours",
                "resources": [r for r in topic_resources if r["type"] == "Project"][:2],
                "project": {
                    "title": "Advanced Project",
                    "description": "Create an optimized application with advanced features",
                    "github_template": "https://github.com/",
                    "skills": ["Advanced Features", "Optimization", "Deployment"]
                }
            },
            {
                "week": 4,
                "theme": "Real-World Projects",
                "focus": "Build portfolio-worthy projects and deploy them",
                "objectives": ["Complete major project", "Deploy application", "Document code"],
                "time_estimate": "25-30 hours",
                "resources": [{"type": "Project", "title": "Portfolio Projects", "url": "https://github.com/topics/portfolio", "platform": "GitHub"}],
                "project": {
                    "title": "Portfolio Showcase",
                    "description": "Build a complete application for your portfolio",
                    "github_template": "https://github.com/",
                    "skills": ["Full-stack Development", "Deployment", "Documentation"]
                }
            }
        ],
        "milestone_projects": topic_projects[:3] if topic_projects else [
            {
                "name": "Portfolio Project",
                "description": "Showcase your skills with a complete application",
                "skills": ["Frontend", "Backend", "Deployment"]
            },
            {
                "name": "Open Source Contribution",
                "description": "Contribute to a real open-source project",
                "skills": ["Git", "Collaboration", "Code Review"]
            }
        ],
        "success_tips": [
            "Code consistently - small daily progress beats occasional marathons",
            "Build projects you're passionate about",
            "Join communities and ask for help",
            "Document your journey and share learnings",
            "Don't fear mistakes - they're learning opportunities"
        ],
        "community_recommendations": [
            "Discord Programming Communities",
            "Reddit Learning Subreddits",
            "GitHub Open Source",
            "Stack Overflow for Questions"
        ],
        "visual_timeline": [
            {"week": 1, "theme": "Fundamentals", "milestones": ["Setup", "Basics", "First Project"]},
            {"week": 2, "theme": "Core Skills", "milestones": ["Practice", "Small Apps", "Debugging"]},
            {"week": 3, "theme": "Advanced", "milestones": ["Advanced Features", "Optimization", "Testing"]},
            {"week": 4, "theme": "Real World", "milestones": ["Portfolio Project", "Deployment", "Documentation"]}
        ],
        "generated_at": datetime.now().isoformat(),
        "topic": topic
    }

@app.post("/update-progress")
def update_progress(update: ProgressUpdate):
    """Update user progress"""
    if update.roadmap_id not in progress_db:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    
    progress = progress_db[update.roadmap_id]["progress"]
    
    if update.week_completed not in progress["completed_weeks"]:
        progress["completed_weeks"].append(update.week_completed)
    
    if update.project_done:
        progress.setdefault("completed_projects", []).append(update.week_completed)
    
    if update.notes:
        progress.setdefault("notes", []).append({
            "week": update.week_completed,
            "note": update.notes,
            "timestamp": datetime.now().isoformat()
        })
    
    roadmap = progress_db[update.roadmap_id]["roadmap"]
    total_weeks = len(roadmap.get("weekly_plan", []))
    completed = len(progress["completed_weeks"])
    percentage = (completed / total_weeks * 100) if total_weeks > 0 else 0
    
    return {
        "status": "success",
        "progress_percentage": round(percentage, 1),
        "completed_weeks": progress["completed_weeks"],
        "total_weeks": total_weeks
    }

@app.get("/roadmap/{roadmap_id}")
def get_roadmap(roadmap_id: str):
    """Get roadmap with progress"""
    if roadmap_id not in progress_db:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    
    data = progress_db[roadmap_id].copy()
    progress = data["progress"]
    
    total_weeks = len(data["roadmap"].get("weekly_plan", []))
    completed = len(progress.get("completed_weeks", []))
    
    data["stats"] = {
        "progress_percentage": round((completed / total_weeks * 100) if total_weeks > 0 else 0, 1),
        "completed_weeks": completed,
        "total_weeks": total_weeks
    }
    
    return data

@app.get("/visual-timeline/{roadmap_id}")
def get_visual_timeline(roadmap_id: str):
    """Get visual timeline data for charts"""
    if roadmap_id not in progress_db:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    
    roadmap = progress_db[roadmap_id]["roadmap"]
    progress = progress_db[roadmap_id]["progress"]
    
    timeline_data = []
    for week in roadmap.get("weekly_plan", []):
        timeline_data.append({
            "week": week["week"],
            "theme": week["theme"],
            "completed": week["week"] in progress.get("completed_weeks", []),
            "project": week["project"]["title"]
        })
    
    return {
        "timeline": timeline_data,
        "total_weeks": len(timeline_data),
        "completed_weeks": len(progress.get("completed_weeks", []))
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)