import csv
from mc_utilities import *
import os
from datetime import datetime


def writeAnswerToCSV(results,ai_model):
    # Open the output.csv file in append mode
    results['Timestamp'] = datetime.now().strftime('%Y-%m-%d')
    filename_with_timestamp = filename.replace(".csv", f"_{results['Timestamp']}_" + ai_model + "_Answers.csv")
    with open(filename_with_timestamp, 'a', newline='', encoding='utf-8') as file:
        fieldnames = results.keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # Check if the file is empty
        if file.tell() == 0:
            # Write the header row
            writer.writeheader()
        # Write the results as a dictionary
        writer.writerow(results)
def checkIfAlreadyAnswered(question_number,ai_model):
    #this should probably just return the last question answered.
    #Right now it checks every question one at a time.
    timstamp = datetime.now().strftime('%Y-%m-%d')
    filename_with_timestamp = filename.replace(".csv", f"_{timstamp}_" + ai_model + "_Answers.csv")
    if not os.path.isfile(filename_with_timestamp):
        return False

    with open(filename_with_timestamp, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Question Number'] == question_number and row['Model'] == ai_model:
                print("Already answered: ",question_number,ai_model)
                return True
    return False
def checkAgainstSingleAI(question,question_number,right_answer,question_category,ai_platform,models):
    glama_models = ["o3-mini-2025-01-31","o3-mini-high","o1-2024-12-17","qwen-max","qwen-plus","qwen-turbo","grok-3"]
    if any(item in glama_models for item in models):
        #Glama.ai for certain models
        #This will only work if all the models given are Glama.ai models.
        for model in models:
            if(checkIfAlreadyAnswered(question_number,model)):
                continue
            results = glama(question,model,ai_platform)
            results['Question Number'] = question_number
            results['Law Category'] = question_category
            results['Right Answer'] = right_answer
            results['Model'] = model
            results['AI Platform'] = ai_platform
            results['total_cost'] = f"{results['total_cost']:.10f}".rstrip('0').rstrip('.')
            results['prompt_cost'] = f"{results['prompt_cost']:.10f}".rstrip('0').rstrip('.')
            results['completion_cost'] = f"{results['completion_cost']:.10f}".rstrip('0').rstrip('.')
            results['Correct'] = True if results['Right Answer'] == results['Best Answer'] else False
            writeAnswerToCSV(results,model)
            time.sleep(15)

    #Check ChatGPT models
    elif ai_platform == "ChatGPT":
        for model in models:
            if(checkIfAlreadyAnswered(question_number,model)):
                continue
            results = chatGPT(question,model)
            results['Question Number'] = question_number
            results['Law Category'] = question_category
            results['Right Answer'] = right_answer
            results['Model'] = model
            results['AI Platform'] = ai_platform
            results['total_cost'] = f"{results['total_cost']:.10f}".rstrip('0').rstrip('.')
            results['prompt_cost'] = f"{results['prompt_cost']:.10f}".rstrip('0').rstrip('.')
            results['completion_cost'] = f"{results['completion_cost']:.10f}".rstrip('0').rstrip('.')
            results['Correct'] = True if results['Right Answer'] == results['Best Answer'] else False
            writeAnswerToCSV(results,model)
    elif ai_platform == 'Gemini':
        #Check Gemini
        for model in models:
            if(checkIfAlreadyAnswered(question_number,model)):
                continue
            results = gemini(question,model)
            results['Question Number'] = question_number
            results['Law Category'] = question_category
            results['Right Answer'] = right_answer
            results['Model'] = model
            results['AI Platform'] = ai_platform
            results['total_cost'] = f"{results['total_cost']:.10f}".rstrip('0').rstrip('.')
            results['prompt_cost'] = f"{results['prompt_cost']:.10f}".rstrip('0').rstrip('.')
            results['completion_cost'] = f"{results['completion_cost']:.10f}".rstrip('0').rstrip('.')
            results['Correct'] = True if results['Right Answer'] == results['Best Answer'] else False
            writeAnswerToCSV(results,model)
            #time.sleep(30) #Sleep for 30 seconds to avoid rate limiting (only for gemini 2)
    elif ai_platform == "Grok":
        for model in models:
            if(checkIfAlreadyAnswered(question_number,model)):
                continue
            results = grok(question,model)
            results['Question Number'] = question_number
            results['Law Category'] = question_category
            results['Right Answer'] = right_answer
            results['Model'] = model
            results['AI Platform'] = ai_platform
            results['total_cost'] = f"{results['total_cost']:.10f}".rstrip('0').rstrip('.')
            results['prompt_cost'] = f"{results['prompt_cost']:.10f}".rstrip('0').rstrip('.')
            results['completion_cost'] = f"{results['completion_cost']:.10f}".rstrip('0').rstrip('.')
            results['Correct'] = True if results['Right Answer'] == results['Best Answer'] else False
            writeAnswerToCSV(results,model)
            time.sleep(1)
    elif ai_platform == "Claude":
        for model in models:
            if(checkIfAlreadyAnswered(question_number,model)):
                continue
            results = claude(question,model)
            results['Question Number'] = question_number
            results['Law Category'] = question_category
            results['Right Answer'] = right_answer
            results['Model'] = model
            results['AI Platform'] = ai_platform
            results['total_cost'] = f"{results['total_cost']:.10f}".rstrip('0').rstrip('.')
            results['prompt_cost'] = f"{results['prompt_cost']:.10f}".rstrip('0').rstrip('.')
            results['completion_cost'] = f"{results['completion_cost']:.10f}".rstrip('0').rstrip('.')
            results['Correct'] = True if results['Right Answer'] == results['Best Answer'] else False
            writeAnswerToCSV(results,model)
    elif ai_platform == "Llama" or ai_platform == "DeepSeek":
        #Deepseek and Llama (through DeepInfra)
        for model in models:
            if(checkIfAlreadyAnswered(question_number,model)):
                continue
            results = llama_deepseek(question,model,ai_platform)
            results['Question Number'] = question_number
            results['Law Category'] = question_category
            results['Right Answer'] = right_answer
            results['Model'] = model
            results['AI Platform'] = ai_platform
            results['total_cost'] = f"{results['total_cost']:.10f}".rstrip('0').rstrip('.')
            results['prompt_cost'] = f"{results['prompt_cost']:.10f}".rstrip('0').rstrip('.')
            results['completion_cost'] = f"{results['completion_cost']:.10f}".rstrip('0').rstrip('.')
            results['Correct'] = True if results['Right Answer'] == results['Best Answer'] else False
            writeAnswerToCSV(results,model)


filename = 'NCBE MBE Questions.csv'
#ai_platform = "Alibaba"
ai_platform = "ChatGPT"
models = ["o1-2024-12-17"]
#o1-2024-12-17
#qwen-max
with open(filename, 'r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    for x,row in enumerate(reader):
        #print(row)
        question_number = row['ID']
        question_category = row['Question Category']
        question = row['Question Prompt']
        answer1 = row['Choice A']
        answer2 = row['Choice B']
        answer3 = row['Choice C']
        answer4 = row['Choice D']
        right_answer = row['Correct Answer']
        full_question = f"""{question}
         A) {answer1}
         B) {answer2}
         C) {answer3} 
         D) {answer4}
        """
        #print(full_question)
        print("Question Number: ",question_number)
        #checkQuestionAgainstAllAis(full_question,question_number,right_answer,question_category)
        checkAgainstSingleAI(full_question,question_number,right_answer,question_category,ai_platform,models)
        #time.sleep(15) #This is useful for some gemini experimental models that have limits on how many requests you can make per minute
        if x > 220:
            break