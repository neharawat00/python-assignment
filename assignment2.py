import csv
import statistics 

print("============================================")
print("            GRADEBOOK ANALYZER")
print("============================================")
print("1. Manual Input of Student Marks")
print("2. Load from CSV File")
print("============================================")

while True:

    choice = input("\nChoose an option (1 or 2): ")

    marks = {}     # store {name: marks}

    # ------------------------------------------------
    # Option 1 → Manual entry
    # ------------------------------------------------
    if choice == "1":
        n = int(input("How many students? "))

        for i in range(n):
            name = input(f"Enter name of student {i+1}: ")
            score = int(input("Enter marks: "))
            marks[name] = score

    # ------------------------------------------------
    # Option 2 → CSV input
    # ------------------------------------------------
    elif choice == "2":
        filename = input("Enter CSV filename: ")

        try:
            with open(filename, "r") as file:
                reader = csv.reader(file)
                next(reader)  # skip header

                for row in reader:
                    marks[row[0]] = int(row[1])

        except FileNotFoundError:
            print("File not found! Try again.")
            continue
    else:
        print("Invalid choice. Enter 1 or 2.")
        continue

    # ------------------------------------------------
    # Task 3: Statistical Analysis (NO FUNCTIONS)
    # ------------------------------------------------
    values = list(marks.values())

    average = sum(values) / len(values)
    median = statistics.median(values)

    max_student = max(marks, key=marks.get)
    min_student = min(marks, key=marks.get)

    print("\n=========== STATISTICS ===========")
    print(f"Average Marks: {average:.2f}")
    print(f"Median Marks: {median}")
    print(f"Highest Score: {max_student} → {marks[max_student]}")
    print(f"Lowest Score: {min_student} → {marks[min_student]}")

    # ------------------------------------------------
    # Task 4: Grade assignment (NO FUNCTIONS)
    # ------------------------------------------------
    grades = {}

    for name, score in marks.items():
        if score >= 90:
            grades[name] = "A"
        elif score >= 80:
            grades[name] = "B"
        elif score >= 70:
            grades[name] = "C"
        elif score >= 60:
            grades[name] = "D"
        else:
            grades[name] = "F"

    # Count grade distribution
    grade_count = {
        "A": list(grades.values()).count("A"),
        "B": list(grades.values()).count("B"),
        "C": list(grades.values()).count("C"),
        "D": list(grades.values()).count("D"),
        "F": list(grades.values()).count("F"),
    }

    print("\n=========== GRADE DISTRIBUTION ===========")
    for grade, count in grade_count.items():
        print(f"{grade}: {count}")

    # ------------------------------------------------
    # Task 5: Pass/Fail using list comprehension
    # ------------------------------------------------
    passed = [name for name, score in marks.items() if score >= 40]
    failed = [name for name, score in marks.items() if score < 40]

    print("\n=========== PASS / FAIL REPORT ===========")
    print(f"Passed ({len(passed)}): {passed}")
    print(f"Failed ({len(failed)}): {failed}")

    # ------------------------------------------------
    # Task 6: Final result table
    # ------------------------------------------------
    print("\n=========== FINAL GRADEBOOK TABLE ===========")
    print("Name\t\tMarks\tGrade")
    print("-------------------------------------------")

    for name, score in marks.items():
        print(f"{name}\t\t{score}\t{grades[name]}")

    print("-------------------------------------------")

    # ------------------------------------------------
    # Repeat loop
    # ------------------------------------------------
    again = input("\nDo you want to analyze again? (yes/no): ").lower()
    if again != "yes":
        print("\nThank you for using GradeBook Analyzer! 😊")
        break