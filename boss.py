from bs4 import BeautifulSoup
import requests
import json
import sys
import stat

url = sys.argv[1]

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

if soup.text == "Just a moment...Enable JavaScript and cookies to continue":
	print("Bypassing anti-scrap protection...")
	scr = soup.findAll("script")[-1].string
	scr = scr[scr.index("var a=toNumbers"):].split(';')
	line = scr[0]
	abc = []
	while "toNumbers" in line:
		i = line.index("toNumbers")
		line = line[i+11:]
		abc.append(line[:line.index('"')])
	from Crypto.Cipher import AES
	def to_numbers(x):
		return bytes(int(x[i:i+2], 16) for i in range(0, len(x), 2))
	key, iv, cipher = map(to_numbers, abc)
	aes = AES.new(key, AES.MODE_CBC, iv)
	rcpc = aes.decrypt(cipher).hex()
	print(f"RCPC = {rcpc}")
	url = scr[-2]
	url = url[url.index('"')+1:-1]
	r = requests.get(url, cookies={"RCPC": rcpc})
	s = r.text
	soup = BeautifulSoup(s, "html.parser")

problem_statements = soup.find_all(class_='problem-statement')

#print(problem_statements)

for statement in problem_statements:
    # title
    title = statement.find(class_='title').text.strip()
    
    # time limit
    time_limit = statement.find(class_='time-limit').text.strip().replace('time limit per test', '')
    
    # memory limit
    memory_limit = statement.find(class_='memory-limit').text.strip().replace('memory limit per test', '')
    
    # input format
    input_spec = statement.find(class_='input-specification').text.strip().replace('Input', '')
    # print("Input Specification:", input_spec)
    
    # output format
    output_spec = statement.find(class_='output-specification').text.strip().replace('Output', '')
    # print("Output Specification:", output_spec)
    
    problem = ""
    for child in statement.children:
        if child.name == 'div' and ('input-specification' in child.get('class', [])):
            break

        if child.name == 'div' and ('header' not in child.get('class', [])):
            problem += child.text.strip()

    # sample inputs
    examples = statement.find(class_='sample-tests')
    input_tests = examples.find_all(class_='test-example-line')

    inputs = ""
    for i in input_tests: 
        input_example_lines = i.text.strip()
        inputs += input_example_lines
        inputs += '\n'
    
    # sample outputs
    output_tests = examples.find_all(class_='output')    
    outputs = ""

    # print(output_tests.text.strip())
    for i in output_tests:  
        output_example_lines = i.text.strip().replace('Output\n', '')
        outputs += output_example_lines
        outputs += '\n'
    
    note = statement.find(class_='note')
    notes = ""

    if note:
        note_text = note.text.strip().replace('Note', '')
        notes += note_text
        # print("Note:", note_text)
    
    data = {
        "title": title,
        "time_limit": time_limit,
        "memory_limit": memory_limit,
        "input_format": input_spec,
        "output_format": output_spec,
        "statement": problem,
        "sample_input": inputs,   
        "sample_outputs": outputs,
        "note": notes
    }

    json_data = json.dumps(data, indent=0)
    print(json_data)
