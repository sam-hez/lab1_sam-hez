import csv
import sys
import os

def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists, 
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")
    
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
        
    assignments = []
    
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert numeric fields to floats for calculations
                assignments.append({
                    'assignment': row['assignment'],
                    'group': row['group'],
                    'score': float(row['score']),
                    'weight': float(row['weight'])
                })
        return assignments
    
    #CSV Error Handling (missing column in csv & score and weight numeric validation)
    except KeyError as e:
        print(f"ERROR: Missing required column in CSV: {e}")
        sys.exit(1)

    except ValueError:
        print("ERROR: The SCORE and WEIGHT must be numeric values.")
        sys.exit(1)

    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

def evaluate_grades(data):
    """
    Evaluates the students' grades by validating scores and weights,
    calculating final grade and GPA, checking pass/fail,
    and identifying the resubmission options
    """
    print("\n--- Processing Grades ---")

    #Error Handling for empty CSV file
    if not data:
        print("ERROR: The CSV file is empty. No grades to process.")
        return
    
    total_weight = 0
    formative_weight = 0
    summative_weight = 0

    total_grade = 0
    formative_points = 0
    summative_points = 0

    failed_formative = []

    for item in data:
        assignment = item['assignment']
        group = item['group']
        score = item['score']
        weight = item['weight']

        # 1. Validate the score range
        if score < 0 or score > 100:
            print(f"ERROR: '{assignment}' has an invalid score of {score}. The Scores must be between 0 - 100 ")
            return
        
        # 2. Validate the weight range
        if weight < 0 or weight > 100:
            print(f"ERROR: '{assignment}' has an invalid weight of {weight}. The Weights must be between 0 - 100")
            return
        
        # 3. Validate the group name
        if group not in ["Formative", "Summative"]:
            print(f"ERROR: '{assignment}' has an invalid group '{group}'. Use only Formative and Summative groups ")
            return
        
        weighted_score = (score * weight) / 100
        total_grade += weighted_score
        total_weight += weight

        if group == "Formative":
            formative_weight += weight
            formative_points += weighted_score

            if score < 50:
                failed_formative.append(item)
        
        elif group == "Summative":
            summative_weight += weight
            summative_points += weighted_score


        


        
        

    
    # TODO: a) Check if all scores are percentage based (0-100)
    # TODO: b) Validate total weights (Total=100, Summative=40, Formative=60)
    # TODO: c) Calculate the Final Grade and GPA
    # TODO: d) Determine Pass/Fail status (>= 50% in BOTH categories)
    # TODO: e) Check for failed formative assignments (< 50%)
    #          and determine which one(s) have the highest weight for resubmission.
    # TODO: f) Print the final decision (PASSED / FAILED) and resubmission options
    
    pass

if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()
    
    # 2. Process the features
    evaluate_grades(course_data)