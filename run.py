import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
 
def authorize_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
    client = gspread.authorize(creds)
    return client

def open_sheet(client, sheet_name):
    return client.open(sheet_name).sheet1

def append_row_to_sheet(sheet, row_data):
    sheet.append_row(row_data)

def append_answer_to_sheet(sheet, user_name, question_num, user_answer):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([timestamp, user_name, question_num, user_answer])

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def determine_temperament(result):
    count_a = result.count('a')
    count_b = result.count('b')
    count_c = result.count('c')
    count_d = result.count('d')

    temperament_counts = {
        'a': count_a,
        'b': count_b,
        'c': count_c,
        'd': count_d
    }

    max_count = max(temperament_counts.values())
    max_temperaments = [key for key, value in temperament_counts.items() if value == max_count]

    if len(max_temperaments) > 1:
        return "Mixed"
    else:
        temperament_map = {
            'a': "Sanguine",
            'b': "Choleric",
            'c': "Phlegmatic",
            'd': "Melancholic"
        }
        return temperament_map[max_temperaments[0]]

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

        answers = [user_name]
        for i, (question, options) in enumerate(questions_and_options):
            while True:
                print(f"\nQuestion {i+1}: {question}")
                for option in options:
                    print(option)
                user_answer = input("Your answer (a, b, c, d) or 0 to quit: ").strip().lower()
                
                if user_answer == '0':
                    break
                elif user_answer in ['a', 'b', 'c', 'd']:
                    answers.append(user_answer)
                    clear_terminal()
                    break
                else:
                    print("Invalid answer. Please choose a, b, c, d or 0.")
                    continue

            if user_answer == '0':
                clear_terminal()
                break

        if user_answer == '0':
            while len(answers) < 11:
                answers.append('-')
            result = "".join(answers[1:])
            answers.append(result)
            append_row_to_sheet(sheet, answers)
            continue

        result = "".join(answers[1:])
        answers.append(result)
        temperament = determine_temperament(result)
        answers.append(temperament)
        append_row_to_sheet(sheet, answers)
        print(f"\n{user_name}, your answers are: {result}")
        print(f"Your temperament is: {temperament}")

if __name__ == "__main__":
    quiz()