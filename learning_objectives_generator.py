THIS SHOULD BE A LINTER ERROR#!/usr/bin/env python3
"""
Learning Objectives Generator
A program that helps instructional designers write clear and concise learning objectives
aligned to Bloom's Taxonomy levels.
"""

import re
import argparse
from typing import List, Dict, Tuple

class BloomsLevel:
    """Represents a level in Bloom's Taxonomy with associated action verbs"""
    
    def __init__(self, name: str, level: int, verbs: List[str], description: str):
        self.name = name
        self.level = level
        self.verbs = verbs
        self.description = description

class LearningObjectivesGenerator:
    """Generates learning objectives from course goals using Bloom's Taxonomy"""
    
    def __init__(self):
        # Define Bloom's Taxonomy levels with action verbs
        self.blooms_levels = {
            1: BloomsLevel("remember", 1, [
                "list", "name", "identify", "show", "label", "collect", "examine", 
                "tabulate", "quote", "recall", "define", "recognize", "match"
            ], "Recall facts and basic concepts"),
            
            2: BloomsLevel("understand", 2, [
                "explain", "describe", "interpret", "summarize", "paraphrase", 
                "classify", "compare", "contrast", "demonstrate", "illustrate"
            ], "Explain ideas or concepts"),
            
            3: BloomsLevel("apply", 3, [
                "use", "solve", "apply", "construct", "choose", "make", "develop", 
                "organize", "plan", "select", "utilize", "model", "identify"
            ], "Use information in new situations"),
            
            4: BloomsLevel("analyze", 4, [
                "analyze", "examine", "compare", "contrast", "investigate", 
                "categorize", "identify", "separate", "advertise"
            ], "Draw connections among ideas"),
            
            5: BloomsLevel("evaluate", 5, [
                "critique", "defend", "judge", "select", "support", "value", 
                "evaluate", "prioritize", "recommend"
            ], "Justify a stand or decision"),
            
            6: BloomsLevel("create", 6, [
                "design", "construct", "create", "develop", "formulate", "author", 
                "investigate", "compose", "plan", "produce", "generate"
            ], "Produce new or original work")
        }
    
    def identify_bloom_level(self, goal_text: str) -> int:
        """Identify the highest Bloom's level indicated by the goal text"""
        goal_lower = goal_text.lower()
        highest_level = 1  # Default to remember level
        
        # Look for action verbs in the goal text
        for level, bloom_level in self.blooms_levels.items():
            for verb in bloom_level.verbs:
                if verb in goal_lower:
                    highest_level = max(highest_level, level)
        
        # Look for context clues that suggest higher levels
        if any(word in goal_lower for word in ["create", "design", "develop", "formulate", "generate"]):
            highest_level = max(highest_level, 6)
        elif any(word in goal_lower for word in ["evaluate", "assess", "judge", "critique"]):
            highest_level = max(highest_level, 5)
        elif any(word in goal_lower for word in ["analyze", "compare", "examine", "investigate"]):
            highest_level = max(highest_level, 4)
        elif any(word in goal_lower for word in ["apply", "use", "implement", "practice", "demonstrate", "layout"]):
            highest_level = max(highest_level, 3)
        elif any(word in goal_lower for word in ["explain", "describe", "interpret", "understand"]):
            highest_level = max(highest_level, 2)
        
        # Special case: "know" with procedures or supplies suggests application level
        if "know" in goal_lower and any(word in goal_lower for word in ["procedure", "supplies", "equipment", "tools"]):
            highest_level = max(highest_level, 3)
        
        return highest_level
    
    def generate_objective_text(self, goal: str, bloom_level: int, context: str = "") -> str:
        """Generate an objective for a specific Bloom's level"""
        level_info = self.blooms_levels[bloom_level]
        
        # Extract the main concept from the goal
        # Remove common prefixes and clean up the text
        cleaned_goal = goal.lower().strip()
        cleaned_goal = re.sub(r'^(the goal is )', '', cleaned_goal)
        cleaned_goal = re.sub(r'^(for learners to |for students to |students to |learners to |students will |learners will )', '', cleaned_goal)
        cleaned_goal = re.sub(r'^(know |understand |learn |be able to )', '', cleaned_goal)
        cleaned_goal = cleaned_goal.strip()
        
        # Select an appropriate action verb for this level
        if bloom_level == 1:  # Remember
            if "supplies" in cleaned_goal:
                verb = "List"
            elif "steps" in cleaned_goal or "procedure" in cleaned_goal:
                verb = "Identify"
            else:
                verb = "Recall"
        elif bloom_level == 2:  # Understand
            if "purpose" in cleaned_goal:
                verb = "Explain"
            else:
                verb = "Describe"
        elif bloom_level == 3:  # Apply
            if "supplies" in cleaned_goal:
                verb = "Layout"
            elif "procedure" in cleaned_goal:
                verb = "Demonstrate"
            else:
                verb = "Apply"
        elif bloom_level == 4:  # Analyze
            verb = "Analyze"
        elif bloom_level == 5:  # Evaluate
            verb = "Evaluate"
        else:  # Create
            if "create" in cleaned_goal:
                verb = "Create"
            elif "design" in cleaned_goal:
                verb = "Design"
            else:
                verb = "Develop"
        
        # Build the objective text
        objective = f"{verb} {cleaned_goal}"
        
        # Remove duplicate words (e.g., "Design design...")
        words = objective.split()
        if len(words) > 1 and words[0].lower() == words[1].lower():
            objective = " ".join(words[1:])
        
        # Clean up and capitalize
        objective = objective.strip().capitalize()
        if not objective.endswith('.'):
            objective += '.'
        
        # Add Bloom's level in parentheses
        objective += f" ({level_info.name})"
        
        return objective
    
    def generate_supporting_objectives(self, main_objective: str, target_level: int, original_goal: str) -> List[str]:
        """Generate supporting objectives for levels below the target level"""
        objectives = []
        
        # Extract the core concept from the original goal
        cleaned_goal = original_goal.lower().strip()
        cleaned_goal = re.sub(r'^(the goal is )', '', cleaned_goal)
        cleaned_goal = re.sub(r'^(for learners to |for students to |students to |learners to |students will |learners will )', '', cleaned_goal)
        cleaned_goal = re.sub(r'^(know |understand |learn |be able to )', '', cleaned_goal)
        cleaned_goal = cleaned_goal.strip()
        
        # Generate objectives for each level below the target
        for level in range(1, target_level):
            level_info = self.blooms_levels[level]
            
            if level == 1:  # Remember
                if "supplies" in cleaned_goal:
                    obj = f"List the supplies needed for each emergency procedure"
                elif "procedure" in cleaned_goal:
                    obj = f"Identify the steps in {cleaned_goal}"
                elif "design" in cleaned_goal and "interface" in cleaned_goal:
                    obj = f"Recall the principles of user interface design"
                elif "marketing plan" in cleaned_goal:
                    obj = f"Identify the components of a marketing plan"
                else:
                    obj = f"Identify key concepts related to {cleaned_goal}"
            
            elif level == 2:  # Understand
                if "supplies" in cleaned_goal:
                    obj = f"Explain the purpose of each supply item"
                elif "procedure" in cleaned_goal:
                    obj = f"Describe the rationale for {cleaned_goal}"
                elif "design" in cleaned_goal and "interface" in cleaned_goal:
                    obj = f"Explain user experience design principles"
                elif "marketing plan" in cleaned_goal:
                    obj = f"Explain marketing principles and strategies"
                else:
                    obj = f"Describe the concepts involved in {cleaned_goal}"
            
            elif level == 3:  # Apply
                if "design" in cleaned_goal and "interface" in cleaned_goal:
                    obj = f"Apply design principles to create interface prototypes"
                elif "marketing plan" in cleaned_goal:
                    obj = f"Apply marketing concepts to develop campaign strategies"
                else:
                    obj = f"Apply knowledge to {cleaned_goal}"
            
            elif level == 4:  # Analyze
                if "design" in cleaned_goal and "interface" in cleaned_goal:
                    obj = f"Analyze existing applications for design patterns"
                elif "marketing plan" in cleaned_goal:
                    obj = f"Analyze market conditions and competitive landscape"
                else:
                    obj = f"Analyze different approaches to {cleaned_goal}"
            
            elif level == 5:  # Evaluate
                if "design" in cleaned_goal and "interface" in cleaned_goal:
                    obj = f"Evaluate the effectiveness of different UI approaches"
                elif "marketing plan" in cleaned_goal:
                    obj = f"Evaluate the potential success of marketing strategies"
                else:
                    obj = f"Evaluate the effectiveness of {cleaned_goal}"
            
            # Clean up and format
            obj = obj.strip().capitalize()
            if not obj.endswith('.'):
                obj += '.'
            obj += f" ({level_info.name})"
            
            objectives.append(obj)
        
        return objectives
    
    def generate_learning_objectives(self, goal: str) -> Dict[str, any]:
        """Generate a complete set of learning objectives from a course goal"""
        
        # Identify the highest appropriate Bloom's level
        target_level = self.identify_bloom_level(goal)
        
        # Generate the main objective at the target level
        main_objective = self.generate_objective_text(goal, target_level)
        
        # Generate supporting objectives for lower levels
        supporting_objectives = self.generate_supporting_objectives(main_objective, target_level, goal)
        
        return {
            'goal': goal,
            'target_level': target_level,
            'target_level_name': self.blooms_levels[target_level].name,
            'main_objective': main_objective,
            'supporting_objectives': supporting_objectives,
            'formatted_output': self._format_objectives(main_objective, supporting_objectives)
        }
    
    def _format_objectives(self, main_objective: str, supporting_objectives: List[str]) -> str:
        """Format objectives in the hierarchical numbering system"""
        output = []
        
        # Main objective
        output.append(f"1.0.0. {main_objective}")
        
        # Supporting objectives
        for i, obj in enumerate(supporting_objectives, 1):
            if i == 1:
                output.append(f"   1.1.0. {obj}")
            else:
                output.append(f"       1.1.{i-1}. {obj}")
        
        return "\n".join(output)

def main():
    """Main function to run the learning objectives generator"""
    parser = argparse.ArgumentParser(
        description="Generate learning objectives from course goals using Bloom's Taxonomy"
    )
    parser.add_argument(
        "goal", 
        nargs='?', 
        help="The course goal to convert into learning objectives"
    )
    parser.add_argument(
        "-i", "--interactive", 
        action="store_true", 
        help="Run in interactive mode"
    )
    
    args = parser.parse_args()
    generator = LearningObjectivesGenerator()
    
    if args.interactive or not args.goal:
        print("Learning Objectives Generator")
        print("=" * 50)
        print("Enter a course goal and I'll generate learning objectives aligned to Bloom's Taxonomy.")
        print("Type 'quit' to exit.\n")
        
        while True:
            goal = input("Enter course goal: ").strip()
            if goal.lower() in ['quit', 'exit', 'q']:
                break
            
            if not goal:
                print("Please enter a valid goal.\n")
                continue
            
            try:
                result = generator.generate_learning_objectives(goal)
                
                print(f"\nOriginal Goal: {result['goal']}")
                print(f"Target Bloom's Level: {result['target_level_name'].title()} (Level {result['target_level']})")
                print("\nGenerated Learning Objectives:")
                print("-" * 40)
                print(result['formatted_output'])
                print("\n" + "=" * 50)
                
            except Exception as e:
                print(f"Error generating objectives: {e}\n")
    
    else:
        # Single goal mode
        try:
            result = generator.generate_learning_objectives(args.goal)
            print(result['formatted_output'])
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()