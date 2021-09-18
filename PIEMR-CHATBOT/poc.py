import chat00

reflections = {
  "ami "       : "you are",
  "i was"      : "you were",
  "i"          : "you",
  "i'm"        : "you are",
  "i'd"        : "you would",
  "i've"       : "you have",
  "i'll"       : "you will",
  "my"         : "your",
  "you are"    : "I am",
  "you were"   : "I was",
  "you've"     : "I have",
  "you'll"     : "I will",
  "your"       : "my",
  "yours"      : "mine",
  "you"        : "me",
  "me"         : "you"
}

import json
 
f = open('course_branch.json',)
 
# returns JSON object as
# a dictionary
course_branch = json.load(f)

print(course_branch['courses'].keys())
all_courses=course_branch['courses'].keys()

def rec():
    print("Hi! I am a chatbot created by DAJA VU Hackathon 1.0")
    # chat1 = chat00(pairs, reflections)
    a= 'hello'
    while 1:
        a=input('BOLOO : ')

        chat00.converse(a)
#initiate the conversation
if __name__ == "__main__":
    rec()

