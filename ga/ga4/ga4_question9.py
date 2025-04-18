import pandas as pd
import pdfplumber
import re

def extract_params_from_question(question: str) -> dict:
    """
    Extracts parameters like subject, minimum marks, group range, and target subject from the question using regex.

    Parameters:
    - question (str): The input question.

    Returns:
    - dict: A dictionary containing the extracted parameters.
    """
    regex_pattern = r"total\s+(\w+)\s+marks\s+of\s+students\s+who\s+scored\s+(\d+)\s+or\s+more\s+marks\s+in\s+(\w+)\s+in\s+groups\s+(\d+)-(\d+)"
    match = re.search(regex_pattern, question, re.IGNORECASE)
    if match:
        target_subject = match.group(1).strip()
        min_marks = int(match.group(2).strip())
        filter_subject = match.group(3).strip()
        group_start = int(match.group(4).strip())
        group_end = int(match.group(5).strip())
        return {
            "target_subject": target_subject,
            "min_marks": min_marks,
            "filter_subject": filter_subject,
            "group_range": (group_start, group_end)
        }
    else:
        raise ValueError("Could not extract parameters from the question.")

def extract_data_from_pdf(pdf_path: str) -> pd.DataFrame:
    """
    Extracts data from a PDF file containing student marks.

    Parameters:
    - pdf_path (str): The path to the PDF file.

    Returns:
    - pd.DataFrame: A DataFrame containing the extracted data.
    """
    data = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            # Detect group number once per page
            group_match = re.search(r"Group\s+(\d+)", text)
            group_number = int(group_match.group(1)) if group_match else None

            if group_number is not None:
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        if len(row) == 5:  # Ensure the row has the expected number of columns
                            clean_row = [group_number] + [cell.strip() if cell else "0" for cell in row]
                            data.append(clean_row)

    # Create DataFrame in one step
    df = pd.DataFrame(data, columns=["Group", "Maths", "Physics", "English", "Economics", "Biology"])
    df = df.apply(pd.to_numeric, errors="coerce").dropna()

    return df

def filter_and_calculate(df: pd.DataFrame, group_range: tuple, filter_subject: str, min_marks: int, target_subject: str) -> float:
    """
    Filters the DataFrame based on the group range and minimum marks, and calculates the total target subject marks.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing student marks.
    - group_range (tuple): The range of groups to filter (start, end).
    - filter_subject (str): The subject to filter students by.
    - min_marks (int): The minimum marks required in the filter subject.
    - target_subject (str): The subject for which the total marks need to be calculated.

    Returns:
    - float: The total marks for the target subject.
    """
    # Filter students based on marks in the filter_subject and group range
    df_filtered = df[
        (df["Group"].between(group_range[0], group_range[1])) &
        (df[filter_subject] >= min_marks)
    ]

    # Calculate the total target_subject marks
    total = df_filtered[target_subject].sum()
    return total

def main(pdf_path: str, question: str) -> float:
    """
    Main function to extract data from the PDF, filter it, and calculate the total marks.

    Parameters:
    - pdf_path (str): The path to the PDF file.
    - question (str): The input question containing the parameters.

    Returns:
    - float: The total marks for the target subject.
    """
    try:
        # Extract parameters from the question
        params = extract_params_from_question(question)

        # Extract data from the PDF
        df = extract_data_from_pdf(pdf_path)

        # Filter and calculate the total marks
        total_marks = filter_and_calculate(
            df,
            group_range=params["group_range"],
            filter_subject=params["filter_subject"],
            min_marks=params["min_marks"],
            target_subject=params["target_subject"]
        )

        return str(total_marks)
    except Exception as e:
        raise RuntimeError(f"An error occurred while processing the PDF: {str(e)}")

