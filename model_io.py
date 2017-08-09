import os, markovify, json
def write_model(input_dir, filename, newline = True):
	all_text = ""
	for i in os.listdir(input_dir):
	    with open(input_dir + i) as f:
	        all_text += f.read()
	text_model = markovify.NewlineText(all_text) if newline else markovify.Text(all_text)
	model_json = text_model.to_json()
	with open("{0}.txt".format(filename), 'w') as f:
		json.dump(model_json, f)

def read_model(filename, newline = True):
	filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), "models", "{0}.txt".format(filename)))
	with open(filepath, 'r') as f:
		print('Found file!')
		return markovify.NewlineText.from_json(json.load(f)) if newline else markovify.Text.from_json(json.load(f))
