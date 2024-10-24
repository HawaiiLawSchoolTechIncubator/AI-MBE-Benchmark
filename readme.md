# A.I. Model MBE Benchmarking

This project is a benchmarking of different AI models to see which one is the best at solving the multiple choice section of the bar exam known as the Multistate Bar Exam (MBE). 

This study was conducted by the William S. Richardson School of Law. The authors are below.  
- **Matthew Stubenberg**
    - Innovator in Residence - University of Hawaii, William S. Richardson School of Law
- **Chloe Berridge**
    - University of Hawaii, William S. Richardson School of Law Graduate 2024
- **Thomas Fuerst Smith**
    - University of Hawaii, William S. Richardson School of Law Graduate 2025
- **Joshua Casey**
    - University of Hawaii, William S. Richardson School of Law Graduate 2025


## Methodology
The study was conducted on 16 models from Open AI, Google, Meta, and Anthropic. The list of A.I. models used are below. The models were asked to solve 210 sample MBE questions obtained from the National Conference of Bar Examiners at https://store.ncbex.org/mbe-study-aid-download/. For a full explantion of the study please see the full report.

## Models:
- **Open AI**
    - gpt-4o-2024-05-13
    - gpt-4-0613
    - gpt-4-turbo-2024-04-09
    - gpt-4o-mini-2024-07-18
    - gpt-3.5-turbo-0125

- **Google**
    - gemini-1.5-pro-latest
    - gemini-1.5-flash-latest
    - gemini-1.0-pro-latest

- **Meta**
    - Meta-Llama-3.1-405B-Instruct
    - Meta-Llama-3.1-70B-Instruct
    - Meta-Llama-3-70B-Instruct
    - Meta-Llama-3.1-8B-Instruct
    - Meta-Llama-3-8B-Instruct

- **Anthropic**
    - claude-3-5-sonnet-20240620
    - claude-3-opus-20240229
    - claude-3-haiku-20240307

## Results
For a full breakdown please see the full report. The best performer was Antropic's Claude 3.5 Sonnet which answered 181 questions correctly out of 210 possible questions.

![Number of Correct Answers by AI Model](Create%20Graphs/graphs/Number%20of%20Correct%20Answers%20by%20AI%20Model.png)

The full report also contains a breakdown of the number of correct answers by subject matter, cost, duration, and compared to human performance.

## Raw Data
The MBE questions from this study cannot be included publically because they belong to the National Conference of Bar Examiners. However, they can be purchased at https://store.ncbex.org/mbe-study-aid-download/. 

The results of the study are located in the folder results.

## Graphs
The graphs and code to generate the graphs are located in the folder Create Graphs. They were created using the data from the Results folder.

## Follow Up Studies
There are a couple of areas we would like to explore in the future.

- **Prompt Engineering**: Only one prompt template was used for the analysis. Different prompt engineering might yield better performance. Example: Changing the system role from “You are an expert attorney” to “You are a law student taking the bar exam.”

- **Single Run Analysis**: The analysis was conducted only once. Generative AI can produce varying results for the same prompt. Running the analysis multiple times and averaging the results could mitigate this variation.

- **Temperature and Top-p Settings**: The analysis used a temperature of zero and a top-p of 0.2. Different models might perform differently with adjusted settings. Future studies could explore various temperature and top-p values to test this hypothesis.

## Notes
- I had a lot of trouble with getting the lower level llama models to return a single character. I eventually had to check to see if the answer was more than a character and if not then use ChatGPT to determine what the correct letter was. All of these were manually checked for accuracy though.
- I had to turn off Gemini's dangerous content block as it would flag it as potentially offensive.
- Llama is more traditionally known as an LLM that you can launch on a local machine but we are using a service that hosts several llama models call DeepInfra. A different set up could lower costs and time.
