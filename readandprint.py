import pandas as pd
import re

# Define column names for each CSV file
department_columns = ['Department_ID', 'Department_Name', 'DOE']
employee_columns = ['Employee_ID', 'DOB', 'DOJ', 'Department_ID']
student_columns = ['Student_ID', 'DOA', 'DOB', 'Department_Choices', 'Department_Admission']
performance_columns = ['Student_ID', 'Semester_Name', 'Paper_ID', 'Paper_Name', 'Marks', 'Effort_Hours']

# Define foreign keys
foreign_keys = {'Employee': 'Department_ID', 'Student': 'Department_Choices', 'Performance': 'Student_ID'}

def validate_clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate and clean the data.
    """
    # Check for missing values
    missing_values = df.isnull().sum()
    print("Missing Values:\n HERE", missing_values)
    


    # Handle missing values
    if 'Marks' in df.columns:
        df['Marks'].fillna(0, inplace=True)  # Replace missing 'Marks' values with 0
        df['Marks'] = df['Marks'].apply(lambda x: re.sub(r'[^0-9.]', '', str(x)))  # Remove non-numeric characters
        df['Marks'] = pd.to_numeric(df['Marks'], errors='coerce')  # Convert 'Marks' column to numeric type
    
    if 'Paper_Name' in df.columns:
        df['Paper_Name'].fillna('Unknown', inplace=True)  # Replace missing 'Paper_Name' values with 'Unknown'

    if 'DOE' in df.columns:
        df.fillna({'DOE': 0}, inplace=True)  # Replace missing 'Marks' values with 0
        df.fillna({'Department_Choices': 'Unknown'}, inplace=True)  # Replace missing 'Department_Choices' values with Unknown
    if 'Department_Admission' in df.columns:
        df.fillna({'Department_Admission': 'Unknown'}, inplace=True)  # Replace missing 'Department_Admission' values with Unknown
    if 'Effort_Hours' in df.columns:
        df['Effort_Hours'].fillna(0, inplace=True)  # Replace missing 'Effort_Hours' values with 0
        df['Marks'] = pd.to_numeric(df['Marks'], errors='coerce')  # Convert 'Effort_Hours' column to numeric type
    return df

def find_effort_hours(df: pd.DataFrame, mark_value: str) -> pd.DataFrame:
    """
    Find columns with 'Effort_Hours' entered as the specified value.
    """
    # Initialize a list to store columns with 'Effort_Hours' entered as the specified value
    columns_with_xx = []
    
    # Iterate over DataFrame columns
    for col in df.columns:
        int= sum
        # Filter the DataFrame for rows where 'Effort_Hours' column has the specified value
        filtered_df = df[df['Effort_Hours'] == mark_value]
        # If any rows are found, add the column name to the list
        if not filtered_df.empty:
            columns_with_xx.append(col)
    
    print("COUNT OF INSTANCE:")
    print(len(filtered_df))
    return columns_with_xx

def main():
    # Load data from CSV files into DataFrames
    department_df = pd.read_csv(r"Department_Information.csv", names=department_columns)
    employee_df = pd.read_csv(r"Employee_Information.csv", names=employee_columns)
    student_df = pd.read_csv(r"Student_Counseling_Information.csv", names=student_columns)
    performance_df = pd.read_csv(r"Student_Performance_Data.csv", names=performance_columns)
    

    # Validate and clean the data
    department_df = validate_clean_data(department_df)
    employee_df = validate_clean_data(employee_df)
    student_df = validate_clean_data(student_df)
    performance_df = validate_clean_data(performance_df)
    print("------------------")
    
    # Perform joins based on foreign keys
    employee_department_df = pd.merge(employee_df, department_df, on='Department_ID', how='left')
    student_department_df = pd.merge(student_df, department_df, left_on='Department_Choices', right_on='Department_ID', how='left')
    student_performance_df = pd.merge(student_df, performance_df, on='Student_ID', how='left')

    # Aggregate the data as needed
    # For example, aggregate performance data by Semester_Name and calculate mean marks
    aggregated_performance_df = performance_df.groupby('Semester_Name')['Marks'].mean().reset_index()




    # Further analysis or transformations as needed
    
    # Print the first few rows of each DataFrame for verification
    print("Employee Department DataFrame:")
    print(employee_department_df.head())
    print("\nStudent Department DataFrame:")
    print(student_department_df.head())
    print("\nStudent Performance DataFrame:")
    print(student_performance_df.head())
    print("\nAggregated Performance DataFrame:")
    print(aggregated_performance_df.head())
    missing_values = department_df.isnull().sum()
    print("Missing Values:\n", missing_values)
    print("Missing Values:\n", missing_values)
    print("Student-Performance:\n",student_performance_df.dtypes)    
    print("Employee-Department:\n",employee_department_df.dtypes)
    print("Student-Department:\n",student_department_df.dtypes)
     # Call the function to find columns with 'Effort_Hours' entered as 'XX'
    columns_with_xx = find_effort_hours(performance_df, '0')

    # Display the columns with 'Effort_Hours' entered as 'XX'
    if columns_with_xx:
        print("Columns with 'Effort_Hours' entered as 'XX':")
        print(columns_with_xx)
    else:
        print("No columns with 'Effort_Hours' entered as 'XX' found.")
    






main()
