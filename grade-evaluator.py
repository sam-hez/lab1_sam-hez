#!/usr/bin/env python3

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
        print(f"\033[31mError: The file '{filename}' was not found. \033[0m")
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
        print(f"\033[31mERROR: Missing required column in CSV: {e} \033[0m")
        sys.exit(1)

    except ValueError:
        print("\033[31mERROR: The SCORE and WEIGHT must be numeric values. \033[0m")
        sys.exit(1)

    except Exception as e:
        print(f"\033[31mERROR: An error occurred while reading the file: {e} \033[0m")
        sys.exit(1)

def evaluate_grades(data):
    """
    Evaluates the students' grades by validating scores and weights,
    calculating final grade and GPA, checking pass/fail,
    and identifying the resubmission options
    """
    print("\n\033[32m--- Processing Grades --- \033[0m")

    #Error Handling for empty CSV file
    if not data:
        print("\033[31mERROR: The CSV file is empty. No grades to process. \033[0m")
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
            print(f"\033[31mERROR: '{assignment}' has an invalid score of {score}. The Scores must be between 0 - 100 \033[0m")
            return
        
        # 2. Validate the weight range
        if weight < 0 or weight > 100:
            print(f"\033[31mERROR: '{assignment}' has an invalid weight of {weight}. The Weights must be between 0 - 100 \033[0m")
            return
        
        # 3. Validate the group name
        if group not in ["Formative", "Summative"]:
            print(f"\033[31mERROR: '{assignment}' has an invalid group '{group}'. Use only Formative and Summative groups \033[0m")
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

    # 4. Validate the weights
    if total_weight != 100:
        print(f"\033[31mERROR: Total Weight is {total_weight}, but it must be exactly 100 \033[0m")
        return
        
    if formative_weight != 60:
        print(f"\033[31mERROR: Formative Weight {formative_weight}, but it must be exactly 60 \033[0m")
        return
        
    if summative_weight != 40:
        print(f"\033[31mERROR: Summative Weight is {summative_weight}, but it must be exactly 40 \033[0m")
        return
    
    # 5. Calculate the category percentages 
    formative_percentage = (formative_points / formative_weight) * 100
    summative_percentage = (summative_points / summative_weight) * 100

    # 6. Calculate GPA
    gpa = (total_grade / 100) * 5.0

    #7. Determine the final status
    if formative_percentage >= 50 and summative_percentage >= 50:
        status = "\033[32mPASSED \033[0m"
    else:
        status = "\033[31mFAILED \033[0m"

    # 8. Determine resubmission options
    resubmission_assignments = []

    if failed_formative:
        highest_weight = max(item['weight'] for item in failed_formative)
        resubmission_assignments = [
            item['assignment']
            for item in failed_formative
            if item['weight'] == highest_weight
        ]

    # 9. Print Results
    print(f"\033[32mFinal Grade: {total_grade:.2f}% \033[0m")
    print(f"\033[32mGPA: {gpa:.2f}/5.00 \033[0m") 
    print(f"Formative Percentage: {formative_percentage:.2f}%")
    print(f"Summative Percentage: {summative_percentage:.2f}%")
    print(f"Final Status: {status}")

    if resubmission_assignments:
        print("Eligible Formative Assignment(s) for Resubmission:")
        for assignment in resubmission_assignments:
            print(f"- {assignment}")
    else:
        print("No formative resubmission needed.")

    print("-" * 35)
    print()
    

if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()
    
    # 2. Process the features
    evaluate_grades(course_data)