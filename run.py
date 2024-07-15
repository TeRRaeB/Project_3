import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
 
def authorize_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    return client

def open_sheet(client, sheet_name):
    return client.open(sheet_name).list1

def append_answer_to_sheet(sheet, user_name, question_num, user_answer):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([timestamp, user_name, question_num, user_answer])
 
def quiz():
    questions_and_options = [
        ("How do you usually react to unexpected changes in plans?", 
         ["a) With enthusiasm and readiness for new challenges.",
          "b) With irritation, but quickly adapt.",
          "c) Calmly, don't see a problem.",
          "d) With anxiety and worry."]),
        ("How do you spend your free time?", 
         ["a) Actively, attending various events and meetings.",
          "b) Engaging in active sports or hobbies.",
          "c) Reading books or watching movies at home.",
          "d) Prefer calm walks and reflections."]),
        ("How do you behave in conflict situations?", 
         ["a) Try to resolve the conflict peacefully by discussing the problem.",
          "b) Often show aggressiveness and persistence.",
          "c) Try to avoid conflicts and find compromises.",
          "d) Feel insecure and tend to self-analyze."]),
        ("How do you feel about routine work?", 
         ["a) Routine work quickly bores me.",
          "b) I can work routinely if I see the point in it.",
          "c) Routine work doesn't bother me.",
          "d) Often feel tired of routine work."]),
        ("How do you feel in a noisy company?", 
         ["a) I love noisy companies and being the center of attention.",
          "b) I like noisy companies, but sometimes prefer solitude.",
          "c) I prefer quieter and more peaceful gatherings.",
          "d) Feel uncomfortable and try to avoid such situations."]),
        ("How do you perceive criticism?", 
         ["a) I take criticism constructively and strive to improve.",
          "b) Often react emotionally and can argue.",
          "c) Calmly accept criticism and analyze it.",
          "d) Often take criticism to heart and worry."]),
        ("How do you make decisions?", 
         ["a) Quickly, relying on intuition.",
          "b) Quickly, but with some doubts.",
          "c) Slowly and thoughtfully.",
          "d) Slowly and with difficulty, worrying about the consequences."]),
        ("How do you cope with stress?", 
         ["a) Easily, trying to find positive sides.",
          "b) Can be irritable, but quickly calm down.",
          "c) Try to stay calm and find rational solutions.",
          "d) Hardly, often feel strong anxiety."]),
        ("How do you perceive new acquaintances?", 
         ["a) With enthusiasm and interest.",
          "b) With pleasure, but cautiously.",
          "c) Calmly, without much emotion.",
          "d) With some caution and anxiety."]),
        ("How do you handle meeting deadlines?", 
         ["a) Often put off until the last moment, but manage to do it.",
          "b) Try to do it on time, but sometimes delay.",
          "c) Always meet deadlines.",
          "d) Often worry that I won't make it and do it in advance."])
    ]

    client = authorize_google_sheets()
    sheet = open_sheet(client, 'temperament-test')

    while True:
        user_name = input("Please enter your name: ")
        if not user_name:
            continue

        answers = []
        for i, (question, options) in enumerate(questions_and_options):
            print(f"\nQuestion {i+1}: {question}")
            for option in options:
                print(option)
            user_answer = input("Your answer (a, b, c, d) or 0 to quit: ").strip().lower()
            
            if user_answer == '0':
                break
            elif user_answer in ['a', 'b', 'c', 'd']:
                answers.append(user_answer)
                append_answer_to_sheet(sheet, user_name, i+1, user_answer)
            else:
                print("Invalid answer. Please choose a, b, c, d or 0.")
                continue

        if user_answer == '0':
            continue

        result = "".join(answers)
        print(f"\n{user_name}, your answers are: {result}")

        retry = input("Do you want to take the quiz again? (yes/no): ").strip().lower()
        if retry != 'yes':
            break

if __name__ == "__main__":
    quiz()