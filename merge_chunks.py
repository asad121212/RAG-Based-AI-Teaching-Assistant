import os       # Provides functions to interact with the operating system
import json     # Used for reading and writing JSON files
import math     # Provides mathematical functions like ceil()

n = 5           # Number of chunks to merge together

# Loop through all files in the 'jsons' directory
for filename in os.listdir('jsons'):
    if filename.endswith('.json'):  # Process only .json files
        file_path = os.path.join('jsons', filename)  # Full path to the file

        # Open and read the JSON file
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)  # Load JSON content into a Python dictionary
            new_chunks = []      # List to store merged chunks

            num_chunks = len(data['chunks'])       # Total number of chunks
            group_chunks = math.ceil(num_chunks / n)  # Number of groups after merging

            # Loop to merge every 'n' chunks together
            for i in range(group_chunks):
                start_index = i * n                         # Start index of current group
                end_index = min((i + 1) * n, num_chunks)    # End index (within limit)

                chunk_group = data['chunks'][start_index:end_index]  # Get the group of chunks

                # Create a merged chunk
                new_chunks.append({
                    "number": data['chunks'][0]['number'],   # Keep same number as first chunk
                    "title": data['chunks'][0]['title'],     # Keep same title as first chunk
                    "start": chunk_group[0]['start'],        # Start time of first chunk
                    "end": chunk_group[-1]['end'],           # End time of last chunk
                    "text": " ".join([chunk['text'] for chunk in chunk_group])  # Merge text
                })

            # Create output folder if not exists
            os.makedirs('merged_jsons', exist_ok=True)

            # Save merged chunks into a new JSON file
            with open(os.path.join('merged_jsons', filename), 'w', encoding='utf-8') as json_file:
                json.dump({"chunks": new_chunks, "text": data['text']}, json_file, indent=4)

            
