from openai import OpenAI
from dotenv import load_dotenv
import os
import time
import google.generativeai as genai
from transformers import AutoTokenizer, AutoModelForCausalLM
import anthropic
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import csv



def loadModelCosts():
    #Stores the costs of the models in a dictionary
    model_costs = []
    with open('Model_Costs.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            model_costs.append(row)
    return model_costs

def getCostOfModel(model):
    for model_cost in model_costs:
        if model_cost['Model'] == model:
            return [float(model_cost['Cost Per Million Tokens Prompt']),float(model_cost['Cost Per Million Tokens Completion'])]
    else:
        print("Model not found in costs")
        exit()

def useChatGPTToGetAnswerFromLongAnswer(answer):
    #This function is designed to pick the letter from the answer that is returned from Llama and then use that to get the answer from ChatGPT.
    #This is because Llama has a habit of returning the answer in a format that is not just the letter.
    #For instance it might return "The answer is A" instead of just "A"
    # Get the API key from the environment variables
    open_ai_api_key = os.getenv("open_ai_api_key")

    # Create the OpenAI client
    open_ai_client = OpenAI(api_key=open_ai_api_key)

    prompt_setup = "The following statement contains a description and answer to a multiple choice question either (A, B, C, or D). Choose the correct letter that the statement is answering. "
    final_prompt = prompt_setup + answer + ".Your response should be a single letter (A, B, C, or D) nothing else."
    
    # Generate the completion
    response = open_ai_client.chat.completions.create(
        model="gpt-4o",
        temperature=0,
        messages=[
            {"role": "system", "content": "You are an expert attorney."},
            {"role": "user", "content": final_prompt},
        ]
    )
    answer = response.choices[0].message.content
    answer = ''.join(c for c in answer if c.isalpha())

    # If the answer is more than one letter after removing special characters, then there is an error.
    if(len(answer) > 1):
        print("ChatGPT Reading Llama Answer is still more than one letter after removing special characters")
        print(answer)
        exit()
    return answer.strip()


def gemini(question,model):
    gemini_api_key = os.getenv("gemini_api_key")
    genai.configure(api_key=gemini_api_key)
    # List all the models that support the generateContent method
    # for m in genai.list_models():
    #     if 'generateContent' in m.supported_generation_methods:
    #         print(m.name)
    model_config = {
    "temperature": temperature,
    "top_p": top_p,
    }
    model_obj = genai.GenerativeModel(model,generation_config=model_config)
    prompt_setup = "You are an expert attorney. Choose the correct answer to the following question."
    final_prompt = prompt_setup + question + "Your response should be a single letter (A, B, C, or D) nothing else."
    # Get total prompt tokens (including question and ending sentence)
    #There has got to be a better way to get the total tokens than this
    total_tokens = model_obj.count_tokens(final_prompt)
    total_tokens = int(str(total_tokens).split(":")[1].strip())

    #Start the timer so we can get total time.
    start_time = time.time()
    #Generate the content from the prompt
    #For Gemini I need to specify the safety settings or they will block certain questions.
    response = model_obj.generate_content(final_prompt,
        safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    })

    #End timer and calculate duration
    end_time = time.time()
    duration = end_time - start_time
    #print(response)
    #saveFullResponseText(response,question_id,model)

    #Get the cost of the tokens
    cost_per_million_tokens_prompt,cost_per_million_tokens_completion = getCostOfModel(model)


    results_dictionary = {}

    #Gemini had a habit of flagging questions as potentially harmful and not giving the results.
    try:
        answer = response.text
    except Exception as e:
        print(f"Failed to retrieve answer: {e}")
        print(response)
        print(response.candidates[0])
        exit()
    results_dictionary['Original Answer'] = answer.strip()

    # Extract the answer from the response and clean it to remove any special characters.
    # This is needed because sometimes the response may be "A." so we need to remove the .
    answer = ''.join(c for c in answer if c.isalpha()).strip()

    # If the answer is more than one letter after removing special characters, then there is an error.
    if(len(answer) > 1):
        ai_answer = useChatGPTToGetAnswerFromLongAnswer(results_dictionary['Original Answer'])
    else:
        ai_answer = None        
    if(ai_answer != None):
        best_answer = ai_answer
    else:
        best_answer = answer
    
    #Put all the information into a singular dictionary
    results_dictionary["Answer Special Characters Removed"] = answer
    results_dictionary["AI answer"] = ai_answer
    results_dictionary["Best Answer"] = best_answer
    results_dictionary["completion_tokens"] = int(response.candidates[0].token_count) 
    results_dictionary["prompt_tokens"] = total_tokens
    results_dictionary["prompt_cost"] = (results_dictionary["prompt_tokens"] / 1_000_000) * cost_per_million_tokens_prompt
    results_dictionary["completion_cost"] = (results_dictionary["completion_tokens"] / 1_000_000) * cost_per_million_tokens_completion
    results_dictionary["total_tokens"] = results_dictionary["completion_tokens"] + total_tokens
    results_dictionary["total_cost"] = results_dictionary["prompt_cost"] + results_dictionary["completion_cost"]
    results_dictionary["duration"] = duration
    results_dictionary["response"] = str(response)
    return results_dictionary

def chatGPT(question,model):
    # Get the API key from the environment variables
    open_ai_api_key = os.getenv("open_ai_api_key")

    # Create the OpenAI client
    open_ai_client = OpenAI(api_key=open_ai_api_key)

    prompt_setup = "Choose the correct answer to the following question."
    final_prompt = prompt_setup + question + "Your response should be a single letter (A, B, C, or D) nothing else."
    
    # Start the timer so we can get total time.
    start_time = time.time()
    #The o1 models don't support system role.
    if "o1" in model:
            # Generate the completion
        response = open_ai_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": "You are an expert attorney." + final_prompt},
        ]
        )      
    else:
        response = open_ai_client.chat.completions.create(
        model=model,
        temperature=temperature,
        top_p=top_p,
        messages=[
            {"role": "system", "content": "You are an expert attorney."},
            {"role": "user", "content": final_prompt},
        ]
        )


    # End the timer and calculate the duration
    end_time = time.time()
    duration = end_time - start_time
    #saveFullResponseText(response,question_id,model)

    results_dictionary = {}

    # Extract the answer from the response and clean it to remove any special characters.
    # This is needed because sometimes the response may be "A." so we need to remove the .
    answer = response.choices[0].message.content
    results_dictionary['Original Answer'] = answer.strip()

    answer = ''.join(c for c in answer if c.isalpha()).strip()

    # If the answer is more than one letter after removing special characters, then there is an error.
    if(len(answer) > 1):
        ai_answer = useChatGPTToGetAnswerFromLongAnswer(results_dictionary['Original Answer'])
    else:
        ai_answer = None    
    
    #Selects the best answer to use for the final answer.
    #If there is an AI answer then use that, otherwise use the original answer.
    if(ai_answer != None):
        best_answer = ai_answer
    else:
        best_answer = answer
    #Cost of tokens
    cost_per_million_tokens_prompt,cost_per_million_tokens_completion = getCostOfModel(model)

    results_dictionary["Answer Special Characters Removed"] = answer
    results_dictionary["AI answer"] = ai_answer
    results_dictionary["Best Answer"] = best_answer
    results_dictionary["completion_tokens"] = response.usage.completion_tokens
    results_dictionary["prompt_tokens"] = response.usage.prompt_tokens
    results_dictionary["prompt_cost"] = (results_dictionary["prompt_tokens"] / 1_000_000) * cost_per_million_tokens_prompt
    results_dictionary["completion_cost"] = (results_dictionary["completion_tokens"] / 1_000_000) * cost_per_million_tokens_completion
    results_dictionary["total_tokens"] = response.usage.total_tokens
    results_dictionary["total_cost"] = results_dictionary["prompt_cost"] + results_dictionary["completion_cost"]
    results_dictionary["duration"] = duration
    results_dictionary["response"] = str(response)

    return results_dictionary



def llama(question,model):
    # Get the API key from the environment variables
    deepinfra_api_key = os.getenv("deepinfra_api_key")

    # Create the OpenAI client
    llama_client = OpenAI(
        api_key=deepinfra_api_key,
        base_url="https://api.deepinfra.com/v1/openai")

    prompt_setup = "Choose the correct answer to the following question."
    final_prompt = prompt_setup + question + "Your response should be a single letter (A, B, C, or D) nothing else."
    
    # Start the timer so we can get total time.
    start_time = time.time()
    # Generate the completion
    response = llama_client.chat.completions.create(
        model=model,
        temperature=temperature,
        top_p = top_p,
        messages=[
            {"role": "system", "content": "You are an expert attorney."},
            {"role": "user", "content": final_prompt},
        ]
    )
    # End the timer and calculate the duration
    end_time = time.time()
    duration = end_time - start_time
    #saveFullResponseText(response,question_id,model)

    results_dictionary = {}
    

    # Extract the answer from the response and clean it to remove any special characters.
    # This is needed because sometimes the response may be "A." so we need to remove the .
    answer = response.choices[0].message.content
    results_dictionary['Original Answer'] = answer.strip()
    answer_joined = ''.join(c for c in answer if c.isalpha()).strip()

    # If the answer is more than one letter after removing special characters, then there is an error.
    if(len(answer_joined) > 1):
        ai_answer = useChatGPTToGetAnswerFromLongAnswer(results_dictionary['Original Answer'])
    else:
        ai_answer = None

    #Sets the "best answer" this will speed up the human double checking afterwards.
    if(ai_answer != None):
        best_answer = ai_answer
    else:
        best_answer = answer
    
    #Get cost of tokens
    cost_per_million_tokens_prompt,cost_per_million_tokens_completion = getCostOfModel(model)

    results_dictionary["Answer Special Characters Removed"] = answer
    results_dictionary["AI answer"] = ai_answer
    results_dictionary["Best Answer"] = best_answer
    results_dictionary["completion_tokens"] = response.usage.completion_tokens
    results_dictionary["prompt_tokens"] = response.usage.prompt_tokens
    results_dictionary["prompt_cost"] = (results_dictionary["prompt_tokens"] / 1_000_000) * cost_per_million_tokens_prompt
    results_dictionary["completion_cost"] = (results_dictionary["completion_tokens"] / 1_000_000) * cost_per_million_tokens_completion
    results_dictionary["total_tokens"] = response.usage.total_tokens
    #This works but they give us the estimated cost so just go with that.
    #results_dictionary["total_cost"] = results_dictionary["prompt_cost"] + results_dictionary["completion_cost"]
    results_dictionary["total_cost"] = response.usage.estimated_cost
    results_dictionary["duration"] = duration
    results_dictionary["response"] = str(response)

    return results_dictionary



def claude(question,model):
    # Get the API key from the environment variables
    claude_api_key = os.getenv("claude_api_key")
    client = anthropic.Anthropic(api_key=claude_api_key)

    prompt_setup = "Choose the correct answer to the following question."
    final_prompt = prompt_setup + question + "Your response should be a single letter (A, B, C, or D) nothing else."
 
    start_time = time.time()
    message = client.messages.create(
        model=model,
        max_tokens=4096,
        temperature=temperature,
        top_p=top_p,
        system="You are an expert attorney.",
        messages=[
            {"role": "user", "content": final_prompt}
        ]
    )
    end_time = time.time()
    duration = end_time - start_time
    #saveFullResponseText(message,question_id,model)


    answer = message.content[0].text
    results_dictionary = {}
    results_dictionary['Original Answer'] = answer.strip()
    # If the answer is more than one letter after removing special characters, then there is an error.
    answer = ''.join(c for c in answer if c.isalpha()).strip()

    # If the answer is more than one letter after removing special characters, then there is an error.
    if(len(answer) > 1):
        #Use chatgpt to try and get the answer out from Llama.
        ai_answer = useChatGPTToGetAnswerFromLongAnswer(results_dictionary['Original Answer'])
    else:
        ai_answer = None

    if(ai_answer != None):
        best_answer = ai_answer
    else:
        best_answer = answer
    
    #Cost of tokens
    cost_per_million_tokens_prompt,cost_per_million_tokens_completion = getCostOfModel(model)

    results_dictionary["Answer Special Characters Removed"] = answer
    results_dictionary["AI answer"] = ai_answer
    results_dictionary["Best Answer"] = best_answer
    results_dictionary["completion_tokens"] = int(message.usage.output_tokens)
    results_dictionary["prompt_tokens"] = int(message.usage.input_tokens)
    results_dictionary["prompt_cost"] = (results_dictionary["prompt_tokens"] / 1_000_000) * cost_per_million_tokens_prompt
    results_dictionary["completion_cost"] = (results_dictionary["completion_tokens"] / 1_000_000) * cost_per_million_tokens_completion
    results_dictionary["total_tokens"] = results_dictionary["completion_tokens"] + results_dictionary["prompt_tokens"]
    results_dictionary["total_cost"] = results_dictionary["prompt_cost"] + results_dictionary["completion_cost"]
    results_dictionary["duration"] = duration
    results_dictionary["Full Response"] = str(message)



    return results_dictionary

def grok(question,model):
    # Get the API key from the environment variables
    xai_api_key = os.getenv("xai_api_key")

    # Create the OpenAI client
    grok_client = OpenAI(
        api_key=xai_api_key,
        base_url="https://api.x.ai/v1")

    prompt_setup = "Choose the correct answer to the following question."
    final_prompt = prompt_setup + question + "Your response should be a single letter (A, B, C, or D) nothing else."
    
    # Start the timer so we can get total time.
    start_time = time.time()
    # Generate the completion
    response = grok_client.chat.completions.create(
        model=model,
        temperature=temperature,
        top_p = top_p,
        messages=[
            {"role": "system", "content": "You are an expert attorney."},
            {"role": "user", "content": final_prompt},
        ]
    )
    # End the timer and calculate the duration
    end_time = time.time()
    duration = end_time - start_time
    #saveFullResponseText(response,question_id,model)

    results_dictionary = {}
    

    # Extract the answer from the response and clean it to remove any special characters.
    # This is needed because sometimes the response may be "A." so we need to remove the .
    answer = response.choices[0].message.content
    results_dictionary['Original Answer'] = answer.strip()
    answer_joined = ''.join(c for c in answer if c.isalpha()).strip()

    # If the answer is more than one letter after removing special characters, then there is an error.
    if(len(answer_joined) > 1):
        ai_answer = useChatGPTToGetAnswerFromLongAnswer(results_dictionary['Original Answer'])
    else:
        ai_answer = None

    #Sets the "best answer" this will speed up the human double checking afterwards.
    if(ai_answer != None):
        best_answer = ai_answer
    else:
        best_answer = answer
    
    #Get cost of tokens
    cost_per_million_tokens_prompt,cost_per_million_tokens_completion = getCostOfModel(model)

    results_dictionary["Answer Special Characters Removed"] = answer
    results_dictionary["AI answer"] = ai_answer
    results_dictionary["Best Answer"] = best_answer
    results_dictionary["completion_tokens"] = response.usage.completion_tokens
    results_dictionary["prompt_tokens"] = response.usage.prompt_tokens
    results_dictionary["prompt_cost"] = (results_dictionary["prompt_tokens"] / 1_000_000) * cost_per_million_tokens_prompt
    results_dictionary["completion_cost"] = (results_dictionary["completion_tokens"] / 1_000_000) * cost_per_million_tokens_completion
    results_dictionary["total_tokens"] = response.usage.total_tokens
    results_dictionary["total_cost"] = results_dictionary["prompt_cost"] + results_dictionary["completion_cost"]
    results_dictionary["duration"] = duration
    results_dictionary["response"] = str(response)

    return results_dictionary




#Set Default Values
temperature = 0.0
top_p = 0.2


# Load the environment variables from .env file
load_dotenv()
#Load the model costs from a csv and save it as a global variable.
model_costs = loadModelCosts()

