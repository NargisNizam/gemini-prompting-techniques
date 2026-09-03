"""
prompts.py
----------
Builds the three prompt variants required by the assignment:
1. Zero-Shot Prompting
2. Few-Shot Prompting
3. Structured Reasoning / Chain-of-Thought Style Prompting

Each function takes a StudentInfo-like object (must have the attributes
name, subject, weak_topics, days_remaining, hours_per_day, skill_level)
and returns a ready-to-send prompt string for the Gemini API.
"""


def _student_block(info) -> str:
    """Common block describing the student, reused across prompts."""
    return (
        f"Student Name: {info.name}\n"
        f"Subject: {info.subject}\n"
        f"Weak Topics: {info.weak_topics}\n"
        f"Exam In: {info.days_remaining} days\n"
        f"Study Time: {info.hours_per_day} hours per day\n"
        f"Skill Level: {info.skill_level}"
    )


def build_zero_shot_prompt(info) -> str:
    """
    Part 1: Zero-Shot Prompting
    Gemini receives the student's information with no prior examples.
    """
    return (
        "Analyze the following student's situation and create a "
        f"{info.days_remaining}-day study plan. Identify the weak topics, "
        "prioritize them, and recommend suitable study activities for each day.\n\n"
        f"{_student_block(info)}"
    )


def build_few_shot_prompt(info) -> str:
    """
    Part 2: Few-Shot Prompting
    Gemini is given 2-3 worked examples before the new student's data,
    so it can match the pattern and format of the response.
    """
    return (
        "You are an AI Study Coach. Study the examples below, then create a "
        "study plan for the new student in the same style and format.\n\n"
        "Example 1\n"
        "Student:\n"
        "A student has an SQL exam in 3 days and struggles mainly with SQL joins.\n\n"
        "Recommended Plan:\n"
        "- Day 1: Study INNER, LEFT, RIGHT, and FULL joins\n"
        "- Day 2: Practice SQL join queries\n"
        "- Day 3: Complete a mock test and review mistakes\n\n"
        "Example 2\n"
        "Student:\n"
        "A student has a Python exam in 7 days and struggles with "
        "Object-Oriented Programming.\n\n"
        "Recommended Plan:\n"
        "- Day 1-2: Classes and objects\n"
        "- Day 3-4: Inheritance and polymorphism\n"
        "- Day 5-6: Coding exercises\n"
        "- Day 7: Final revision and mock test\n\n"
        "Now generate a study plan for this new student:\n\n"
        f"{_student_block(info)}"
    )


def build_structured_prompt(info) -> str:
    """
    Part 3: Structured Reasoning / Chain-of-Thought Style Prompting
    Gemini is instructed to work through the situation systematically
    before giving the final recommendation. We ask for concise
    explanations rather than hidden internal reasoning.
    """
    return (
        "You are an AI Study Coach. Analyze the student's situation "
        "systematically before giving your final recommendation.\n\n"
        f"{_student_block(info)}\n\n"
        "Work through the following steps, and show each step's outcome "
        "briefly before moving to the next:\n"
        "1. Identify the student's weak topics.\n"
        "2. Determine which topics are most important.\n"
        "3. Consider how many days remain before the exam.\n"
        "4. Consider how many hours the student can study per day.\n"
        "5. Recommend suitable learning activities.\n"
        "6. Generate the final day-by-day study plan.\n"
        "7. Give a short explanation for why each activity was selected.\n\n"
        "Do not reveal hidden internal reasoning or a chain of thought. "
        "Present each step as a short, concise summary, ending with the "
        "final structured day-by-day study plan and brief justifications."
    )
