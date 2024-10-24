import matplotlib.pyplot as plt
import numpy as np
import csv
from adjustText import adjust_text

# Read data from CSV
AIName = []
Correct = []
with open('Number of Correct Answers by AI Model.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        AIName.append(row['AI Model'])
        Correct.append(int(row['Number of Correct Answers']))

# Add the "Student Average" model
AIName.append('Human Test Taker Average')
Correct.append(148.89)
# Sort AIName and Correct by the number of correct answers
sorted_data = sorted(zip(Correct, AIName), reverse=True)
Correct, AIName = zip(*sorted_data)
# Total number of questions (assuming it's a known constant)
total_number_of_questions = 210

# Data for the bar chart
models = AIName
correct_rates = [(correct / total_number_of_questions) * 100 for correct in Correct]

# Random guessing line and MBE passing range
random_guessing = 25
mbe_passing_range = [58, 67]  # Example range for the passing score

# Colors for different model categories (Red and Blue)
colors = ['#D62728' if model == 'Human Test Taker Average' else '#1F77B4' for model in models]

# Create the figure and axis
fig, ax = plt.subplots(figsize=(10, 12))

# Create the bars without error bars
bars = ax.bar(models, correct_rates, color=colors, capsize=5)

# Add the MBE passing range
plt.fill_between(np.arange(-1, len(models) + 1), mbe_passing_range[0], mbe_passing_range[1], color='gray', alpha=0.2, label='MBE Passing Range')

# Remove the text labels with rounded percentages
# for i, v in enumerate(correct_rates):
#     ax.text(i, v + 2, f'{v:.2f}%', ha='center')

# Add grid, labels, and title
ax.set_title('Percentage of Correct Answers by AI Model', fontsize=18)
ax.set_ylabel('Percentage of Correct Answers', fontsize=16)
ax.set_xlabel('AI Model', fontsize=16)
ax.set_ylim(0, 90)  # Adjusted ylim to give more space above the bars

# Set x-axis labels at a 45 degree angle
plt.xticks(rotation=45, ha='right',fontsize=14)
plt.legend(loc='upper right')
plt.tight_layout()

# Save the plot to the graphs folder
plt.savefig('graphs/percentage_correct_answers_by_ai_model.png')

# Export percentages to a CSV file
with open('Number of Correct Answers By Percentages.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['AI Model', 'Correct Rate (%)'])
    for model, rate in zip(models, correct_rates):
        writer.writerow([model, round(rate, 2)])
