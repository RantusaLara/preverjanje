import pandas as pd

df_grades = pd.read_csv("raw/students_grades.csv", sep = ",", decimal = ".")
df_school = pd.read_excel("raw/students_school.xlsx")
df_students = pd.read_csv("raw/students.txt", sep = ";", decimal = ".")

df_grades_school = pd.merge(df_grades, df_school, on=['student_id'])
df_merged = pd.merge(df_grades_school, df_students, on=['student_id'])
df_merged['final_grade'] = df_merged[['G1', 'G2', 'G3']].mean(axis=1)
df_merged.to_csv("processed/current_data.csv", sep=';', decimal = ".")