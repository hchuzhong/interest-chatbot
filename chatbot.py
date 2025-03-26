import telegram
from telegram.ext import Updater, MessageHandler, Filters
import logging
import os
from dotenv import load_dotenv
from bu_chatgpt import HKBU_ChatGPT
from db import connect_to_db
import datetime

load_dotenv()

def main():
    token = os.getenv('TELEGRAM_ACCESS_TOKEN')
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    global db, client
    db, client = connect_to_db()

    global chatgpt
    chatgpt = HKBU_ChatGPT()
    chatgpt_handler = MessageHandler(Filters.text & (~Filters.command), equip_chatgpt)

    dispatcher.add_handler(chatgpt_handler)

    updater.start_polling()
    updater.idle()

def get_data(update, context):
    user_id = update.message.chat.id
    user = db.users.find_one({"userId": str(user_id)})
    if user:
        return user
    else:
        return None

def equip_chatgpt(update, context):
    global chatgpt
    global db, client

    interests = get_user_interest(update, context)

    if interests:
        cur_user = get_data(update, context)
        if cur_user:
            update_user_interests(update, cur_user, interests)
        else:
            insert_new_user(update, interests)

        user_list = find_users_with_similar_interests(update, interests)
        event_list = find_events_related_to_interests(interests)

        reply_message = format_response(interests, user_list, event_list)
    else:
        # If no interests are detected, send the message directly to ChatGPT
        reply_message = chatgpt.submit(update.message.text)

    logging.info("Update: " + str(update))
    logging.info("Context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)


def update_user_interests(update, cur_user, interests):
    """Update the user's interests in the database."""
    new_interests = cur_user['interests'] + interests
    new_interests = list(set(new_interests))  # Remove duplicates
    db.users.update_one(
        {"userId": str(update.message.chat.id)},
        {"$set": {"interests": new_interests}}
    )


def insert_new_user(update, interests):
    """Insert a new user with their interests into the database."""
    db.users.insert_one({
        "userId": str(update.message.chat.id),
        "interests": interests,
        "username": update.message.chat.first_name,
        "lastUpdated": datetime.datetime.now()
    })


def find_users_with_similar_interests(update, interests):
    """Find users with similar interests."""
    max_users_num = 3
    cur_users_num = 0
    user_list = []

    for interest in interests:
        users = db.users.find({
            "interests": {"$elemMatch": {"$regex": f".*{interest}.*", "$options": "i"}},
            "userId": {"$ne": str(update.message.chat.id)}
        })
        if users:
            for user in users:
                user_list.append({'userId': user['userId'], 'username': user['username']})
                cur_users_num += 1
                if cur_users_num >= max_users_num:
                    break
    return user_list


def find_events_related_to_interests(interests):
    """Find events related to the user's interests."""
    max_events_num = 3
    cur_events_num = 0
    event_list = []

    for interest in interests:
        events = db.events.find({
            "type": {"$regex": f".*{interest}.*", "$options": "i"}
        })
        if events:
            for event in events:
                event_date = datetime.datetime.strptime(event['date'], '%Y-%m-%dT%H:%M:%S.%fZ')
                formatted_date = event_date.strftime('%Y-%m-%d %H:%M:%S')
                event_list.append({'eventId': event['eventId'], 'name': event['name'], 'date': formatted_date})
                cur_events_num += 1
                if cur_events_num >= max_events_num:
                    break
    return event_list


def get_user_interest(update, context):
    try:
        global chatgpt
        template = 'I will provide some sentences, which may related about my interests or not. Please analyze the information and only return the results as a Python string of interests which connected by ";" and " ", use ";" between different interests and use " " in the same interest. If the sentences is not about interests, return a empty string. For example, if I input "I like reading books and go hiking", the return format should be: "reading books;go hiking". Here are my interests: ' + update.message.text
        interests = chatgpt.submit(template)
        # remove the first and last character (quotes)
        interests = interests[1:-1]
        if not interests or interests == '':
            return []
        interests_list = interests.split(';')
        return interests_list
    except Exception as e:
        logging.info('Cannot transfer the interests to list')
        logging.error(e)
        return []

def format_response(user_interests, matched_users, related_events):
    # Convert interest to a readable string (single interest here)
    interest_str = user_interests[0] if user_interests else "your interests"

    # Format matched users
    user_list = "\n- " + "\n- ".join([user["username"] for user in matched_users]) if matched_users else "None found yet!"

    # Format events with readable dates
    event_list = []
    for event in related_events:
        event_list.append(f"- *{event['name']}* - {event['date']}")
    event_str = "\n".join(event_list) if event_list else "No events found right now."

    # Combine into final response
    response = (
        f"Hey! Since you love *{interest_str}*, I found some folks and events you might enjoy:\n\n"
        f"**People who share your vibe:**\n{user_list}\n\n"
        f"**Upcoming Events:**\n{event_str}\n\n"
        f"Feel free to connect with these users or join an event—let me know what you think!"
    )
    return response

if __name__ == '__main__':
    main()