import os
from io import StringIO
import ast_node
import py_flowchart
import sys
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/dis')
def dis_python_code():
	py_code = request.args.get('code')
	print(py_code)
	py_code = py_code.replace("(enter)","\r\n")
	py_code = py_code.replace("(tab)","\t")
	py_code = py_code.replace("(add)","+")

	file = open("source_code.txt",'w')
	file.write(py_code)
	file.close()

	file_name = "source_code.txt"
	base = os.path.splitext(file_name)[0]
	os.rename(file_name, base + '.py')

	source_py = "source_code.py"

	try:
		dis_code = ""
		py_2_llc_map = ast_node.parse_pseudo_code(source_py)
		file = open('pseudo_code.txt','r')
		dis_code = file.read()
		file.close()
		
		print(dis_code)	
	except:
		print(sys.exc_info()[0])
		print("The ast tree generated error.")

	return jsonify(code=str(dis_code),map=py_2_llc_map)
 
@app.route('/flowchart')
def fc_python_code():
	py_code = request.args.get('code')
	print(py_code)
	py_code = py_code.replace("(enter)","\r\n")
	py_code = py_code.replace("(tab)","\t")
	py_code = py_code.replace("(add)","+")

	file = open("source_code.txt",'w')
	file.write(py_code)
	file.close()

	file_name = "source_code.txt"
	base = os.path.splitext(file_name)[0]
	os.rename(file_name, base + '.py')

	source_py = "source_code.py"

	try:
		fc_code = ""
		# py_flowchart.parse_flowchart_code(source_py)
		file = open('flowchart.txt','r')
		fc_code = file.read()
		file.close()
		
		print(fc_code)	
	except:
		print(sys.exc_info()[0])
		print("The ast tree generated error.")
	
	# byte_code = compile(source_code, source_py, "exec")
	# dis_code = dis.Bytecode(byte_code).dis()
	# print("Dissembly Code:\n",dis_code)

	# for x in byte_code.co_consts:
	# 	if isinstance(x, types.CodeType):
	# 		sub_byte_code = x
	# 		func_name = sub_byte_code.co_name
	# 		print('\nDisassembly of %s:' % func_name)
	# 		dis.dis(sub_byte_code)

	return jsonify(code=str(fc_code))

@app.route('/flowchart-sample')
def fc_sample():

	py_code = request.args.get('code')
	# print(py_code)

	py_code = "def Module():\n\t"+ py_code
	py_code = py_code.replace("(enter)","\r\n\t")
	py_code = py_code.replace("(tab)","\t\t")
	py_code = py_code.replace("(add)","+")

	file = open("source_code.txt",'w')
	file.write(py_code)
	file.close()

	file_name = "source_code.txt"
	base = os.path.splitext(file_name)[0]
	os.rename(file_name, base + '.py')

	source_py = "source_code.py"

	os.system("python3 pyflowchart/__main__.py {0} --no-simplify > flowchart.txt".format(source_py))
	print("system out",sys.stdout)

	with open('flowchart.txt') as file:
		fc_code = file.read()
	
	print(fc_code)

	return jsonify(code=str(fc_code))
	