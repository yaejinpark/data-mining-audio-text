# Import modules
import sys
import time
import speech_recognition as sr
import ConversationIntentAnalyzer as cia

# Define parameters
sample_rate = 48000     # how often values are recorded
chunk_size = 2048       # number of bytes of data that can be read at once
device_id = -1

# Initialize recognizer
r = sr.Recognizer()

# Generate list of all audio devices
mic_list = sr.Microphone.list_microphone_names()

# User chooses a microphone option
mic_list_names = []
print("\nChoose an available microphone:\n")

for i, mic_option in enumerate(mic_list):
    mic_list_names.append(mic_option)
    print("(" + str(i) + ") " + mic_option)

mic_choice = input("\nchoice: ")
print()

# Check that input is valid type and value
try:
    mic_choice = int(mic_choice)
except ValueError:
    print("Choose a valid audio device index.")
    sys.exit(1)

if mic_choice not in range(len(mic_list)):
    print("Choose a valid audio device index.")
    sys.exit(1)

# Set device ID to mic that was specified before
for i,mic in enumerate(mic_list):
    if mic == mic_list_names[mic_choice]:
        device_id = i

# Set up mic as source of input
try:
    with sr.Microphone(device_index=device_id, sample_rate=sample_rate, chunk_size=chunk_size) as src:

        # Let recognizer adjust to energy threshold based on ambient noise
        print("Adjusting background noise...\n")
        r.adjust_for_ambient_noise(src)

        # Create analzer object
        analyzer = cia.ConversationIntentAnalyzer()

        # Run in an infinite loop until user says "stop" 
        try:
            while True:

                # Get audio sample from user
                print("Listening for audio...")
                audio = r.listen(src)

                # Audio recognition & exception handling
                try:
                    start_time = time.time()
                    text = r.recognize_google(audio)
                except sr.UnknownValueError:
                    #print("Google Speech Recognition could not understand audio.")
                    continue
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition Service at this time.")
                    continue
                
                # Listen for quit command
                if text == "stop":
                    print("Exiting program...")
                    sys.exit(2)

                # Speech classification
                analyzer.prediction([text])

                # Print out time of execution of speech recognition + classification
                end_time = time.time()
                print("Time of execution: %s seconds\n" % (end_time - start_time))

        except KeyboardInterrupt:
            print("Exiting program...")
            sys.exit(3)
except:
    print("Choose a working audio device.")
    sys.exit(4)