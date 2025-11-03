"""
Project Planner with Matplotlib
Simpler, faster, more reliable Gantt charts
"""

import os, json
import matplotlib
# Use a non-GUI backend to allow rendering in server/request threads
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
load_dotenv()

HISTORY_FILE = "chat_history.json"

# Load/Save history
def load_history():
    return json.load(open(HISTORY_FILE)) if os.path.exists(HISTORY_FILE) else []

def save_history(history):
    json.dump(history, open(HISTORY_FILE, "w"), indent=2)


# Tool 1: Generate Gantt Chart with Matplotlib
def create_gantt_chart(tasks_json: str) -> str:
    """
    Creates a Gantt chart using matplotlib.
    
    Args:
        tasks_json: JSON string with tasks.
                   Format: [{"name": "Task Name", "duration": 5}, ...]
                   Duration is in DAYS.
    
    Returns:
        Success message with chart filename
    
    Example:
        create_gantt_chart('[{"name": "Design", "duration": 5}, {"name": "Dev", "duration": 10}]')
    """
    try:
        print("\n🔧 [Tool Called: create_gantt_chart]")
        
        # Parse JSON
        tasks = json.loads(tasks_json)
        
        if not tasks or len(tasks) == 0:
            return "❌ Error: No tasks provided."
        
        # Prepare data
        task_names = []
        start_days = []
        durations = []
        
        current_day = 0
        for task in tasks:
            task_names.append(task.get("name", "Unnamed"))
            start_days.append(current_day)
            duration = int(task.get("duration", 1))
            durations.append(duration)
            current_day += duration
        
        total_duration = current_day
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, max(6, len(tasks) * 0.8)))
        
        # Color palette
        colors = plt.cm.Set3(range(len(tasks)))
        
        # Create bars
        y_pos = range(len(tasks))
        bars = ax.barh(y_pos, durations, left=start_days, height=0.6, 
                      color=colors, edgecolor='black', linewidth=1.5)
        
        # Add duration labels on bars
        for i, (bar, duration) in enumerate(zip(bars, durations)):
            width = bar.get_width()
            x_pos = bar.get_x() + width / 2
            ax.text(x_pos, bar.get_y() + bar.get_height()/2, 
                   f'{duration}d',
                   ha='center', va='center', 
                   fontweight='bold', fontsize=10,
                   color='black')
        
        # Customize chart
        ax.set_yticks(y_pos)
        ax.set_yticklabels(task_names, fontsize=11)
        ax.set_xlabel('Days from Start', fontsize=12, fontweight='bold')
        ax.set_ylabel('Tasks', fontsize=12, fontweight='bold')
        ax.set_title(f'Project Gantt Chart\n{len(tasks)} Tasks • {total_duration} Days Total', 
                    fontsize=14, fontweight='bold', pad=20)
        
        # Grid
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        
        # Set x-axis limits with padding
        ax.set_xlim(0, total_duration * 1.1)
        
        # Tight layout
        plt.tight_layout()
        
        # Save
        output_file = "gantt_chart.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        print(f"✅ Chart saved: {output_file}")
        
        return f"""✅ Successfully created Gantt chart"""
        
    except json.JSONDecodeError as e:
        return f"❌ Error: Invalid JSON format.\nDetails: {str(e)}"
    except Exception as e:
        return f"❌ Error creating chart: {str(e)}"


# Create agent
agent = Agent(
    model=OpenAIChat(id="gpt-4.1-mini"),
    tools=[create_gantt_chart],
    markdown=True,
    instructions=[
        "You are a project planning assistant that creates Gantt charts and reports.",
        "",
        "CRITICAL RULES:",
        "1. When user describes tasks with durations, IMMEDIATELY call create_gantt_chart",
        "2. Don't ask permission - just create the chart automatically",
        "3. Use this EXACT JSON format:",
        '   [{"name": "Task Name", "duration": 5}, {"name": "Another", "duration": 10}]',
        "",
        "Duration MUST be in DAYS (convert if user says weeks/months):",
        "• 1 week = 7 days",
        "• 1 month = 30 days",
        "",
        "EXAMPLES:",
        "User: 'Design (2 weeks), Development (1 month), Testing (5 days)'",
        "You: [Call create_gantt_chart with:",
        '     \'[{"name": "Design", "duration": 14}, {"name": "Development", "duration": 30}, {"name": "Testing", "duration": 5}]\']',
        "",
        "After creating chart, you can offer to create a report too and display it",
    ]
)


# Main loop
def main():
    print("Project Planner with Matplotlib")
    
    history = load_history()
    
    if history:
        print(f"\n📚 Loaded {len(history)} previous messages")
    
    print()
    
    while True:
        user_input = input("\n\033[1;36mYou:\033[0m ").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() == "exit":
            print("\n👋 Goodbye!")
            break
        
        if user_input.lower() == "clear":
            history = []
            save_history(history)
            print("\n🗑️ History cleared!")
            continue
      
        # Add to history
        history.append({"role": "user", "content": user_input})
        
        # Build context
        context = "\n".join(f"{m['role']}: {m['content']}" for m in history[-10:])
        
        try:
            # Run agent
            response = agent.run(context, stream=False)
            print(response.content)
            reply = response.content if hasattr(response, "content") else str(response)
            
            # Save to history
            history.append({"role": "assistant", "content": reply})
            save_history(history)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
        main()