# Learning Objectives Generator

A Python program that helps instructional designers write clear and concise learning objectives aligned to Bloom's Taxonomy levels.

## Features

- Converts course goals into structured learning objectives
- Automatically identifies the appropriate Bloom's Taxonomy level
- Generates hierarchical objectives following the numbering format (1.0.0, 1.1.0, 1.1.1, etc.)
- Creates supporting objectives for each level below the identified target level
- Interactive and command-line modes available

## Bloom's Taxonomy Levels

The program recognizes and generates objectives for all six levels of Bloom's Taxonomy:

1. **Remember** - Recall facts and basic concepts (list, identify, recall)
2. **Understand** - Explain ideas or concepts (explain, describe, interpret)
3. **Apply** - Use information in new situations (apply, demonstrate, layout)
4. **Analyze** - Draw connections among ideas (analyze, compare, examine)
5. **Evaluate** - Justify a stand or decision (evaluate, critique, assess)
6. **Create** - Produce new or original work (create, design, develop)

## Quick Start

The easiest way to get started is with the startup script:

```bash
python3 start.py
```

This will present you with a menu of options to choose from.

## Usage

### Web Interface (Recommended)

The easiest way to use the Learning Objectives Generator is through the web interface:

```bash
python3 simple_web_server.py
```

Then open your browser and go to `http://localhost:8080`

The web interface provides:
- Easy-to-use form for entering course goals
- Example goals you can click to try
- Beautiful formatted results
- No additional dependencies required (uses Python standard library only)

### Command Line Mode

```bash
python3 learning_objectives_generator.py "your course goal here"
```

**Example:**
```bash
python3 learning_objectives_generator.py "the goal is for learners to know the supplies needed for each emergency procedure"
```

**Output:**
```
1.0.0. Layout the supplies needed for each emergency procedure. (apply)
   1.1.0. List the supplies needed for each emergency procedure. (remember)
       1.1.1. Explain the purpose of each supply item. (understand)
```

### Interactive Command Line Mode

```bash
python3 learning_objectives_generator.py -i
```

This will start an interactive session where you can enter multiple course goals and get immediate feedback.

### Advanced Web Interface (Flask-based)

If you have Flask installed, you can also use the more advanced web interface:

```bash
python3 app.py
```

This requires installing Flask:
```bash
pip install Flask==2.3.3
```

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## How It Works

1. **Goal Analysis**: The program analyzes the input goal text to identify action verbs and context clues
2. **Level Identification**: Determines the highest appropriate Bloom's Taxonomy level for the goal
3. **Main Objective Generation**: Creates the primary learning objective at the identified level
4. **Supporting Objectives**: Generates at least one objective for each level below the target level
5. **Formatting**: Outputs objectives in the hierarchical numbering format

## Examples

### Emergency Procedures
**Input:** "the goal is for learners to know the supplies needed for each emergency procedure"
**Output:**
```
1.0.0. Layout the supplies needed for each emergency procedure. (apply)
   1.1.0. List the supplies needed for each emergency procedure. (remember)
       1.1.1. Explain the purpose of each supply item. (understand)
```

### Software Development
**Input:** "students will design a user interface for a mobile application"
**Output:**
```
1.0.0. Design a user interface for a mobile application. (create)
   1.1.0. Recall the principles of mobile UI design. (remember)
       1.1.1. Explain user experience best practices. (understand)
       1.1.2. Apply design principles to mobile interfaces. (apply)
       1.1.3. Analyze existing mobile applications for design patterns. (analyze)
       1.1.4. Evaluate the effectiveness of different UI approaches. (evaluate)
```

## Contributing

This program can be extended to:
- Support additional taxonomy models (e.g., SOLO taxonomy)
- Include domain-specific action verbs
- Generate assessment criteria for each objective
- Export objectives to various formats (PDF, Word, etc.)

## License

This project is open source and available under the MIT License.