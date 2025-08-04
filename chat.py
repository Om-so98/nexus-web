  "Hi! How are you doing today?"
        ]

    def setup_voice(self):
        """Configure voice settings"""
        voices = self.engine.getProperty('voices')
        if voices:
            # Try to set a female voice if available
            for voice in voices:
                if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
        
        # Set speech rate and volume
        self.engine.setProperty('rate', 180)  # Speed of speech
        self.engine.setProperty('volume', 0.8)  # Volume level (0.0 to 1.0)

    def load_preferences(self):
        """Load user preferences from file"""
        try:
            if os.path.exists(self.preferences_file):
                with open(self.preferences_file, 'r') as f:
                    prefs = json.load(f)
                    self.user_name = prefs.get('user_name')
                    print(f"Welcome back, {self.user_name}!" if self.user_name else "Welcome!")
        except:
            pass

    def save_preferences(self):
        """Save user preferences to file"""
        try:
            prefs = {'user_name': self.user_name}
            with open(self.preferences_file, 'w') as f:
                json.dump(prefs, f)
        except:
            pass

    def speak(self, text):
        """Make the bot speak with improved formatting"""
        print(f"🤖 Bot: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        """Listen for voice input with improved error handling"""
        with sr.Microphone() as source:
            print("🎤 Listening...")
            # Adjust for background noise
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            try:
                # Listen for up to 7 seconds
                audio = self.recognizer.listen(source, timeout=7, phrase_time_limit=10)
                # Recognize speech using Google Web Speech API
                user_input = self.recognizer.recognize_google(audio)
                print(f"👤 You: {user_input}")
                
                # Add to conversation history
                self.conversation_history.append(f"User: {user_input}")
                return user_input.lower()
                
            except sr.WaitTimeoutError:
                print("⏰ No speech detected")
                return None
            except sr.UnknownValueError:
                responses = [
                    "Sorry, I didn't catch that. Could you repeat?",
                    "I didn't quite hear you. Please try again.",
                    "Could you say that again? I missed it."
                ]
                self.speak(random.choice(responses))
                return None
            except sr.RequestError as e:
                self.speak("Sorry, there was an issue with the speech service.")
                print(f"Error: {e}")
                return None

    def get_weather(self, city="London"):
        """Get weather information (requires API key)"""
        if not EXTENDED_FEATURES:
            return "Weather feature requires additional libraries."
        
        # Note: You'll need to get a free API key from OpenWeatherMap
        # and replace 'YOUR_API_KEY' with your actual key
        api_key = "YOUR_API_KEY"
        if api_key == "YOUR_API_KEY":
            return "Weather feature requires an API key. Please configure it in the code."
        
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            response = requests.get(url, timeout=5)
            data = response.json()
            
            if response.status_code == 200:
                temp = data['main']['temp']
                description = data['weather'][0]['description']
                return f"The weather in {city} is {temp}°C with {description}."
            else:
                return "Sorry, I couldn't get the weather information."
        except:
            return "Sorry, I couldn't connect to the weather service."

    def search_wikipedia(self, query):
        """Search Wikipedia for information"""
        if not EXTENDED_FEATURES:
            return "Wikipedia search requires additional libraries."
        
        try:
            # Search for the topic
            wikipedia.set_lang("en")
            summary = wikipedia.summary(query, sentences=2)
            return f"Here's what I found about {query}: {summary}"
        except wikipedia.exceptions.DisambiguationError as e:
            # If multiple results, pick the first one
            try:
                summary = wikipedia.summary(e.options[0], sentences=2)
                return f"Here's what I found about {e.options[0]}: {summary}"
            except:
                return f"I found multiple results for {query}. Could you be more specific?"
        except wikipedia.exceptions.PageError:
            return f"Sorry, I couldn't find information about {query}."
        except:
            return "Sorry, I couldn't search Wikipedia right now."

    def get_response(self, user_input):
        """Generate bot responses with enhanced logic"""
        if not user_input:
            return None
        
        # Personal interactions
        if "my name is" in user_input:
            name_match = re.search(r"my name is (\w+)", user_input)
            if name_match:
                self.user_name = name_match.group(1).title()
                self.save_preferences()
                return f"Nice to meet you, {self.user_name}! I'll remember that."
        
        if "what is my name" in user_input or "what's my name" in user_input:
            if self.user_name:
                return f"Your name is {self.user_name}!"
            else:
                return "I don't know your name yet. You can tell me by saying 'My name is...'"
        
        # Greetings
        if any(word in user_input for word in ["hello", "hi", "hey", "good morning", "good afternoon"]):
            greeting = random.choice(self.greetings)
            if self.user_name:
                greeting = greeting.replace("there", self.user_name)
            return greeting
        
        # Time and date
        if "time" in user_input:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            return f"It's {current_time}."
        
        if "date" in user_input or "day" in user_input:
            current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
            return f"Today is {current_date}."
        
        # Bot identity
        if "name" in user_input and "your" in user_input:
            return "I'm your friendly voice assistant! You can call me Voice Bot."
        
        if "how are you" in user_input:
            responses = [
                "I'm doing great, thank you for asking!",
                "I'm excellent! How are you doing?",
                "I'm fantastic! Ready to help you with anything."
            ]
            return random.choice(responses)
        
        # Jokes
        if "joke" in user_input:
            return random.choice(self.jokes)
        
        # Weather
        if "weather" in user_input:
            return self.get_weather()
        
        # Wikipedia search
        if "tell me about" in user_input or "what is" in user_input or "who is" in user_input:
            # Extract the topic
            patterns = [
                r"tell me about (.+)",
                r"what is (.+)",
                r"who is (.+)"
            ]
            
            for pattern in patterns:
                match = re.search(pattern, user_input)
                if match:
                    topic = match.group(1).strip()
                    return self.search_wikipedia(topic)
        
        # Math calculations
        if any(word in user_input for word in ["calculate", "plus", "minus", "times", "multiply", "divide"]):
            try:
                # Simple math parsing
                user_input = user_input.replace("plus", "+").replace("minus", "-")
                user_input = user_input.replace("times", "*").replace("multiply", "*")
                user_input = user_input.replace("divide", "/").replace("divided by", "/")
                
                # Extract numbers and operators
                math_match = re.search(r"(\d+(?:\.\d+)?)\s*([+\-*/])\s*(\d+(?:\.\d+)?)", user_input)
                if math_match:
                    num1, operator, num2 = math_match.groups()
                    result = eval(f"{num1} {operator} {num2}")
                    return f"The answer is {result}"
            except:
                return "Sorry, I couldn't calculate that. Try something like 'calculate 5 plus 3'."
        
        # Conversation history
        if "what did i say" in user_input or "conversation history" in user_input:
            if len(self.conversation_history) > 1:
                return f"Recently you said: {self.conversation_history[-2].replace('User: ', '')}"
            else:
                return "We just started our conversation!"
        
        # Help
        if "help" in user_input or "what can you do" in user_input:
            return ("I can help you with: telling time and date, jokes, weather, "
                   "simple math, Wikipedia searches, remembering your name, and more! "
                   "Just ask me naturally!")
        
        # Exit commands
        if any(word in user_input for word in ["stop", "exit", "quit", "goodbye", "bye"]):
            farewell = f"Goodbye{', ' + self.user_name if self.user_name else ''}! Have a great day!"
            return farewell
        
        # Default responses
        default_responses = [
            "That's interesting! Could you tell me more?",
            "I'm not sure about that. Try asking about time, weather, or say 'help' for more options.",
            "Hmm, I didn't quite understand. You can ask me about jokes, time, weather, or math!",
            "I'm still learning! Try asking 'what can you do' to see my capabilities."
        ]
        return random.choice(default_responses)

    def main(self):
        """Main chatbot loop with enhanced features"""
        welcome_msg = "Hello! I'm your enhanced voice chatbot. I can help with time, weather, Wikipedia searches, math, and more!"
        if self.user_name:
            welcome_msg = f"Welcome back, {self.user_name}! " + welcome_msg
        
        self.speak(welcome_msg)
        
        while True:
            user_input = self.listen()
            if user_input:
                response = self.get_response(user_input)
                if response:
                    self.speak(response)
                    
                    # Add bot response to history
                    self.conversation_history.append(f"Bot: {response}")
                    
                    # Keep history manageable
                    if len(self.conversation_history) > 20:
                        self.conversation_history = self.conversation_history[-10:]
                    
                    if any(word in response.lower() for word in ["goodbye", "bye"]):
                        break
            
            time.sleep(1)  # Short pause to avoid rapid looping

if __name__ == "__main__":
    bot = VoiceChatbot()