import pandas as pd

# Create a dataset for 50 student records
students = pd.DataFrame({
    'Roll Number': list(range(1, 51)),
    'Name': [
        'Aarav', 'Aditi', 'Aditya', 'Aisha', 'Akash', 'Alia', 'Aman', 'Ananya', 'Anil', 'Anita',
        'Arjun', 'Ashwin', 'Bhavya', 'Chirag', 'Deepak', 'Divya', 'Ekta', 'Gaurav', 'Gina', 'Hitesh',
        'Isha', 'Jatin', 'Kabir', 'Karan', 'Krishna', 'Lakshmi', 'Manish', 'Meera', 'Naina', 'Neha',
        'Nikhil', 'Omkar', 'Pooja', 'Rahul', 'Riya', 'Rohan', 'Sahil', 'Sanya', 'Sara', 'Shreya',
        'Simran', 'Sonam', 'Tarun', 'Tanya', 'Uday', 'Varun', 'Veena', 'Vikram', 'Yash', 'Zara'
    ],
    'Marks': [95, 82, 78, 88, 61, 74, 68, 92, 84, 55, 47, 81, 69, 73, 90, 66, 59, 71, 85, 93,
              88, 77, 64, 79, 83, 60, 89, 54, 91, 38, 42, 72, 56, 87, 96, 80, 49, 67, 70, 58,
              75, 39, 92, 86, 53, 45, 97, 65, 76, 99],
    'Attendance': [85, 92, 78, 88, 91, 83, 70, 95, 89, 60, 54, 82, 67, 75, 94, 73, 68, 76, 90, 93,
                   88, 81, 62, 79, 84, 72, 96, 58, 87, 45, 55, 80, 59, 91, 97, 86, 49, 66, 74, 69,
                   77, 52, 94, 89, 61, 57, 98, 63, 71, 99]
})

# Students scoring above 80
above_80 = students[students['Marks'] > 80]
print('Students scoring above 80:')
print(above_80)
print()

# Students scoring below 35
below_35 = students[students['Marks'] < 35]
print('Students scoring below 35:')
print(below_35)
print()

# Average marks
average_marks = students['Marks'].mean()
print('Average marks:', round(average_marks, 2))
print()

# Top 5 students by marks
top_5 = students.nlargest(5, 'Marks')
print('Top 5 students:')
print(top_5)
print()

# Bottom 5 students by marks
bottom_5 = students.nsmallest(5, 'Marks')
print('Bottom 5 students:')
print(bottom_5)
print()

# Attendance below 75%
attendance_below_75 = students[students['Attendance'] < 75]
print('Students with attendance below 75%:')
print(attendance_below_75)
print()

# Export filtered students into separate CSV
filtered_csv = 'students_filtered.csv'
students[students['Marks'] > 80].to_csv(filtered_csv, index=False)
print(f'Exported students scoring above 80 to {filtered_csv}')
