import json

def remove_non_skill_entities(input_file, output_file):
    # Load the JSON data
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Process each entry in the dataset
    cleaned_data = []
    for entry in data:
        text = entry[0]  # The text is the first element of the tuple in your JSON
        annotations = entry[1]["entities"]  # The annotations (entities) are the "entities" field in the second element
        
        # Filter entities to keep only "Skills" entities
        skill_entities = [entity for entity in annotations if entity[2] == "SKILLS"]
        
        # Create the cleaned entry with only "Skills" entities
        cleaned_entry = [text, {"entities": skill_entities}]  # Keep as a tuple-like list
        cleaned_data.append(cleaned_entry)
    
    # Save the cleaned data to a new JSON file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(cleaned_data, f, indent=4)
    
    print(f"Cleaned data saved to {output_file}")

# Example usage
input_file = "dataset.json"  # Replace with your input file name
output_file = "dataset.json"  # Replace with your desired output file name

remove_non_skill_entities(input_file, output_file)