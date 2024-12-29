import pandas as pd

input_file = "captions_8k.txt"
output_file = "generated_captions.csv"

with open(input_file, 'r') as f:
    lines = f.readlines()

data = []
for line in lines[1:]:
    if ',' in line:  
        image, caption = line.strip().split(',', 1)
        data.append((image, caption))

df = pd.DataFrame(data, columns=["image", "caption"])

filtered_data = df.groupby("image").last().reset_index()

filtered_data.to_csv(output_file, index=False, header=["image", "caption"])

print(f"Filtered CSV saved to {output_file}")
