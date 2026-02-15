import re

medical_records = [
    {
        'patient_id': 'P1001',
        'age': 34,
        'gender': 'Female',
        'diagnosis': 'Hypertension',
        'medications': ['Lisinopril'],
        'last_visit_id': 'V2301',
    },
    {
        'patient_id': 'p1002',
        'age': 17,  # invalid age for testing
        'gender': 'male',
        'diagnosis': 'Type 2 Diabetes',
        'medications': ['Metformin', 'Insulin'],
        'last_visit_id': 'v2302',
    },
    {
        'patient_id': 'P1003',
        'age': 29,
        'gender': 'females',  # invalid gender
        'diagnosis': 'Asthma',
        'medications': ['Albuterol'],
        'last_visit_id': 'v2303',
    },
    {
        'patient_id': 'p1004',
        'age': 56,
        'gender': 'Male',
        'diagnosis': 'Chronic Back Pain',
        'medications': ['Ibuprofen', 'Physical Therapy'],
        'last_visit_id': 'V2304',
    }
]

def find_invalid_records(patient_id, age, gender, diagnosis, medications, last_visit_id):
    constraints = {
        'patient_id': isinstance(patient_id, str) and re.fullmatch('p\d+', patient_id, re.IGNORECASE),
        'age': isinstance(age, int) and age >= 18,
        'gender': isinstance(gender, str) and gender.lower() in ('male', 'female'),
        'diagnosis': isinstance(diagnosis, str) or diagnosis is None,
        'medications': isinstance(medications, list) and all(isinstance(i, str) for i in medications),
        'last_visit_id': isinstance(last_visit_id, str) and re.fullmatch('v\d+', last_visit_id, re.IGNORECASE)
    }
    return [key for key, value in constraints.items() if not value]

def validate(data):
    """
    Validates a list of medical records.
    
    Returns:
        dict: Summary of invalid fields for each record (index as key)
    """
    if not isinstance(data, (list, tuple)):
        print('Invalid format: expected a list or tuple.')
        return None

    invalid_summary = {}  # store all invalid fields by record index
    key_set = {'patient_id', 'age', 'gender', 'diagnosis', 'medications', 'last_visit_id'}

    for index, dictionary in enumerate(data):
        if not isinstance(dictionary, dict):
            invalid_summary[index] = {'error': 'Expected dictionary'}
            continue

        if set(dictionary.keys()) != key_set:
            invalid_summary[index] = {'error': 'Missing or invalid keys'}
            continue

        invalid_records = find_invalid_records(**dictionary)
        if invalid_records:
            invalid_summary[index] = {key: dictionary[key] for key in invalid_records}

    if not invalid_summary:
        print("All records are valid.")
        return {}

    # Print a summary
    print("Summary of invalid records:")
    for idx, errors in invalid_summary.items():
        print(f"Record {idx}: {errors}")

    return invalid_summary

# Run the validator
summary = validate(medical_records)
