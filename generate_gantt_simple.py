"""
Generate Professional Gantt Chart - No Pandas Required
CN7021 School Activity Booking System
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

def create_gantt_chart():
    # 8-week project: Oct 16 - Dec 22, 2024
    start_date = datetime(2024, 10, 16)
    
    # Define tasks with sprint allocation
    tasks = [
        # Sprint 1 (Weeks 1-2): Oct 16 - Oct 29
        {"task": "Requirements Analysis & SRS", "start": 0, "duration": 7, "owner": "All", "sprint": 1},
        {"task": "Database Design (ERD, 3NF)", "start": 5, "duration": 7, "owner": "Shiva", "sprint": 1},
        {"task": "System Architecture Design", "start": 7, "duration": 7, "owner": "Sanchit", "sprint": 1},
        
        # Sprint 2 (Weeks 3-4): Oct 30 - Nov 12
        {"task": "Authentication Module", "start": 14, "duration": 7, "owner": "Chichebendu", "sprint": 2},
        {"task": "Parent Dashboard Development", "start": 14, "duration": 10, "owner": "Sharjeel", "sprint": 2},
        {"task": "Activity Booking Core Logic", "start": 17, "duration": 10, "owner": "Shiva", "sprint": 2},
        
        # Sprint 3 (Weeks 5-6): Nov 13 - Nov 26
        {"task": "Email Notification System", "start": 28, "duration": 7, "owner": "Sanchit", "sprint": 3},
        {"task": "PDF Invoice Generation", "start": 28, "duration": 7, "owner": "Sanchit", "sprint": 3},
        {"task": "Admin Dashboard & RBAC", "start": 28, "duration": 10, "owner": "Chichebendu", "sprint": 3},
        {"task": "Waitlist Management", "start": 31, "duration": 7, "owner": "Shiva", "sprint": 3},
        
        # Sprint 4 (Weeks 7-8): Nov 27 - Dec 10
        {"task": "Unit Testing & Integration", "start": 42, "duration": 7, "owner": "All", "sprint": 4},
        {"task": "Security Testing (OWASP ZAP)", "start": 45, "duration": 5, "owner": "Chichebendu", "sprint": 4},
        {"task": "Deployment & Cloud Hosting", "start": 47, "duration": 5, "owner": "Sanchit", "sprint": 4},
        
        # Final Phase: Dec 11 - Dec 22
        {"task": "Report Writing & Documentation", "start": 49, "duration": 14, "owner": "All", "sprint": 5},
        {"task": "Final Testing & Bug Fixes", "start": 52, "duration": 10, "owner": "All", "sprint": 5},
    ]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 10))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('#f8f9fa')
    
    # Color scheme for team members
    colors = {
        "All": "#3498db",      # Blue
        "Sanchit": "#e74c3c",  # Red
        "Sharjeel": "#2ecc71", # Green
        "Chichebendu": "#f39c12", # Orange
        "Shiva": "#9b59b6"     # Purple
    }
    
    # Draw tasks
    for i, task in enumerate(tasks):
        start_day = start_date + timedelta(days=task["start"])
        end_day = start_day + timedelta(days=task["duration"])
        
        # Draw bar
        ax.barh(i, task["duration"], left=mdates.date2num(start_day), 
                height=0.6, color=colors[task["owner"]], 
                edgecolor='black', linewidth=0.5, alpha=0.85)
        
        # Add task label
        task_label = f"{task['task']} ({task['owner']})"
        ax.text(mdates.date2num(start_day) - 1, i, task_label, 
                va='center', ha='right', fontsize=9, fontweight='bold')
        
        # Add duration label
        mid_point = mdates.date2num(start_day) + task["duration"]/2
        ax.text(mid_point, i, f"{task['duration']}d", 
                va='center', ha='center', fontsize=8, color='white', fontweight='bold')
    
    # Add sprint separators
    sprint_dates = [
        (datetime(2024, 10, 16), "Sprint 1\\nSetup & Design"),
        (datetime(2024, 10, 30), "Sprint 2\\nCore Development"),
        (datetime(2024, 11, 13), "Sprint 3\\nFeatures & Integration"),
        (datetime(2024, 11, 27), "Sprint 4\\nTesting & Deployment"),
        (datetime(2024, 12, 11), "Final Phase\\nDocumentation"),
    ]
    
    for date, label in sprint_dates:
        ax.axvline(x=mdates.date2num(date), color='red', linestyle='--', linewidth=1.5, alpha=0.7)
        ax.text(mdates.date2num(date), len(tasks) + 0.5, label, 
                rotation=0, va='bottom', ha='center', fontsize=9, 
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # Formatting
    ax.set_ylim(-1, len(tasks))
    ax.set_xlim(mdates.date2num(start_date) - 5, 
                mdates.date2num(datetime(2024, 12, 22)) + 2)
    
    # X-axis (dates)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
    plt.xticks(rotation=45, ha='right')
    
    # Remove y-axis labels
    ax.set_yticks([])
    
    # Grid
    ax.grid(True, axis='x', linestyle=':', alpha=0.3)
    
    # Title and labels
    ax.set_xlabel('Timeline (Oct 2024 - Dec 2024)', fontsize=12, fontweight='bold')
    ax.set_title('School Activity Booking System - Project Gantt Chart\\nCN7021 Advanced Software Engineering (Group 3.B)', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # Legend
    legend_elements = [plt.Rectangle((0,0),1,1, fc=colors[owner], label=owner, alpha=0.85) 
                      for owner in ["All", "Sanchit", "Sharjeel", "Chichebendu", "Shiva"]]
    ax.legend(handles=legend_elements, loc='upper right', title='Team Members', 
              frameon=True, fancybox=True, shadow=True)
    
    # Add project info
    info_text = "Total Duration: 68 days (9.7 weeks) | Team Size: 4 members | Total Effort: 180 person-hours"
    fig.text(0.5, 0.02, info_text, ha='center', fontsize=9, 
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
    
    plt.tight_layout()
    
    # Save
    output_file = 'Gantt_Chart_Professional.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Professional Gantt Chart saved: {output_file}")
    print(f"📊 Resolution: 300 DPI (publication quality)")
    print(f"📏 Dimensions: 14x10 inches")
    print(f"🎨 Color-coded by team member: All(Blue), Sanchit(Red), Sharjeel(Green), Chichebendu(Orange), Shiva(Purple)")
    print(f"✅ Ready to insert into Section 8.3 of DOCX!")
    print(f"\\n📋 Insert as: Figure 8 or Figure 9 (Gantt Chart)")
    
    plt.close()

if __name__ == '__main__':
    create_gantt_chart()
