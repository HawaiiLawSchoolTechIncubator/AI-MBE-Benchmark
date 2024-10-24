import csv
from mc_utilities import *
import os


def writeAnswerToCSV(results):
    # Open the output.csv file in append mode
    with open(filename.replace(".csv","") + '_Answer.csv', 'a', newline='',encoding='utf-8') as file:
        fieldnames = results.keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # Check if the file is empty
        if file.tell() == 0:
            # Write the header row
            writer.writeheader()
        # Write the results as a dictionary
        writer.writerow(results)
def checkIfAlreadyAnswered(question_number,model):
    if not os.path.isfile(filename.replace(".csv","")+'_Answer.csv'):
        return False

    with open(filename.replace(".csv","") + '_Answer.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Question Number'] == question_number and row['Model'] == model:
                return True
    return False
def checkQuestionAgainstAllAis(question,question_number,right_answer,question_category):
    #Check Claude
    ai_platform = "Claude"
    claude_models = ["claude-3-haiku-20240307","claude-3-5-sonnet-20240620","claude-3-opus-20240229"]
    for model in claude_models:
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
        writeAnswerToCSV(results)
        
 
    #Check Gemini
    ai_platform = "Gemini"
    geimin_models = ['gemini-1.0-pro-latest','gemini-1.5-pro-latest','gemini-1.5-flash-latest']
    for model in geimin_models:
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
        writeAnswerToCSV(results)

    #Check ChatGPT models
    ai_platform = "ChatGPT"
    chatGPT_models = ["gpt-3.5-turbo-0125","gpt-4-turbo-2024-04-09","gpt-4-0613","gpt-4o-2024-05-13","gpt-4o-mini-2024-07-18"]
    for model in chatGPT_models:
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
        writeAnswerToCSV(results)



    #Llama
    ai_platform = "Llama"
    llama_models = ["meta-llama/Meta-Llama-3.1-405B-Instruct","meta-llama/Meta-Llama-3.1-70B-Instruct","meta-llama/Meta-Llama-3.1-8B-Instruct","meta-llama/Meta-Llama-3-70B-Instruct","meta-llama/Meta-Llama-3-8B-Instruct"]
    for model in llama_models:
        if(checkIfAlreadyAnswered(question_number,model)):
            continue
        results = llama(question,model)
        results['Question Number'] = question_number
        results['Law Category'] = question_category
        results['Right Answer'] = right_answer
        results['Model'] = model
        results['AI Platform'] = ai_platform
        results['total_cost'] = f"{results['total_cost']:.10f}".rstrip('0').rstrip('.')
        results['prompt_cost'] = f"{results['prompt_cost']:.10f}".rstrip('0').rstrip('.')
        results['completion_cost'] = f"{results['completion_cost']:.10f}".rstrip('0').rstrip('.')
        results['Correct'] = True if results['Right Answer'] == results['Best Answer'] else False
        writeAnswerToCSV(results)
    


filename = 'NCBE MBE Questions.csv'
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
        checkQuestionAgainstAllAis(full_question,question_number,right_answer,question_category)
        time.sleep(1)
        if x > 250:
            break