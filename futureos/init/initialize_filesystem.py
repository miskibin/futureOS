import os
from pathlib import Path
from typing import Optional


def initialize_filesystem(base_path: Optional[Path] = None) -> None:
    """Initialize a minimal filesystem for AI navigation demonstration"""
    if base_path is None:
        base_path = Path.cwd() / "FileSystem"
    # if already exists, return
    if base_path.exists():
        return
    # Create base filesystem directory
    os.makedirs(base_path, exist_ok=True)

    # Define simple directory structure
    structure = {
        "documents": {
            "meeting_notes.txt": "Team sync - March 15, 2024\n- Discussed Q2 roadmap\n- New feature priorities\n- Team capacity planning\n\nAction items:\n1. Sarah to finalize specs\n2. Mike to estimate backend work\n3. Follow up next week\n",
            "personal_tasks.txt": "TODO:\n- Schedule dentist appointment\n- Pay electricity bill\n- Buy groceries\n- Call mom\n- Renew gym membership\n",
            "recipes.txt": "Favorite Pasta Recipe:\n\nIngredients:\n- 400g spaghetti\n- 2 cloves garlic\n- Olive oil\n- Fresh basil\n- Parmesan cheese\n\nInstructions:\n1. Boil pasta\n2. Sauté garlic...\n",
        },
        "pictures": {},  # Empty for now, could add binary files if needed
        "work": {
            "Company": {
                "project_proposal.txt": "Project: Customer Portal Redesign\nDue Date: April 30, 2024\n\nObjectives:\n1. Improve user experience\n2. Reduce support tickets by 30%\n3. Increase self-service adoption\n\nBudget: $75,000\nTimeline: 3 months\n",
                "meeting_minutes.txt": "Client Meeting - March 12, 2024\n\nAttendees:\n- John (Project Manager)\n- Sarah (Designer)\n- Client stakeholders\n\nDiscussion:\n- Current pain points\n- Desired features\n- Timeline constraints\n",
                "quarterly_goals.txt": "Q2 2024 Objectives:\n\n1. Launch mobile app v2.0\n2. Achieve 95% customer satisfaction\n3. Reduce technical debt by 20%\n4. Implement automated testing\n",
                "team_contacts.csv": "name,role,email,phone\nJohn Smith,Project Manager,john.s@company.com,555-0101\nSarah Johnson,UI Designer,sarah.j@company.com,555-0102\nMike Williams,Developer,mike.w@company.com,555-0103\n",
            },
            "Personal_Projects": {
                "budget_tracker.csv": "date,category,amount,notes\n2024-03-01,Groceries,125.50,Weekly shopping\n2024-03-03,Transport,45.00,Bus pass\n2024-03-05,Utilities,180.75,Electricity bill\n2024-03-07,Entertainment,60.00,Movie night\n",
                "workout_log.txt": "March 2024 Workouts:\n\n03/01 - Upper Body\n- Bench press: 3x10\n- Pull-ups: 3x8\n- Shoulder press: 3x12\n\n03/03 - Lower Body\n- Squats: 3x10\n- Deadlifts: 3x8\n- Lunges: 3x12\n",
                "ideas.txt": "Project Ideas:\n\n1. AI-powered meal planner\n2. Home automation system\n3. Personal finance dashboard\n4. Fitness tracking app\n\nTechnology stack:\n- Python\n- React\n- PostgreSQL\n",
            },
        },
    }

    def create_structure(current_path: Path, structure: dict):
        for name, content in structure.items():
            path = current_path / name
            if isinstance(content, dict):
                os.makedirs(path, exist_ok=True)
                create_structure(path, content)
            else:
                os.makedirs(path.parent, exist_ok=True)
                with open(path, "w") as f:
                    f.write(content)

    create_structure(base_path, structure)
    return base_path
