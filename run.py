import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re


def authorize_google_sheets():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    return client


def open_sheet(client, sheet_name):
    return client.open(sheet_name).sheet1


def welcome():
    print(
        r"""
        /==========================\ 
        ||+-+-+-+-+-+-+-+-+-+-+-+ ||
        |||T|E|M|P|E|R|A|M|E|N|T| ||
        ||+-+-+-+-+-+-+-+-+-+-+-+ ||
        \==========================/
          """
    )
    print(
        "Temperament is the internal “rhythm” of a person. \nIt affects the speed with which we react to certain situations, \nhow strongly and intensely we experience emotions and determines our activity. \nLet's take the test and find out your temperament.\n \n \n"
    )


def append_row_to_sheet(sheet, row_data):
    sheet.append_row(row_data)


def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


def is_valid_name(name):
    return re.match(r"^[A-Za-z]+(?: [A-Za-z]+)*$", name) is not None


def determine_temperament(result):
    count_a = result.count("a")
    count_b = result.count("b")
    count_c = result.count("c")
    count_d = result.count("d")

    temperament_counts = {"a": count_a, "b": count_b, "c": count_c, "d": count_d}

    max_count = max(temperament_counts.values())
    max_temperaments = [
        key for key, value in temperament_counts.items() if value == max_count
    ]

    if len(max_temperaments) > 1:
        return "Mixed"
    else:
        temperament_map = {
            "a": "Sanguine",
            "b": "Choleric",
            "c": "Phlegmatic",
            "d": "Melancholic",
        }
        return temperament_map[max_temperaments[0]]


def description_temp(temperament):
    temperament_map = {
        "Sanguine": "People who are defined as sanguine are typically extroverted and sociable.\nThey are chipper people who see a glass as half full instead of half empty.\nYou will likely find them in the middle of a crowd and not at the fringes.\nSocial interactions come easy to them, and they can be talkative and energetic.",
        "Choleric": "The defining characteristics of choleric people are dominant and assertive.\nPeople who belong to this temperament type are goal-oriented and driven.\nThey are high achievers at work, school, or even play and are often selected as team leaders.",
        "Phlegmatic": "Laid-back is the word that's likely to come to mind when encountering a phlegmatic person immediately.\nThey are easygoing people who tend to be very empathetic when relating with others.\nThey are dependable and patient people who find comfort in the mundane and routine.",
        "Melancholic": "People often conflate melancholic with joyless or sad,\nbut there's so much more to people with this temperament.\nAlthough reserved, melancholic people are also thoughtful and sensitive.\nThey can also be analytical and methodical, especially at work, making them valuable to any workplace.",
        "Mixed": "The mixed type of temperament represents various parts taken from other temperaments.\nFor a more accurate result, it is better to take a more advanced test.",
    }
    return temperament_map[temperament]


def test():
    questions_and_options = [
        (
            "How do you usually react to unexpected changes in plans?",
            [
                "a) With enthusiasm and readiness for new challenges.",
                "b) With irritation, but quickly adapt.",
                "c) Calmly, don't see a problem.",
                "d) With anxiety and worry.",
            ],
        ),
        (
            "How do you spend your free time?",
            [
                "a) Actively, attending various events and meetings.",
                "b) Engaging in active sports or hobbies.",
                "c) Reading books or watching movies at home.",
                "d) Prefer calm walks and reflections.",
            ],
        ),
        (
            "How do you behave in conflict situations?",
            [
                "a) Try to resolve the conflict peacefully by discussing the problem.",
                "b) Often show aggressiveness and persistence.",
                "c) Try to avoid conflicts and find compromises.",
                "d) Feel insecure and tend to self-analyze.",
            ],
        ),
        (
            "How do you feel about routine work?",
            [
                "a) Routine work quickly bores me.",
                "b) I can work routinely if I see the point in it.",
                "c) Routine work doesn't bother me.",
                "d) Often feel tired of routine work.",
            ],
        ),
        (
            "How do you feel in a noisy company?",
            [
                "a) I love noisy companies and being the center of attention.",
                "b) I like noisy companies, but sometimes prefer solitude.",
                "c) I prefer quieter and more peaceful gatherings.",
                "d) Feel uncomfortable and try to avoid such situations.",
            ],
        ),
        (
            "How do you perceive criticism?",
            [
                "a) I take criticism constructively and strive to improve.",
                "b) Often react emotionally and can argue.",
                "c) Calmly accept criticism and analyze it.",
                "d) Often take criticism to heart and worry.",
            ],
        ),
        (
            "How do you make decisions?",
            [
                "a) Quickly, relying on intuition.",
                "b) Quickly, but with some doubts.",
                "c) Slowly and thoughtfully.",
                "d) Slowly and with difficulty, worrying about the consequences.",
            ],
        ),
        (
            "How do you cope with stress?",
            [
                "a) Easily, trying to find positive sides.",
                "b) Can be irritable, but quickly calm down.",
                "c) Try to stay calm and find rational solutions.",
                "d) Hardly, often feel strong anxiety.",
            ],
        ),
        (
            "How do you perceive new acquaintances?",
            [
                "a) With enthusiasm and interest.",
                "b) With pleasure, but cautiously.",
                "c) Calmly, without much emotion.",
                "d) With some caution and anxiety.",
            ],
        ),
        (
            "How do you handle meeting deadlines?",
            [
                "a) Often put off until the last moment, but manage to do it.",
                "b) Try to do it on time, but sometimes delay.",
                "c) Always meet deadlines.",
                "d) Often worry that I won't make it and do it in advance.",
            ],
        ),
    ]

    client = authorize_google_sheets()
    sheet = open_sheet(client, "temperament-test")
    welcome()
    while True:
        user_name = input("Please enter your full name (example: John Smith): ")
        if not is_valid_name(user_name):
            print(
                "Invalid name. Please enter a valid name without numbers or special characters."
            )
            continue
        clear_terminal()
        answers = [user_name]
        for i, (question, options) in enumerate(questions_and_options):
            while True:
                print(f"\nQuestion {i+1}: {question}")
                for option in options:
                    print(option)
                user_answer = (
                    input("Your answer (a, b, c, d) or 0 to quit: ").strip().lower()
                )

                if user_answer == "0":
                    break
                elif user_answer in ["a", "b", "c", "d"]:
                    answers.append(user_answer)
                    clear_terminal()
                    break
                else:
                    print("Invalid answer. Please choose a, b, c, d or 0.")
                    continue

            if user_answer == "0":
                clear_terminal()
                break

        if user_answer == "0":
            while len(answers) < 11:
                answers.append("-")
            result = "".join(answers[1:])
            answers.append(result)
            append_row_to_sheet(sheet, answers)
            continue

        result = "".join(answers[1:])
        answers.append(result)
        temperament = determine_temperament(result)
        answers.append(temperament)
        append_row_to_sheet(sheet, answers)
        print(f"{user_name}, Your temperament is: {temperament}")
        print(description_temp(temperament))
        retry = input("Do you want to take the test again? (yes): ").strip().lower()
        if retry != "yes":
            break


if __name__ == "__main__":
    test()
