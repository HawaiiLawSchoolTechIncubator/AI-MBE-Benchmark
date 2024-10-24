import csv
import matplotlib.pyplot as plt
import numpy as np
from adjustText import adjust_text
import matplotlib.pyplot as plt
import numpy as np

# Setting up the datasets to be plotted from the original csv file
AIName = []
Correct = []
AICost = []
AIAverageCost = []
AIValue = []
TempLaw = []
TotalDuration = []
AvgDuration = []
QuestionsAnswered = []
total_number_of_questions = 0

# Opens up the csv file and reads it in as a dictionary
with open("..//Temperature Set to 0 8-27-24//NCBE MBE Questions_Answer_HumanChecked.csv", "r", encoding="utf-8") as csvobj:
    csvreader = csv.DictReader(csvobj)

    # Goes through the csv file and adds an item to the array for each AI model
    for row in csvreader:
        corrected_model_name = row['Model'].replace("meta-llama/", "") #This is to remove the extra meta-llama/ from the model name
        if(corrected_model_name not in AIName):
            AIName.append(corrected_model_name)
            Correct.append(0)
            AICost.append(0)
            TotalDuration.append(0)
            QuestionsAnswered.append(0)
        if(row['Law Category'] not in TempLaw):
            TempLaw.append(row['Law Category'])
    law_categories = {category: [] for category in TempLaw}
    total_number_of_questions = int(row['Question Number'])
    for row in AIName:
        for rows in law_categories:
            law_categories[rows].append(0)

    
    # returns to top of csv file and resets csvreader
    csvobj.seek(0)
    csvreader = csv.DictReader(csvobj)

    # Goes through csv one more time and reads in all the data into the arrays
    for row in csvreader:
        corrected_model_name = row['Model'].replace("meta-llama/", "") #This is to remove the extra meta-llama/ from the model name
        if corrected_model_name in AIName and row['Correct'] == "TRUE":
            Correct[AIName.index(corrected_model_name)] +=1
            law_categories[row['Law Category']][AIName.index(corrected_model_name)] +=1
        AICost[AIName.index(corrected_model_name)] +=float(row['total_cost'])
        TotalDuration[AIName.index(corrected_model_name)] += float(row['duration'])
        QuestionsAnswered[AIName.index(corrected_model_name)]+=1
for number, row in enumerate(TotalDuration):
    AvgDuration.append(row / QuestionsAnswered[number])

for number, row in enumerate(AICost):
    AIAverageCost.append(row/total_number_of_questions)

#Set Universal Font Sizes
title_font = 18
label_font = 16
tick_font = 14

# Correct Answers by AI Model
correct_ai_dictionary = dict(zip(AIName, Correct))
correct_ai_answers = dict(sorted(correct_ai_dictionary.items(), key=lambda x: x[1], reverse=True))
title = 'Number of Correct Answers by AI Model'

# Save the results to a CSV file
with open(f"graphs//{title}.csv", "w", newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['AI Model', 'Number of Correct Answers'])
    for ai_model, correct_answers in correct_ai_answers.items():
        writer.writerow([ai_model, correct_answers])

plt.figure(figsize=(10, 10))  # Increase the figure size
plt.bar(correct_ai_answers.keys(), correct_ai_answers.values())
plt.xlabel('AI Model', fontsize=label_font)  # Set font size for x-axis label
plt.ylabel('Number of Correct Answers', fontsize=label_font)  # Set font size for y-axis label
plt.title(title, fontsize=title_font)  # Set font size for title
plt.xticks(rotation=45, ha='right', fontsize=tick_font)  # Rotate labels, align them to the right, and set font size
plt.yticks(fontsize=tick_font)  # Set font size for y-axis ticks
plt.tight_layout()  # Adjust the layout to prevent cutting off labels
plt.savefig(f"graphs//{title}.png")


# Cost of each AI Model
cost_ai_dictionary = dict(zip(AIName, AIAverageCost))
cost_ai_answers = dict(sorted(cost_ai_dictionary.items(), key=lambda x: x[1], reverse=True))
title = 'Average Cost of Each Question & Answer Query'
plt.figure(figsize=(12, 8))  # Increase the figure width
plt.bar(cost_ai_answers.keys(), cost_ai_answers.values())
plt.xlabel('AI Model', fontsize=label_font)  # Set font size for x-axis label
plt.ylabel('Average Cost (cents)', fontsize=label_font)  # Set font size for y-axis label
plt.title(title, fontsize=title_font)  # Set font size for title
plt.xticks(rotation=45, ha='right', fontsize=tick_font)  # Rotate labels, align them to the right, and set font size
plt.yticks(fontsize=tick_font)  # Set font size for y-axis ticks
plt.tight_layout()  # Adjust layout to prevent cut-off
plt.savefig(f"graphs//{title}.png")




# Cost Scatter Plot
title = "Average Cost vs Number of Correct Answers"
plt.figure(figsize=(12, 8))
plt.scatter(AIAverageCost, Correct)
texts = [plt.text(AIAverageCost[i], Correct[i], AIName[i], fontsize=tick_font + 2) for i in range(len(AIName))]
adjust_text(texts, arrowprops=dict(arrowstyle='-', color='gray'))
plt.xlabel('Average Cost (Cents)', fontsize=label_font)
plt.ylabel('Number of Questions Correct', fontsize=label_font)
plt.title(title, fontsize=title_font)
plt.xticks(fontsize=tick_font)
plt.yticks(fontsize=tick_font)
plt.tight_layout()
plt.savefig(f"graphs//{title}.png")


# Correct Answers by Law Category Vertical
title = 'Number of Correct Answers by AI Model and Law Category'
legal_category_ai_dict = {}

for ai_index, ai_name in enumerate(AIName):
    legal_category_ai_dict[ai_name] = {category: law_categories[category][ai_index] for category in law_categories}

# Calculate total scores for each AI model
total_scores = {ai_model: sum(scores.values()) for ai_model, scores in legal_category_ai_dict.items()}

# Sort AI models by total score in descending order
sorted_ai_models = sorted(total_scores, key=total_scores.get, reverse=True)

# Extract categories
categories = list(next(iter(legal_category_ai_dict.values())).keys())

# Create a figure and axis
fig, ax = plt.subplots(figsize=(12, 15))

# Number of categories and models
n_categories = len(categories)
n_ai_models = len(sorted_ai_models)

# The positions of the bars on the x-axis (now sorted AI models are on the x-axis)
bar_width = 0.1  # Width of each bar
x = np.arange(n_ai_models)  # The x locations for the AI models

# Plotting
for i, category in enumerate(categories):
    values = [legal_category_ai_dict[ai_model][category] for ai_model in sorted_ai_models]
    ax.bar(x + i * bar_width, values, bar_width, label=category)

# Add some labels and a title
ax.set_xlabel('AI Models (sorted by total correct answers)', fontsize=label_font)
ax.set_ylabel('Number of Correct Answers', fontsize=label_font)
ax.set_title(title, fontsize=title_font)
ax.set_xticks(x + bar_width * (n_categories / 2))
ax.set_xticklabels(sorted_ai_models, rotation=45, ha='right', fontsize=label_font)  # Increase font size for x-axis labels
ax.legend(fontsize=label_font)  # Increase font size for legend
ax.tick_params(axis='y', labelsize=tick_font)  # Increase the font size of the ticks on the y-axis
# Adjust layout
plt.tight_layout()
plt.savefig(f"graphs//{title}.png")

# Time spent per question
duration_ai_dictionary = dict(zip(AIName, AvgDuration))
duration_ai_sorted = dict(sorted(duration_ai_dictionary.items(), key=lambda x: x[1], reverse=True))
title = 'Average Query Time Per Question'
plt.figure(figsize=(10, 10))  # Increase the figure size
plt.bar(duration_ai_sorted.keys(), duration_ai_sorted.values())
plt.xlabel('AI Model', fontsize=label_font)  # Set font size for x-axis label
plt.ylabel('Average Query Time (Seconds)', fontsize=label_font)  # Set font size for y-axis label
plt.title(title, fontsize=title_font)  # Set font size for title
plt.xticks(rotation=45, ha='right', fontsize=tick_font)  # Rotate labels, align them to the right, and set font size
plt.yticks(fontsize=tick_font)  # Set font size for y-axis ticks
plt.tight_layout()  # Adjust the layout to prevent cutting off labels
plt.savefig(f"graphs//{title}.png")




# Duration Correct Scatter Plot
title = "Average Query Time vs Number of Correct Answers"
plt.figure(figsize=(12, 8))
plt.scatter(AvgDuration, Correct)
texts = [plt.text(AvgDuration[i], Correct[i], AIName[i], fontsize=tick_font + 2) for i in range(len(AIName))]
adjust_text(texts, arrowprops=dict(arrowstyle='-', color='gray'))
plt.xlabel('Average Query Time (Seconds)', fontsize=label_font)
plt.ylabel('Number of Correct Answers', fontsize=label_font)
plt.title(title, fontsize=title_font)
plt.xticks(fontsize=tick_font)
plt.yticks(fontsize=tick_font)
plt.tight_layout()
plt.savefig(f"graphs//{title}.png")

