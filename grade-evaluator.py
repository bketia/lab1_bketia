import csv
import sys
import os

def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists,
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ").strip()

    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

    assignments = []

    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            if reader.fieldnames is None:
                print("Error: The CSV file is empty or missing headers.")
                sys.exit(1)

            for row in reader:
                if not any(row.values()):
                    continue

                assignments.append({
                    'assignment': row['assignment'].strip(),
                    'group': row['group'].strip(),
                    'score': float(row['score']),
                    'weight': float(row['weight'])
                })

        if len(assignments) == 0:
            print("Error: The CSV file has no grade records.")
            sys.exit(1)

        return assignments

    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

def validate_scores(data):
    """
    Checks that all scores are between 0 and 100.
    """
    for item in data:
        if item['score'] < 0 or item['score'] > 100:
            print(f"Invalid score found in '{item['assignment']}': {item['score']}")
            return False
    return True

def validate_weights(data):
    """
    Checks:
    - total weight = 100
    - formative weight = 60
    - summative weight = 40
    """
    total_weight = 0
    formative_weight = 0
    summative_weight = 0

    for item in data:
        total_weight += item['weight']

        if item['group'].lower() == "formative":
            formative_weight += item['weight']
        elif item['group'].lower() == "summative":
            summative_weight += item['weight']
        else:
            print(f"Invalid group found: {item['group']}")
            return False

    if total_weight != 100:
        print(f"Weight Error: Total weight is {total_weight}, but it must be 100.")
        return False

    if formative_weight != 60:
        print(f"Weight Error: Formative weight is {formative_weight}, but it must be 60.")
        return False

    if summative_weight != 40:
        print(f"Weight Error: Summative weight is {summative_weight}, but it must be 40.")
        return False

    return True

def calculate_category_totals(data):
    """
    Returns:
    - final weighted total
    - formative percentage out of 100
    - summative percentage out of 100
    """
    final_total = 0
    formative_weighted = 0
    summative_weighted = 0
    formative_weight = 0
    summative_weight = 0

    for item in data:
        weighted_score = (item['score'] * item['weight']) / 100
        final_total += weighted_score

        if item['group'].lower() == "formative":
            formative_weighted += weighted_score
            formative_weight += item['weight']
        elif item['group'].lower() == "summative":
            summative_weighted += weighted_score
            summative_weight += item['weight']

    formative_percent = (formative_weighted / formative_weight) * 100 if formative_weight > 0 else 0
    summative_percent = (summative_weighted / summative_weight) * 100 if summative_weight > 0 else 0

    return final_total, formative_percent, summative_percent

def find_resubmission_options(data):
    """
    Finds failed formative assignments (<50).
    Returns all failed formative assignments with the highest weight.
    """
    failed_formative = []

    for item in data:
        if item['group'].lower() == "formative" and item['score'] < 50:
            failed_formative.append(item)

    if len(failed_formative) == 0:
        return []

    highest_weight = failed_formative[0]['weight']

    for item in failed_formative:
        if item['weight'] > highest_weight:
            highest_weight = item['weight']

    resubmissions = []
    for item in failed_formative:
        if item['weight'] == highest_weight:
            resubmissions.append(item['assignment'])

    return resubmissions

def evaluate_grades(data):
    """
    Main processing function.
    """
    print("\n--- Processing Grades ---")

    # A) Validate scores
    if not validate_scores(data):
        print("Grade validation failed.")
        return

    # B) Validate weights
    if not validate_weights(data):
        print("Weight validation failed.")
        return

    # C) Calculate totals and GPA
    final_grade, formative_percent, summative_percent = calculate_category_totals(data)
    gpa = (final_grade / 100) * 5.0

    # D) Determine Pass/Fail
    passed = formative_percent >= 50 and summative_percent >= 50

    # E) Find resubmission options
    resubmissions = find_resubmission_options(data)

    # F) Print final report
    print(f"Final Grade: {final_grade:.2f}%")
    print(f"Formative Average: {formative_percent:.2f}%")
    print(f"Summative Average: {summative_percent:.2f}%")
    print(f"GPA: {gpa:.2f}")

    if passed:
        print("Final Decision: PASSED")
    else:
        print("Final Decision: FAILED")

        if len(resubmissions) > 0:
            print("Eligible Formative Assignment(s) for Resubmission:")
            for assignment in resubmissions:
                print(f"- {assignment}")
        else:
            print("No formative resubmission options available.")

if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()

    # 2. Process the features
    evaluate_grades(course_data)  