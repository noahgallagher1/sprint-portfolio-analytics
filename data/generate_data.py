"""
Sprint Performance & Portfolio Analytics - Data Generation Script

Generates realistic data for 6 months (12 sprints) including:
- Sprint-level metrics
- Story-level data (350-400 stories)
- Initiative/Portfolio data (25-30 initiatives)
- Team member data (8 team members)

Includes realistic patterns:
- Velocity stabilization over time
- Holiday impact (Sprint 6)
- Improving estimation accuracy
- Realistic blockers and carryovers
- Initiative distribution across impact/effort quadrants
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)


class SprintDataGenerator:
    """Generates realistic sprint analytics data"""

    def __init__(self):
        self.sprints = []
        self.stories = []
        self.initiatives = []
        self.team_members = []

        # Configuration
        self.num_sprints = 12
        self.num_team_members = 8
        self.num_initiatives = 28
        self.target_stories = 360

        # Start date: 6 months ago
        self.start_date = datetime.now() - timedelta(days=180)

        # Story point options (Fibonacci)
        self.story_points = [1, 2, 3, 5, 8, 13]

        # Story types
        self.story_types = ['Feature', 'Bug', 'Technical Debt', 'Spike']

        # Team roles
        self.roles = ['Frontend Dev', 'Backend Dev', 'QA Engineer', 'Designer',
                      'Backend Dev', 'Frontend Dev', 'Tech Lead', 'Full Stack Dev']

        # Team member names
        self.team_names = ['Alice Chen', 'Bob Martinez', 'Carol Johnson', 'David Kim',
                          'Emma Rodriguez', 'Frank Wilson', 'Grace Lee', 'Henry Brown']

        # Strategic alignment categories
        self.strategic_categories = [
            'Revenue Growth', 'Cost Reduction', 'Customer Experience',
            'Technical Excellence', 'Process Improvement'
        ]

    def generate_all_data(self):
        """Generate all datasets"""
        print("Generating sprint analytics data...")
        print(f"Target: {self.num_sprints} sprints, ~{self.target_stories} stories, {self.num_initiatives} initiatives")

        self.generate_team_members()
        self.generate_initiatives()
        self.generate_sprints_and_stories()

        # Create DataFrames
        sprints_df = pd.DataFrame(self.sprints)
        stories_df = pd.DataFrame(self.stories)
        initiatives_df = pd.DataFrame(self.initiatives)
        team_df = pd.DataFrame(self.team_members)

        # Save to CSV
        sprints_df.to_csv('data/sprint_data.csv', index=False)
        stories_df.to_csv('data/story_data.csv', index=False)
        initiatives_df.to_csv('data/initiative_data.csv', index=False)
        team_df.to_csv('data/team_data.csv', index=False)

        # Print summary
        print("\n" + "="*60)
        print("DATA GENERATION COMPLETE")
        print("="*60)
        print(f"✓ Sprints generated: {len(sprints_df)}")
        print(f"✓ Stories generated: {len(stories_df)}")
        print(f"✓ Initiatives generated: {len(initiatives_df)}")
        print(f"✓ Team members: {len(team_df)}")
        print(f"\nAverage velocity: {sprints_df['completed_points'].mean():.1f} points")
        print(f"Average sprint completion: {(sprints_df['completed_points'].sum() / sprints_df['committed_points'].sum() * 100):.1f}%")
        print(f"Stories per sprint: {len(stories_df) / len(sprints_df):.1f}")
        print("\nFiles saved:")
        print("  - data/sprint_data.csv")
        print("  - data/story_data.csv")
        print("  - data/initiative_data.csv")
        print("  - data/team_data.csv")
        print("="*60)

    def generate_team_members(self):
        """Generate team member data"""
        for i in range(self.num_team_members):
            # Base capacity with some variation
            base_capacity = 40 + np.random.randint(-5, 6)

            self.team_members.append({
                'member_id': f'TM{i+1:03d}',
                'name': self.team_names[i],
                'role': self.roles[i],
                'avg_capacity_per_sprint': base_capacity,
                'specialization': self._get_specialization(self.roles[i])
            })

    def _get_specialization(self, role):
        """Get specializations based on role"""
        specializations = {
            'Frontend Dev': 'React, TypeScript, UI/UX',
            'Backend Dev': 'Python, APIs, Database',
            'QA Engineer': 'Testing, Automation, CI/CD',
            'Designer': 'UI Design, Figma, User Research',
            'Tech Lead': 'Architecture, Code Review, Mentoring',
            'Full Stack Dev': 'React, Python, DevOps'
        }
        return specializations.get(role, 'General Development')

    def generate_initiatives(self):
        """Generate portfolio initiatives with realistic distribution"""

        # Initiative distribution by quadrant:
        # Quick Wins: High Impact (7-10), Low Effort (2-5) - 5 initiatives
        # Major Projects: High Impact (7-10), High Effort (6-10) - 8 initiatives
        # Fill-ins: Low Impact (2-6), Low Effort (2-5) - 10 initiatives
        # Time Sinks: Low Impact (2-6), High Effort (6-10) - 5 initiatives

        initiative_templates = [
            # Quick Wins (5)
            ("Checkout Flow Optimization", "Revenue Growth", 9, 3, "High"),
            ("One-Click Reorder Feature", "Customer Experience", 8, 4, "High"),
            ("Email Campaign Automation", "Revenue Growth", 8, 3, "Medium"),
            ("Mobile App Push Notifications", "Customer Experience", 7, 4, "High"),
            ("Search Performance Enhancement", "Customer Experience", 7, 3, "Medium"),

            # Major Projects (8)
            ("New Payment Gateway Integration", "Revenue Growth", 9, 8, "High"),
            ("Customer Personalization Engine", "Revenue Growth", 9, 9, "High"),
            ("Mobile App Redesign", "Customer Experience", 8, 9, "Medium"),
            ("Multi-Warehouse Fulfillment System", "Cost Reduction", 8, 8, "High"),
            ("Advanced Analytics Platform", "Process Improvement", 7, 7, "Medium"),
            ("Inventory Management System", "Cost Reduction", 8, 8, "High"),
            ("Design System Implementation", "Technical Excellence", 7, 7, "Medium"),
            ("API Rate Limiting & Security", "Technical Excellence", 7, 6, "Medium"),

            # Fill-ins (10)
            ("Update Footer Links", "Process Improvement", 3, 2, "Low"),
            ("Add Product Tooltips", "Customer Experience", 4, 3, "Low"),
            ("Refactor CSS Utilities", "Technical Excellence", 3, 3, "Low"),
            ("Update Terms of Service Page", "Process Improvement", 2, 2, "Low"),
            ("Add Loading Spinners", "Customer Experience", 4, 3, "Low"),
            ("Update Error Messages", "Customer Experience", 3, 2, "Low"),
            ("Database Query Optimization", "Technical Excellence", 5, 4, "Medium"),
            ("Add Google Analytics Events", "Process Improvement", 4, 3, "Low"),
            ("Update Product Image Alt Tags", "Customer Experience", 3, 2, "Low"),
            ("Implement Feature Flags", "Technical Excellence", 5, 4, "Medium"),

            # Time Sinks (5) - These should get deprioritized
            ("Legacy Code Migration", "Technical Excellence", 4, 9, "Low"),
            ("Internal Admin Tool Rebuild", "Process Improvement", 3, 8, "Low"),
            ("Deprecated API Cleanup", "Technical Excellence", 4, 7, "Low"),
            ("Old Report Generator Update", "Process Improvement", 3, 7, "Low"),
            ("Archive System Refactor", "Technical Excellence", 4, 8, "Low"),
        ]

        for i, (name, category, impact, effort, roi) in enumerate(initiative_templates):
            # Determine status based on initiative type and timing
            status = self._determine_initiative_status(i, impact, effort)

            # Assign to sprint based on priority
            priority_score = impact / effort
            if priority_score > 2:  # Quick wins
                target_sprint = random.randint(1, 4)
            elif priority_score > 1:  # Good initiatives
                target_sprint = random.randint(3, 8)
            else:  # Lower priority
                target_sprint = random.randint(6, 12)

            # Generate story points (effort * 5 + variation)
            total_points = effort * 5 + random.randint(-5, 10)

            # Completed points based on status
            if status == 'Completed':
                completed_points = total_points
                actual_sprint = target_sprint + random.randint(0, 2)
            elif status == 'Active':
                completed_points = int(total_points * random.uniform(0.3, 0.8))
                actual_sprint = None
            elif status == 'Deprioritized':
                completed_points = int(total_points * random.uniform(0, 0.3))
                actual_sprint = None
            else:  # Backlog
                completed_points = 0
                actual_sprint = None

            # Owner (stakeholder)
            owners = ['Sarah Chen (VP Product)', 'Mike Johnson (Dir Engineering)',
                     'Lisa Rodriguez (Head of CX)', 'Tom Wilson (CFO)',
                     'Emily Zhang (Dir Operations)', 'David Park (Head of Growth)']

            self.initiatives.append({
                'initiative_id': f'INIT-{i+1:03d}',
                'name': name,
                'description': f'Initiative to deliver {name.lower()} capabilities',
                'impact_score': impact,
                'effort_score': effort,
                'strategic_category': category,
                'status': status,
                'owner': random.choice(owners),
                'total_story_points': total_points,
                'completed_story_points': completed_points,
                'target_sprint': target_sprint,
                'actual_completion_sprint': actual_sprint,
                'roi_estimate': roi,
                'stories_count': 0  # Will be updated when generating stories
            })

    def _determine_initiative_status(self, index, impact, effort):
        """Determine realistic initiative status"""
        priority_score = impact / effort

        # Quick wins (high priority) - mostly completed or active
        if priority_score > 2:
            return random.choice(['Completed', 'Completed', 'Active'])

        # Good initiatives - mix of completed, active, backlog
        elif priority_score > 1:
            return random.choice(['Completed', 'Active', 'Active', 'Backlog'])

        # Lower priority - mostly backlog or deprioritized
        else:
            return random.choice(['Backlog', 'Backlog', 'Deprioritized', 'Active'])

    def generate_sprints_and_stories(self):
        """Generate sprint and story data with realistic patterns"""

        story_id_counter = 1
        current_date = self.start_date

        # Track team estimation accuracy improvement
        base_accuracy = 0.65  # Start at 65%
        accuracy_increment = 0.02  # Improve 2% per sprint

        # Track velocity improvement
        base_velocity = 32

        for sprint_num in range(1, self.num_sprints + 1):
            sprint_start = current_date
            sprint_end = current_date + timedelta(days=14)

            # Team capacity (reduces in Sprint 6 for holidays)
            if sprint_num == 6:
                team_capacity = 200  # Reduced for holidays
            else:
                team_capacity = 320 + random.randint(-20, 20)

            # Velocity improves over time with stabilization
            sprint_velocity = base_velocity + (sprint_num * 1.5) + np.random.normal(0, max(8 - sprint_num * 0.5, 3))
            sprint_velocity = max(25, min(55, sprint_velocity))

            # Committed points (sometimes over-commit early on)
            if sprint_num <= 3:
                committed_points = int(sprint_velocity * random.uniform(0.95, 1.15))
            else:
                committed_points = int(sprint_velocity * random.uniform(0.90, 1.05))

            # Completed points (depends on commitment)
            completion_rate = 0.85 if committed_points > sprint_velocity * 1.1 else 0.95
            completion_rate += min(sprint_num * 0.01, 0.1)  # Improve over time
            completed_points = int(committed_points * completion_rate)

            # Generate stories for this sprint
            sprint_stories = self._generate_sprint_stories(
                sprint_num,
                committed_points,
                completed_points,
                sprint_start,
                sprint_end,
                base_accuracy + (sprint_num * accuracy_increment),
                story_id_counter
            )

            story_id_counter += len(sprint_stories)
            self.stories.extend(sprint_stories)

            # Calculate sprint metrics
            sprint_data = {
                'sprint_number': sprint_num,
                'start_date': sprint_start.strftime('%Y-%m-%d'),
                'end_date': sprint_end.strftime('%Y-%m-%d'),
                'duration_days': 14,
                'team_capacity': team_capacity,
                'committed_points': committed_points,
                'completed_points': completed_points,
                'velocity': completed_points,
                'team_size': self.num_team_members,
                'completion_rate': completed_points / committed_points if committed_points > 0 else 0,
                'stories_count': len(sprint_stories),
                'stories_completed': len([s for s in sprint_stories if s['status'] == 'Completed']),
                'stories_carried_over': len([s for s in sprint_stories if s['status'] == 'Carried Over'])
            }

            self.sprints.append(sprint_data)

            # Move to next sprint
            current_date = sprint_end

        # Update initiative story counts
        self._update_initiative_story_counts()

    def _generate_sprint_stories(self, sprint_num, committed_points, completed_points,
                                  start_date, end_date, accuracy, start_id):
        """Generate stories for a single sprint"""
        stories = []
        story_id = start_id
        points_allocated = 0
        points_completed = 0

        # Determine number of stories (average 30 per sprint, varies)
        num_stories = random.randint(25, 35)

        # Get active initiatives for this sprint
        active_initiatives = [init for init in self.initiatives
                            if init['status'] in ['Active', 'Completed'] and
                            init['target_sprint'] <= sprint_num]

        if not active_initiatives:
            active_initiatives = [init for init in self.initiatives
                                if init['status'] == 'Backlog'][:5]

        # Story type distribution changes over time
        if sprint_num <= 3:
            type_weights = [0.60, 0.25, 0.10, 0.05]  # Early: more features, more bugs
        elif sprint_num <= 6:
            type_weights = [0.65, 0.20, 0.10, 0.05]  # Mid: stabilizing
        else:
            type_weights = [0.70, 0.15, 0.10, 0.05]  # Late: fewer bugs, more features

        for _ in range(num_stories):
            # Story points
            points = random.choice(self.story_points[:5])  # Mostly smaller stories

            # Story type
            story_type = random.choices(self.story_types, weights=type_weights)[0]

            # Assign to initiative
            initiative = random.choice(active_initiatives) if active_initiatives else None
            initiative_id = initiative['initiative_id'] if initiative else None

            # Priority (higher for earlier stories in sprint)
            if _ < num_stories * 0.3:
                priority = 'High'
            elif _ < num_stories * 0.7:
                priority = 'Medium'
            else:
                priority = 'Low'

            # Determine if story is completed
            if points_completed + points <= completed_points:
                status = 'Completed'
                points_completed += points
                final_points = self._apply_estimation_variance(points, accuracy)

                # Cycle time (days in progress)
                cycle_time = random.randint(1, 10)

                # Blockers (10% chance)
                has_blocker = random.random() < 0.10
                num_blockers = 1 if has_blocker else 0
                blocker_duration = random.randint(1, 3) if has_blocker else 0

            elif random.random() < 0.12:  # 12% carried over
                status = 'Carried Over'
                final_points = points
                cycle_time = random.randint(5, 14)
                num_blockers = random.randint(0, 2)
                blocker_duration = random.randint(0, 5)
            else:
                status = random.choice(['Incomplete', 'Incomplete', 'Descoped'])
                final_points = points
                cycle_time = random.randint(1, 14)
                num_blockers = random.randint(0, 1)
                blocker_duration = random.randint(0, 3)

            # Assign to team member
            assignee = random.choice(self.team_members)

            # Dependencies (some stories have dependencies)
            dependencies_count = random.choices([0, 1, 2, 3], weights=[0.7, 0.2, 0.08, 0.02])[0]

            story = {
                'story_id': f'STORY-{story_id:04d}',
                'sprint_number': sprint_num,
                'story_points': points,
                'final_story_points': final_points,
                'story_type': story_type,
                'initiative_id': initiative_id,
                'status': status,
                'cycle_time_days': cycle_time,
                'num_blockers': num_blockers,
                'blocker_duration_days': blocker_duration,
                'assignee_id': assignee['member_id'],
                'assignee_name': assignee['name'],
                'priority': priority,
                'dependencies_count': dependencies_count,
                'start_date': (start_date + timedelta(days=random.randint(0, 3))).strftime('%Y-%m-%d'),
                'estimation_accuracy': abs(points - final_points) / points if points > 0 else 1.0
            }

            stories.append(story)
            story_id += 1
            points_allocated += points

            # Update initiative story count
            if initiative:
                initiative['stories_count'] += 1

        return stories

    def _apply_estimation_variance(self, original_points, accuracy):
        """Apply realistic estimation variance"""
        # Accuracy means how close we get on average
        variance = 1 - accuracy
        adjustment = np.random.normal(0, variance * original_points)
        final_points = max(1, int(original_points + adjustment))
        return final_points

    def _update_initiative_story_counts(self):
        """Update story counts in initiatives based on generated stories"""
        for initiative in self.initiatives:
            init_id = initiative['initiative_id']
            story_count = len([s for s in self.stories if s['initiative_id'] == init_id])
            initiative['stories_count'] = story_count


if __name__ == '__main__':
    generator = SprintDataGenerator()
    generator.generate_all_data()
    print("\n✅ Data generation complete! Ready to run dashboard.")
    print("Next step: streamlit run app.py")
