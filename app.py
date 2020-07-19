from flask import Flask
import random

app = Flask(__name__)

def load_all_questions():
    q_dict = {}
    q_dict["i"] = get_question("data/introvert")
    q_dict["e"] = get_question("data/extrovert")

    q_dict["s"] =  get_question("data/sensing")
    q_dict["n"] =  get_question("data/intuition")

    q_dict["t"] =  get_question("data/thinking")
    q_dict["f"] =  get_question("data/feeling")

    q_dict["j"] =  get_question("data/judging")
    q_dict["p"] =  get_question("data/perceiving")

    return q_dict

def get_question(f):
    my_file = open(f, "r")
    content_list = my_file.readlines()
    return [x.strip().replace('\u00a0', ' ') for x in content_list]

def get_group(offset, fst, scd):
    questions = []

    inv = random.sample(q_dict[fst], 5)
    ext = random.sample(q_dict[scd], 5)
    no = offset

    for i in range(0, 5):
        questions.append({"id": no, "0": inv[i], "1": ext[i]})
        no = no + 1
    
    return questions

def get_questions():
    questions = []

    no = 1
    questions += get_group(no, 'i', 'e')

    no = 6
    questions += get_group(no, 's', 'n')

    no = 11
    questions += get_group(no, 't', 'f')

    no = 16
    questions += get_group(no, 'j', 'p')
    
    return {
        "questions": questions
    }

q_dict = load_all_questions()

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/questions')
def questions():
    return get_questions()

@app.route('/mbti', methods=['POST'])
def mbti():
    return get_questions()

