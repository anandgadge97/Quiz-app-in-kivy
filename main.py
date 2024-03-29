from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
import requests

from kivy.uix.button import Button

class FirstWindow(Screen):
    pass

class SecondWindow(Screen):
    pass

class ThirdWindow(Screen):
    pass

class FourthWindow(Screen):
    pass

class FifthWindow(Screen):
    pass

class SixthWindow(Screen):
    pass 

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file('myapp.kv')

class MyApp(App):
    def build(self):
        return kv

    def button1_pressed(self, instance):
        first_screen = self.root.get_screen("first")
        first_screen.ids.label.text = "Proceeding to the second screen"
        Clock.schedule_once(lambda dt: self.clear_label_text(), 2)

    
    
    def clear_label_text(self):
        # Clear the label text after a delay
        first_screen = self.root.get_screen("first")
        first_screen.ids.label.text = "Welcome"

    def button2_pressed(self, instance):
        second_screen = self.root.get_screen("first")
        second_screen.ids.label.text = "Exiting the program!"
        Clock.schedule_once(lambda dt: self.stop(), 2)


    def change_to_third_screen(self):
            self.root.current = "third"

    def reset_label_fourth(self, dt):
        # Reset the label text after 2 seconds
        fourth_screen = self.root.get_screen('fourth')
        fourth_screen.ids.label.text = "Sign Up"


    def signup_pressed(self, username, email, password, confirm_password):
        if len(username) < 3 or len(password)<5:
            a = ("Username & password atleast 3 & 5 characters ")
            fourth_screen = self.root.get_screen("fourth")
            fourth_screen.ids.label.text= a
            Clock.schedule_once(self.reset_label_fourth, 2)
        elif password != confirm_password:
            b = "Passwords do not match."
            fourth_screen = self.root.get_screen("fourth")
            fourth_screen.ids.label.text = b
            Clock.schedule_once(self.reset_label_fourth, 2)
        else:
            # Your Django API endpoint URL
            api_url = "http://127.0.0.1:8000/api/"

            data = {
                'username':username,
                'email':email,
                'password':password,
            }

            try:
                response = requests.post(api_url,data=data)
                if response.status_code // 100 == 2:
                # Do something with the successful response
                    success_message = "Signup successful!"
                    fourth_screen = self.root.get_screen("fourth")
                    fourth_screen.ids.label.text = success_message
                    Clock.schedule_once(lambda dt: self.change_to_third_screen(), 2)


                else:
                # Handle unsuccessful response
                    error_message = f"Error: {response.text}"
                    fourth_screen = self.root.get_screen("fourth")
                    fourth_screen.ids.label.text = error_message

            except requests.RequestException as e:
                # Handle request exception
                fourth_screen = self.root.get_screen("fourth")
                fourth_screen.ids.label.text = f"Request exception: {str(e)}"


    def submit_button_pressed(self, username_input, password_input):
        username = username_input.text
        password = password_input.text
        api_url = "http://127.0.0.1:8000/api"
        third_screen = self.root.get_screen('third')

        try:
            response = requests.get(api_url)

            if response.status_code // 100 == 2:
                users = response.json()

                for user in users:
                    if user.get('username') == username and user.get('password') == password:
                        # Credentials are correct, redirect to the fifth screen
                        self.root.current = 'fifth'
                        self.root.transition.direction = "left"  
                        return True

                # No match found, update the label in the third screen
                third_screen.ids.label.text = "Invalid password or username"
                Clock.schedule_once(self.reset_label, 2)
                return False

            else:
                print(f"Error fetching users from the API: {response.status_code}")
                return False

        except requests.RequestException as e:
            print(f"Error: {e}")
            return False
        
    def reset_label(self, dt):
        # Reset the label text after 2 seconds
        third_screen = self.root.get_screen('third')
        third_screen.ids.label.text = "Sign In"

    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)
        self.questions = []
        self.current_question_index = 0


    
    def change_to_sixth_screen(self):
            self.root.current = "sixth"
    
    def reset_label(self, dt):
        # Reset the label text after 2 seconds
       
        fifth_screen = self.root.get_screen('fifth')
        fifth_screen.ids.label.text = "Sign In"


    def fetch_quiz_questions(self, instance):
        api_url1 = "https://opentdb.com/api.php?amount=10"
        fifth_screen = self.root.get_screen('fifth')
        try:
            response = requests.get(api_url1)
            if response.status_code == 200:
                data = response.json()
                fifth_screen.ids.label.text = "Fetching data"
                Clock.schedule_once(lambda dt: self.change_to_sixth_screen(), 2)
                self.load_quiz_data(data.get('results', []))
                print("success")              
            else:
                fifth_screen.ids.label.text = f"Error fetching quiz questions: {response.status_code}"

        except requests.RequestException as e:
            fifth_screen.ids.label.text = f"Request exception: {str(e)}"


    def load_quiz_data(self, questions):
        sixth_screen = self.root.get_screen('sixth')
        sixth_screen.ids.layout.clear_widgets()


    def load_quiz_data(self, questions):
        sixth_screen = self.root.get_screen('sixth')
        sixth_screen.ids.layout.clear_widgets()
        for index, question_data in enumerate(questions):
            question_text = question_data.get('question', 'N/A')
            question_id = f"Question {index + 1}:"  # Generate a unique ID for each question
            question_label_text = f"{question_id} {question_text}"  # Combine ID and question text
            question_label = Label(text=question_label_text, size_hint_y=None, height=100)
            sixth_screen.ids.layout.add_widget(question_label)
        

               

if __name__ == '__main__':
    MyApp().run()