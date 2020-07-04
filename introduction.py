import random
import json
import time
from textblob import TextBlob

with open('stock_responses.json', 'r') as fp:
    stock_responses = json.load(fp)
with open('people.json', 'r') as fp:
    person_info = json.load(fp)


def intro(s_r, p_info, mood):
    # first greeting depending on the mood
    if mood > 5:
        name = input(random.choice(s_r["good_hellos"]))
    else:
        name = input(random.choice(s_r["bad_hellos"]))
    time.sleep(2)
    # second greeting depending on familiarity
    if name in p_info:
        greeting(name, s_r, mood, 'familiar')
    else:
        # find out information about the user
        inquiry(stock_responses, person_info, name)
        greeting(name, s_r, mood, 'unfamiliar')
    return name


def inquiry(s_r, p_info, name):
    p_info[name] = {"age": 0, "city": 0, "nickname": 0}
    ans = input('Do you have nickname? ')
    if 'yes' in ans.lower() or 'y' in ans.lower():
        nickname = input('what is your nickname: ')
        print('Good to meet you ' + nickname)
    else:
        nickname = name + name[-1] + 'y'
        print('I will call you ' + nickname)
    p_info[name]['nickname'] = nickname
    time.sleep(2)
    p_info[name]['age'] = int(input('How old are you? '))
    time.sleep(1)
    p_info[name]['city'] = input('which city do you live in? ')
    time.sleep(2)
    with open('people.json', 'r') as fp:
        json.dump(p_info, open("people.json", 'w'))


def greeting(name, s_r, mood, familiarity):
    if familiarity == 'familiar':
        response = random.choice(s_r["familiar_greetings"])
    if familiarity == 'unfamiliar':
        response = random.choice(s_r["unfamiliar_greetings"])
    ans = input(response.replace('NAME', name))
    time.sleep(2)
    blob = TextBlob(ans)
    if blob.polarity > 0.1 and mood >= 5:
        print('Glad you are doing well')
    elif blob.polarity > 0.1 and mood <= 5:
        print('Yea yea yea whatever ')
    elif blob.polarity < -0.1:
        print('I feel your pain human')
    else:
        print('Seems like you are OK')
