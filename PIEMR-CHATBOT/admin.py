from flask import Flask , render_template,session
from flask_socketio import SocketIO, emit, send
import model
import json

from textblob import TextBlob

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app,cors_allowed_origins='*')
SESSION_TYPE = 'redis'

f = open('course_branch.json',encoding="utf8")
course_branch = json.load(f)

f = open('branch_fees.json',encoding="utf8")
branch_fees = json.load(f)

all_al = dict(branch_fees)
print('jfaklfgklsngjksnfduiong',all_al['Computer Science & Engineering']['Fees'])
all_branches=list(branch_fees.keys())
all_courses=list(course_branch['courses'].keys())


@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('start')
def handleMessage(msg):
    emit("bot-message",{'message':"Hii! I am a chatbot developed by Deja Vu Hackathon 1.0 "})
    emit("bot-message",{'message':"Do you want to know about Admissions ?",'isOption' : True,'options':['Yes','No']})

def emit_message(a, select_data):
    if a['select']:
        if select_data in all_courses:
            emit("bot-message",{'message':f"Here are the branches provided by us on program {select_data} .", 'isOption' : True,'options': course_branch['courses'][select_data]['branch']})
        elif select_data in all_branches:
            intake=list(branch_fees[select_data])
            intake.remove('branch_importance')
            emit("bot-message",{'message':f"Here are the branches provided by us on program {select_data } {branch_fees[select_data]['branch_importance']} . : ",'isOption' : True,'options': intake})
            session['branch'] = select_data            
            
        elif select_data.lower() == 'yes' or select_data=='Yes':
            emit("bot-message",{'message':"Please select any program : ",'isOption' : True,'options':list(all_courses)})
        elif select_data.lower() == 'no' or select_data=='No':
            emit("bot-message",{'message':f" If you have any queries please ask.",'isOption' : False})
            
        else:
            if a['select_data']=='Fees':
                Fees_session=all_al[session['branch']]['Fees']
                print(session['branch'])
                # print(res)
                emit("bot-message",{'message':f" Fees for {session['branch']} per year {Fees_session}",'isOption' : False,'options':list(all_courses)})
                emit("bot-message",{'message':f" If you have any queries please ask.",'isOption' : False})
            elif a['select_data']=='Intake' :
                intakes_branch=all_al[session['branch']]['Intake']
                emit("bot-message",{'message':f" Intake for {session['branch']} is {intakes_branch} per year.",'isOption' : False,'options':list(all_courses)})
                emit("bot-message",{'message':f" If you have any queries please ask.",'isOption' : False})

    elif a['message'] == 'yes' or a['message'] == 'Yes':
        a['select']=True
        a['message']=select_data
        emit_message(a,select_data)
    else:
        inp = a['message']
        enhanced_input = TextBlob(inp)
        correct_input = str(enhanced_input.correct())
        res =model.chatbot_response(correct_input)
        if res ==None:
            emit("bot-message",{'message':"Sorry but didn't get you, try again.",'isOption' : False})
        else:
            emit("bot-message",{'message':f"{res}",'isOption' : False})
    
    return True

@socketio.on('client-message')
def abc(msg):
    a = msg
    if len(a['message']) == 0:
        select_data=a['select_data']
    else:
        select_data=a['message']
    emit_message(a,select_data)
    
if __name__ == '__main__':
	socketio.run(app)