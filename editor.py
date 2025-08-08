from flask import Flask, request, render_template, jsonify
import itertools




app = Flask(__name__)
app.config['USER_GLOBALS'] = {}
app.config['COUNTER'] = itertools.count()





@app.route('/submit', methods=['POST'])
def submit():
	data = request.get_json()
	code_text = data.get('code', '')
	print('Received code:', code_text)
	
	user_globals = app.config['USER_GLOBALS']
	output = exec_user_input(code_text, user_globals)
	app.config['USER_GLOBALS'] = user_globals
	
	return output






def exec_function(user_input):
	try:
		compile(user_input, '<stdin>', 'eval')
	except SyntaxError:
		return exec
	return eval


"""
def exec_user_input(i, user_input, user_globals):
	user_globals = user_globals.copy()
	try:
		retval = exec_function(user_input)(user_input, user_globals)
	except Exception as e:
		return user_globals, f"{e.__class__.__name__}: {e}"
	else:
		if retval is not None:
			return user_globals, f"Out [{i}]: {retval}"
	return user_globals, ""

"""


import itertools
import builtins

def exec_user_input(user_input, user_globals):

	input_counter = itertools.count()
	output_history = []

	# Simulate user input

	if user_input.strip():  # Only run if non-empty
		i = next(input_counter)
		output = []

		# Define a custom print function that captures output
		def custom_print(*args, **kwargs):
			sep = kwargs.get("sep", " ")
			end = kwargs.get("end", "\n")
			output.append(sep.join(map(str, args)) + end)

		# Inject the custom print into globals
		user_globals = user_globals.copy()
		user_globals["print"] = custom_print

		try:
			compiled_code = compile(user_input, "<stdin>", "eval")
			exec_type = eval
		except SyntaxError:
			exec_type = exec

		try:
			retval = exec_type(user_input, user_globals)
		except Exception as e:
			output.append(f"{e.__class__.__name__}: {e}\n")
		else:
			if retval is not None:
				output.append(f"Out [{i}]: {retval}\n")

		# Save prompt and output
#		output_history.append(f"In [{i}]: {user_input}")
#		output_history.extend(output)

		# Print final result using real print
#		print("\n".join(output_history))

#		return "\n".join(output_history)
		return "\n".join(output)




def exec_user_input(user_input, user_globals):
    input_counter = itertools.count()
    output = []

    if user_input.strip():  # Only run if non-empty
        i = next(input_counter)

        def custom_print(*args, **kwargs):
            sep = kwargs.get("sep", " ")
            end = kwargs.get("end", "\n")
            output.append(sep.join(map(str, args)) + end)

        user_globals = user_globals.copy()
        user_globals["print"] = custom_print

        try:
            compiled_code = compile(user_input, "<stdin>", "eval")
            exec_type = eval
        except SyntaxError:
            exec_type = exec

        try:
            retval = exec_type(user_input, user_globals)
        except Exception as e:
            output.append(f"{e.__class__.__name__}: {e}\n")
        else:
            if retval is not None:
                output.append(f"{retval}\n")

    return "".join(output)








@app.route('/', methods=['GET', 'POST'])
def index():
	code = ''
	output = ''
	if request.method == 'POST':
		code = request.form.get('go-to-google', '')
		user_globals = app.config['USER_GLOBALS']
		i = next(app.config['COUNTER'])
		user_globals, output = exec_user_input(i, code, user_globals)
		app.config['USER_GLOBALS'] = user_globals
	return render_template('index.html', code=code, output=output)


"""
@app.route('/run', methods=['POST'])
def run():
    data = request.get_json()
    code = data.get("code", "")
    user_globals = app.config['USER_GLOBALS']
    i = next(app.config['COUNTER'])

    user_globals, output = exec_user_input(i, code, user_globals)
    app.config['USER_GLOBALS'] = user_globals

    return jsonify({
        "input_number": i,
        "output": output
    })
"""


def selected_user_globals(user_globals):

	return (
		(key, user_globals[key])
		for key in sorted(user_globals)
		if not key.startswith('__') or not key.endswith('__')
	)


def save_user_globals(user_globals, path='user_globals.txt'):

	with open(path, 'w') as fd:
		for key, val in selected_user_globals(user_globals):
			fd.write('%s = %s (%s)\n' % (
				key, val, val.__class__.__name__
			))

"""

@app.route('/calculate', methods=['POST'])
def calculate():
	user_globals = {}
	
#	for i, user_input in submit():
#		user_globals = exec_user_input(
#			i, user_input, user_globals
#		)
#		save_user_globals(user_globals)
#		return jsonify({"output": result})
#		return jsonify({"output": exec_user_input(i, user_input, user_globals)})
	


	user_input=submit()
	user_globals = exec_user_input(user_input, user_globals)
	print("user globals",user_globals)
	save_user_globals(user_globals)
	return jsonify({"output": user_globals})

"""



if __name__ == '__main__':
	app.run(debug=True)

