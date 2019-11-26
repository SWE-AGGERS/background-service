from celery import Celery
import json
from flask import Flask, request

from constants import ( 
    USERS_SERVICE_IP, 
    USERS_SERVICE_PORT,
    STORIES_SERVICE_IP,
    STORIES_SERVICE_PORT)

# EMAIL IMPORTS
from celery.schedules import crontab
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta

_app = Flask(__name__)

BACKEND = BROKER = 'redis://localhost:6379'
celery = Celery(__name__, backend=BACKEND, broker=BROKER)


celery.conf.beat_schedule = {
    # Executes every morning at 7:30 a.m.
    'add-every-morning': {
        'task': 'email_digest.send_emails',
        'schedule': crontab(hour=7, minute=30) #30.0 -> if u want every 30 sec
    },
}

celery.conf.timezone = 'UTC'

# PERIODIC DIGEST
@celery.task
def send_emails():
    """Send periodic digest to all users"""
    print("Sending emails...")
    data = get_config_data()
    server = get_server(data)
    # Get all users
    user_tab = get_users()

    result = True
    # Send an email with news to all users
    for user in user_tab:
        msg = prepare_message(user, data["email"])
        try:
            server.sendmail(
                from_addr=data["email"],
                to_addrs=user["email"],
                msg=msg.as_string()
            )
        except:
            result = False
            continue

    server.quit()
    return result

def get_config_data():
    with open("config.txt", "r") as config:
        data = json.load(config)

    return data


def get_server(data):
    # STARTING MAIL SERVER
    server = smtplib.SMTP(str(data["smtp"]), int(data["port"]))
    server.starttls()
    try:
        server.login(str(data["email"]), str(data["password"]))
    except:
        raise Exception('Failed to login to smpt server.')
    return server

def prepare_message(user, email):
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = user["email"]
    msg['Subject'] = 'SocialDice - News!'
    message = maker_message(user)
    msg.attach(MIMEText(message))
    return msg

def maker_message(user):
    """Make personalized message for each user"""
    text = "Hello "+user["firstname"]
    followed_list = get_followed_list(user["user_id"])
    if len(followed_list) == 0:
        return text+",\n\nYou have no news for today, take a look and add new writers on Sweaggers' SocialDice!"
    else:
        text += ",\n\nhere you can find what's new on the wall of Sweaggers' SocialDice!\n"

    for followed in followed_list:
        # get all stories of a follower posted in the last 24h
        # count them)
        stories_number = len(get_all_stories_by_writer(followed))
        f = get_user(followed)[0]
        if f is not None:
            # put a line in the text with "<followed_user_name> posts <stories_number> new stories!"
            if stories_number > 0:
                text += "\n - "+f["firstname"]+" "+f["lastname"] + \
                    " posts "+str(stories_number)+" new stories."

    text += "\n\nSee you on SocialDice,\nSweaggers Team"
    return text


def get_all_stories_by_writer(userid):
    """Get stories by writer id using microservice"""
    # Get stories in the last 24h
    init_date = datetime.now()
    end_date = init_date + timedelta(hours=24)
    _json = {"init_date": init_date, "end_date": end_date, "userid": userid}
    try:
        reply = request.get("https://"+STORIES_SERVICE_IP+":"+STORIES_SERVICE_PORT+"/stories/filter", json=_json, timeout=1)
        result = json.load(reply.data)
    except:
        print("Error on /stories/filter api call")
        return []

    if result["result"] == 1:
        return result["stories"]
    elif result["result"] == 0:
        return []
    else:
        print("Error "+result["result"]+" from /stories/filter api call")

    return []



def get_followed_list(userid):
    """Get users followed by userid"""
    try:
        reply = request.get("https://"+USERS_SERVICE_IP+":"+USERS_SERVICE_PORT+"/followed/list/"+str(userid), timeout=1)
        result = json.load(reply.data)["followed"]
    except:
        result = []
        print("Error on /followed/list/<userid> api connection!")
    return result


def get_user(userid):
    """get the User object from the db"""
    try:
        reply = request.get("https://"+USERS_SERVICE_IP+":"+USERS_SERVICE_PORT+"/user/"+str(userid), timeout=1)
        result = json.load(reply.data)
    except:
        print("Error on /user/<userid> api connection!")
        return None

    return result


def get_users():
    """Return all the users in the db"""
    try:
        reply = request.get("https://"+USERS_SERVICE_IP+":"+USERS_SERVICE_PORT+"/users", timeout=1)
        result = json.load(reply.data)
    except:
        result = []
        print("Error on /users api connection!")
    return result
