import pyttsx3
import os
import random
import re
from datetime import datetime
import json

file = None
os.chdir('c:\\Users\\Kuba\\Desktop\\Nowy folder (4)')


engine = pyttsx3.init()
engine.setProperty("voice","IDHKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_PL-PL_PAUL")
engine.setProperty("rate", 250)
rate = engine.getProperty("rate")

#voices = engine.getProperty("voices")

# Lista pytań wywiadu medycznego
questions = [
    "Jak się dzisiaj czujesz?",
    "Czy masz gorączkę? Jeśli tak, od jak dawna?",
    "Czy odczuwasz ból? Jeśli tak, w jakiej części ciała?",
    "Czy występuję kaszel? Suchy czy mokry?",
    "Czy występują inne objawy, takie jak zmęczenie, nudności lub wysypka?",
    "Czy przyjmujesz jakieś leki?",
    "Czy cierpisz na choroby przewlekłe?",
]

# Lista pytań terapeutycznych
therapy_questions = [
    "Jak się teraz czujesz emocjonalnie?",
    "Czy jest coś, co szczególnie Cię niepokoi?",
    "Czy masz jakieś trudności w codziennym życiu?",
    "Co Cię obecnie stresuje?",
    "Jakie są Twoje cele lub marzenia na przyszłość?",
]

# Słownik przechowujący odpowiedzi pacjenta
responses = {
    "timestamp": str(datetime.now()),
    "answers": {}
}

# Dodatkowy słownik do przechowywania odpowiedzi z terapii
therapy_responses = {
    "timestamp": str(datetime.now()),
    "therapy_answers": {}
}
def save_combined_report_to_file(report, therapy_report, filename="raport.txt"):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            now = datetime.now()
            print(now)
            file.write(f'{now: %d-%m-%Y  %H:%M}'+ "---- Raport z wywiadu medycznego i terapii: \n")
            file.write("=" * 50 + "\n\n")
            file.write(report + "\n")
            file.write("=" * 50 + "\n")
            file.write(therapy_report + "\n")
        print(f"Raport został zapisany do pliku: {filename}")
    except Exception as e:
        print(f"Wystąpił błąd podczas zapisywania raportu: {e}")

# prosta logika AI do odpowiadania na pytania
def simple_ai_response(user_input, is_last_question = False):
    global questions
    # Lista słów kluczowych do prostych odpowiedzi
    positive_responses = ['dobrze', 'swietnie', 'ok', 'w porządku','nawet dobrze', 'fantastycznie', 'bardzo dobrze', 
    'super', 'genialnie', 'nie mam kaszlu', 'nie mam gorączki',  'nie cierpię', ' nie występują', 'nie występuję', 'nie']
    negative_responses = ['źle', 'słabo', 'nie dobrze', 'złe', 'boli', 'bolą mnie plecy','przykro', 'przykre','mam kaszel suchy',
    'mam kaszel mokry', 'mam goraczke', 'cierpię', 'występują', 'występuję']

    #Słowniki
    positive_dictionary_ai_answers = ['Miło to słyszeć', 'To wspaniała wiadomość', 'Wspaniale', 'Tak trzymaj', 'Bardzo się cieszę']
    negative_dictionary_ai_answers = ['Przykro mi to słyszeć', 'Mam nadzieję że będzie lepiej', ' To nie zbyt dobrze', ]
    
    # Dopasowanie odpowiedzi na podstawie słów 
    

    if any(word in user_input.lower() for word in positive_responses):
        random_element = random.choice(positive_dictionary_ai_answers)
        return random_element
    elif any(word in user_input.lower() for word in negative_responses):
        random_element1 = random.choice(negative_dictionary_ai_answers)
        return random_element1
    elif not is_last_question:
        print("Przejdźmy do następnego pytania")
        engine.say("Przejdźmy do następnego pytania")
        engine.runAndWait()
    else:
        return ""

    
def validate_text_input(input_text):
    # Sprawdzanie, czy odpowiedź zawiera tylko litery i spacje (no digits, no special characters)
    if re.match("^[,A-Za-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ ]+$", input_text):
        return True
    else:
        return False


# Funkcja do generowania raportu z wywiadu medycznego
def generate_report(responses):
    with open('doctors.json', encoding='UTF-8') as json_file:
        content = json.load(json_file)
        print("Oto lista lekarzy w twoim mieście\n") 
        for row in content:
            print(f'Imie i nazwisko: {row['name']}\n')
            print(f'Adres: {row['addres']}\n')       # DODAĆ FUNKCJE Z DOSTĘPNYMI LEKARZAMI
            print(f'Specjalizacje: {row['specials']}\n')       # DODAĆ FUNKCJE Z DOSTĘPNYMI LEKARZAMI
    report = "Podsumowanie wywiadu medycznego:\n\n"
    for question, answer in responses["answers"].items():
        report += f"{question}\n {answer}\n\n"
    report +=("Dziękujemy za wypełnienie wywiadu. Skontaktuj się z lekarzem w razie potrzeby.")
    engine.say("Dziękujemy za wypełnienie wywiadu. Skontaktuj się z lekarzem w razie potrzeby.")
    engine.runAndWait()
    return report


# Funkcja do generowania raportu z terapii
def generate_therapy_report(therapy_responses):
    report = "Podsumowanie sesji terapeutycznej:\n\n"
    for question, answer in therapy_responses["therapy_answers"].items():
        report += f"{question}\n {answer}\n\n"
    report += ("Dziękujemy za sesję terapeutyczną. Pamiętaj, że możesz wrócić do rozmowy w każdej chwili.")
    engine.say("Dziękujemy za sesję terapeutyczną. Pamiętaj, że możesz wrócić do rozmowy w każdej chwili.")
    engine.runAndWait()
    return report

# funkcja wypisywania metody relaksu
# def relax_method():
#     try:
#         with open('relaxing_methods.txt', 'r', encoding='UTF-8') as file:
#             video_link = "https://www.youtube.com/watch?v=X1HXg6BkKw0 "
#             print("Przykro mi to słyszeć")
#             engine.say("Przykro mi to słyszeć")
#             engine.runAndWait()
#             print()
#             print(f'Polecam obejrzeć ten 25 minutowy filmik: {video_link}\n')
#             engine.say("Polecam obejrzeć ten 25 minutowy filmik")
#             engine.runAndWait()
#             content = file.read()
#             print(content)
#             print("Możemy kontynuować naszą rozmowę.")
#             engine.say("Możemy kontynuować naszą rozmowę.")
#             engine.runAndWait()
#             file.close()
#     except Exception:
#         pass
        #print("Nie znaleziono pliku")

# Funkcja do prowadzenia wywiadu medycznego i terapeutycznego

def get_patient_name(min_length=3):
    while True:
        try:
            name = input("Proszę podać swoje imię (min. 3 znaki): ").strip()
            # Sprawdzamy długość imienia
            if len(name) < min_length:
                print(f"Imię jest za krótkie. Proszę podać imię, które ma co najmniej {min_length} znaki.")
                continue
            # Sprawdzamy, czy imię zawiera tylko litery
            if not name.isalpha():
                print("Imię może zawierać tylko litery. Spróbuj ponownie.")
                continue
            # Jeśli imię jest poprawne, zwracamy je
            return name.capitalize()
        except Exception as e:
            print(f"Wystąpił błąd: {e}. Spróbuj ponownie.")


def start_interview():
    global responses, therapy_responses

    print("Witaj! Jestem Twoim botem medycznym.")
    engine.say("Witaj! Jestem Twoim botem medycznym.")
    engine.runAndWait()
    try:
        patient_name = get_patient_name()
        print(f'Miło mi cię poznać {patient_name.capitalize()}')
        engine.say(f'Miło mi cię poznać {patient_name.capitalize()}')
        engine.runAndWait()
    except ValueError:
        print("Używaj tylko liter :) ")


    print("Czy chcesz rozpocząć wywiad medyczny?) (tak/nie)")
    engine.say("Czy chcesz rozpocząć wywiad medyczny?) (tak/nie)")
    engine.runAndWait()


    while True:
        user_input = input("Wpisz 'tak', aby kontynuować lub 'nie', aby zakończyć: ").lower()
        if user_input == 'tak':
            # Rozpoczynamy wywiad medyczny
            for i, question in enumerate(questions):
                while True:
                    engine.say(question)
                    engine.runAndWait()

                    user_answer = input(f"{question} ")
                    if not validate_text_input(user_answer):
                        print("Nieprawidłowa odpowiedź. Proszę podać odpowiedź tekstową, składającą się tylko z liter.\n")
                        continue

                    responses["answers"][question] = user_answer
                    #ai_response = simple_ai_response(user_answer)
                    #print(f"AI: {ai_response}")  # Odpowiedź AI do pacjenta
                    #break
                    if "przyjmujesz jakieś leki" in question.lower() and user_answer.lower() in ["tak"]:
                        engine.say("Jakie leki przyjmujesz?")
                        engine.runAndWait()
                        medications = input("Jakie leki przyjmujesz? ")
                        responses["answers"]["Przyjmowane leki"] = medications
                        print("AI: Dziękuję za informację o przyjmowanych lekach.")
                        engine.say("Dziękuję za informację o przyjmowanych lekach.")
                        engine.runAndWait()

                    if "cierpisz na choroby przewlekłe" in question.lower() and user_answer.lower() in ["tak"]:
                        engine.say("Na jakie choroby przewlekłe cierpisz?")
                        engine.runAndWait()
                        chronic_diseases = input("Na jakie choroby przewlekłe cierpisz? ")
                        responses["answers"]["Choroby przewlekłe"] = chronic_diseases
                        print("AI: Dziękuję za informację o chorobach przewlekłych.")
                        engine.say("Dziękuję za informację o chorobach przewlekłych.")
                        engine.runAndWait()
        
                    #if "Mam gorączke" in user_answer.lower():
                        #return 
                    
                    is_last_question = (i == len(questions) - 1)
                    ai_response = simple_ai_response(user_answer, is_last_question)
                    if ai_response:  # Wyświetlamy tylko, jeśli odpowiedź AI nie jest pusta
                        engine.say(ai_response)
                        print(f"AI: {ai_response}")
                        engine.runAndWait()
                    break
                      # Odpowiedź AI do pacjenta
            else:
                report = generate_report(responses)
                print(report)

            
            engine.say("Czy chcesz teraz przejść do sesji terapeutycznej? (tak/nie)")
            print("\nCzy chcesz teraz przejść do sesji terapeutycznej? (tak/nie)")
            engine.runAndWait()

            while True:
                therapy_input = input("Wpisz 'tak', aby przejść do terapii lub 'nie', aby zakończyć: ").lower()
                if therapy_input == 'tak':
                    # Rozpoczynamy sesję terapeutyczną
                    for i, question in enumerate(therapy_questions):
                        while True:
                            engine.say(question)
                            engine.runAndWait()

                            user_answer = input(f"{question} ")
                            if not validate_text_input(user_answer):
                                print("Nieprawidłowa odpowiedź. Proszę podać odpowiedź tekstową, składającą się tylko z liter.\n")
                                continue

                            therapy_responses["therapy_answers"][question] = user_answer
                            feelings = ['czuje sie słabo emocjonalnie', 'chyba mam objawy depresji']
                            if any(word in user_answer.lower() for word in feelings):
                                print("Przykro mi to słyszeć")
                                engine.say("Przykro mi to słyszeć\n")
                                engine.runAndWait()
                                print("Polecam obejrzeć ten 25 minutowy filmik: https://www.youtube.com/watch?v=X1HXg6BkKw0")
                                engine.say("Polecam obejrzeć ten 25 minutowy filmik")
                                engine.runAndWait()

                                break

                            is_last_question = (i == len(therapy_questions) -1)
                            ai_response = simple_ai_response(user_answer, is_last_question)
                            if ai_response:
                                engine.say(ai_response)
                                print(f"AI: {ai_response}")  # Odpowiedź AI do pacjenta
                                engine.runAndWait()
                            break
                    else:
                        therapy_report = generate_therapy_report(therapy_responses)
                        print("\nZakończyliśmy sesję terapeutyczną. Oto raport:")
                        print(therapy_report)

                        save_combined_report_to_file(report, therapy_report)
                    break
                elif therapy_input == 'nie':
                    # Generujemy raport z wywiadu medycznego
                    report = generate_report(responses)
                    print("\nZakończyliśmy wywiad medyczny. Oto raport:")
                    print(report)
                    break
                else:
                    print("Nie rozumiem. Wpisz 'tak' lub 'nie'.")
                    continue
            break
        elif user_input == 'nie':
            print("Dziękuje za rozmowę!")
            engine.say("Dziękuje za rozmowę!")
            engine.runAndWait()
            break
        else:
            print("Nie rozumiem. Wpisz 'tak' lub 'nie'.")
            continue

if __name__ == "__main__":
    start_interview()

