from celery import Celery
import json

# EMAIL IMPORTS
from celery.schedules import crontab
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta

BACKEND = BROKER = 'redis://localhost:6379'
celery = Celery(__name__, backend=BACKEND, broker=BROKER)

celery.conf.beat_schedule = {
    # Executes every morning at 7:30 a.m.
    'add-every-morning': {
        'task': 'tasks.send_emails',
        'schedule': crontab(hour=7, minute=30)
    },
}
celery.conf.timezone = 'UTC'

# PERIODIC DIGEST
@celery.task
def send_emails():
    """Send periodic digest to all users"""
    email, password = get_config_data()
    server = get_server(email, password)
    # Get all users
    user_tab = get_users()

    result = True
    # Send an email with news to all users
    for user in user_tab:
        msg = prepare_message(user, email)
        try:
            server.sendmail(
                from_addr=email,
                to_addrs=user.email,
                msg=msg.as_string()
            )
        except:
            result = False
            continue

    server.quit()
    return result

def get_config_data():
    with open("config.txt", r) as config:
        data = json.load(config)
        email = data["email"]
        password = data["password"]

    return email, password


def get_server(email, password):
    # STARTING MAIL SERVER
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    try:
        server.login(email, password)
    except:
        raise serverLoginErrorr


def prepare_message(user, email):
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = user.email
    msg['Subject'] = 'SocialDice - News!'
    message = maker_message(user)
    msg.attach(MIMEText(message))
    return msg

def maker_message(user):
    """Make personalized message for each user"""
    text = "Hello "+user.firstname
    followed_list = get_followed_list(user.id)
    if followed_list == []:
        return text+",\n\nYou have no news for today, take a look and add new writers on Sweaggers' SocialDice!"
    else:
        text += ",\n\nhere you can find what's new on the wall of Sweaggers' SocialDice!\n"

    for followed in followed_list:
        # get all stories of a follower posted in the last 24h
        # count them)
        stories_number = len(get_all_stories_by_writer(followed))
        f = get_user(followed)
        # put a line in the text with "<followed_user_name> posts <stories_number> new stories!"
        if stories_number > 0:
            text += "\n - "+f.firstname+" "+f.lastname + \
                " posts "+str(stories_number)+" new stories."

    text += "\n\nSee you on SocialDice,\nSweaggers Team"

    return text


def get_all_stories_by_writer(userid):
    """Get stories by writer id using microservice"""
    # Get stories in the last 24h
    since = datetime.now() - timedelta(hours=24)
    # TODO
    return []


def get_followed_list(userid):
    """Get users followed by userid"""
    #TODO
    return []


def get_user(userid):
    """get the User object from the db"""
    return None


def get_users():
    """Return all the users in the db"""
    return User.query.all()


# EXCEPTIONS
def serverLoginError(Error):
    """Email server login error. Check e-mail or password!"""
    pass