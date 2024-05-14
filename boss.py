from bs4 import BeautifulSoup
import requests

url = 'https://codeforces.com/contest/1826/problem/A'

response = requests.get(url)

# setup the parser for html
soup = BeautifulSoup(response.text, 'html.parser')

# everything that matters is in this class
problem_statements = soup.find_all(class_='problem-statement')

for statement in problem_statements:
    # title
    title = statement.find(class_='title').text.strip()
    print("Title:", title)
    
    # time limit
    time_limit = statement.find(class_='time-limit').text.strip().replace('time limit per test', '')
    print("Time Limit:", time_limit)
    
    # memory limit
    memory_limit = statement.find(class_='memory-limit').text.strip().replace('memory limit per test', '')
    print("Memory Limit:", memory_limit)
    
    # input format
    input_spec = statement.find(class_='input-specification').text.strip().replace('Input', '')
    print("Input Specification:", input_spec)
    
    # output format
    output_spec = statement.find(class_='output-specification').text.strip().replace('Output', '')
    print("Output Specification:", output_spec)
    
    # sample inputs
    examples = statement.find(class_='sample-tests')
    input_tests = examples.find_all(class_='test-example-line')
    print("Input")
    for i in input_tests: 
        input_example_lines = i.text.strip()
        print(input_example_lines)
    
    # sample outputs
    output_tests = examples.find_all(class_='output')    
    for i in output_tests:  
        output_example_lines = i.text.strip()
        print(output_example_lines)
    
    # extra shit
    note = statement.find(class_='note')
    print(note)
    if note:
        note_text = note.text.strip().replace('Note', '')
        print("Note:", note_text)
    
    print("\n")

