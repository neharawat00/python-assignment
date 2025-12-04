"""
Author: Preet
Date: 19th Sep, 2024
Project: Daily Calorie Tracker CLI
"""

import datetime

def main():
    print("======================================")
    print(" Welcome to the Daily Calorie Tracker ")
    print("======================================")
    print("This tool helps you log meals, track calories, compare with your daily limit,")
    print("and optionally save your session report.\n")

    # Task 2: Input & Data Collection
    meals = []
    calories = []

    num_meals = int(input("How many meals do you want to enter today? "))

    for i in range(num_meals):
        meal_name = input(f"Enter meal {i+1} name: ")
        calorie_amount = float(input(f"Enter calories for {meal_name}: "))
        meals.append(meal_name)
        calories.append(calorie_amount)

    # Task 3: Calorie Calculations
    total_calories = sum(calories)
    avg_calories = total_calories / len(calories)

    daily_limit = float(input("\nEnter your daily calorie limit: "))

    # Task 4: Exceed Limit Warning System
    if total_calories > daily_limit:
        status_message = f"⚠️ Warning: You exceeded your daily limit of {daily_limit} calories!"
    else:
        status_message = f"✅ Good job! You are within your daily limit of {daily_limit} calories."

    # Task 5: Neatly Formatted Output
    print("\n===== Daily Calorie Report =====")
    print("Meal Name\tCalories")
    print("--------------------------------")
    for meal, cal in zip(meals, calories):
        print(f"{meal}\t\t{cal}")
    print("--------------------------------")
    print(f"Total:\t\t{total_calories}")
    print(f"Average:\t{avg_calories:.2f}")
    print(status_message)

    # Task 6 (Bonus): Save Session Log to File
    save_choice = input("\nDo you want to save this report to a file? (yes/no): ").strip().lower()
    if save_choice == "yes":
        filename = "calorie_log.txt"
        with open(filename, "w") as f:
            f.write("===== Daily Calorie Report =====\n")
            f.write(f"Timestamp: {datetime.datetime.now()}\n\n")
            f.write("Meal Name\tCalories\n")
            f.write("--------------------------------\n")
            for meal, cal in zip(meals, calories):
                f.write(f"{meal}\t\t{cal}\n")
            f.write("--------------------------------\n")
            f.write(f"Total:\t\t{total_calories}\n")
            f.write(f"Average:\t{avg_calories:.2f}\n")
            f.write(status_message + "\n")
        print(f"\nReport saved successfully to {filename} ✅")

if __name__ == "__main__":
    main()

