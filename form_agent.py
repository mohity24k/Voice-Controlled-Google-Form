import time
import speech_recognition as sr
import pyttsx3
from selenium import webdriver
from selenium.webdriver.common.by import By
# --- FIREFOX IMPORTS ---
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager


# -----------------------

class GoogleFormVoiceAgent:
    def __init__(self, form_url):
        # 1. Setup Voice Output
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 170)

        # 2. Setup Voice Input
        self.recognizer = sr.Recognizer()

        # 3. Setup Browser (FIREFOX)
        print("Opening Firefox...")
        try:
            self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        except Exception as e:
            print(f"Error opening Firefox: {e}")
            print("Make sure Firefox is installed on your computer.")
            return

        self.driver.get(form_url)
        self.driver.maximize_window()

        self.current_question_index = 0
        self.questions = []

        time.sleep(3)  # Wait a bit longer for Firefox to load
        self.speak("I am ready. Let's fill this form.")
        self.scan_questions()

    def speak(self, text):
        print(f"🤖 Agent: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def scan_questions(self):
        self.questions = self.driver.find_elements(By.XPATH, '//div[@role="listitem"]')
        print(f"Found {len(self.questions)} questions.")

    def highlight_current_question(self):
        if self.current_question_index < len(self.questions):
            q_element = self.questions[self.current_question_index]
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", q_element)
            self.driver.execute_script("arguments[0].style.border='3px solid red'", q_element)
        else:
            self.speak("End of form reached.")

    def listen_for_command(self):
        with sr.Microphone() as source:
            print("🎤 Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=3)
                command = self.recognizer.recognize_google(audio).lower()
                print(f"You said: {command}")
                return command
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                print("Could not understand audio")
                return None
            except sr.RequestError:
                print("API unavailable")
                return None

    def execute_action(self, command):
        if not command: return

        q_element = self.questions[self.current_question_index]
        options = q_element.find_elements(By.XPATH, './/div[@role="radio"]')
        if not options:
            options = q_element.find_elements(By.XPATH, './/div[@role="checkbox"]')

        target_index = -1
        if "one" in command or "1" in command or "first" in command:
            target_index = 0
        elif "two" in command or "2" in command or "second" in command:
            target_index = 1
        elif "three" in command or "3" in command or "third" in command:
            target_index = 2
        elif "four" in command or "4" in command or "fourth" in command:
            target_index = 3
        elif "five" in command or "5" in command or "fifth" in command:
            target_index = 4

        if "next" in command or "skip" in command:
            self.current_question_index += 1
            self.speak("Next question.")
            self.highlight_current_question()
            return

        if "back" in command or "previous" in command:
            if self.current_question_index > 0:
                self.current_question_index -= 1
                self.speak("Going back.")
                self.highlight_current_question()
            return

        if "submit" in command:
            try:
                submit = self.driver.find_element(By.XPATH, '//div[@role="button"]//span[text()="Submit"]')
                submit.click()
                self.speak("Form submitted.")
            except:
                self.speak("I couldn't find the submit button.")
            return

        if target_index != -1:
            if target_index < len(options):
                options[target_index].click()
                self.speak(f"Selected option {target_index + 1}")
                time.sleep(0.5)
                self.current_question_index += 1
                self.highlight_current_question()
            else:
                self.speak("That option does not exist.")
        else:
            self.speak("I didn't catch a valid option number.")

    def run(self):
        self.highlight_current_question()
        try:
            while True:
                cmd = self.listen_for_command()
                if cmd:
                    if "stop" in cmd or "exit" in cmd:
                        self.speak("Goodbye.")
                        break
                    self.execute_action(cmd)
        except KeyboardInterrupt:
            print("Stopping...")
        finally:
            input("Press Enter to close browser...")
            self.driver.quit()


if __name__ == "__main__":
    # REPLACE WITH YOUR FORM URL
    FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdhgutqv7hoaSy79k2XKZNZfaIvBtt3e6D5HZsS0vOck8LRHQ/viewform"
    agent = GoogleFormVoiceAgent(FORM_URL)
    agent.run()