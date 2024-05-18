import time
import azure.cognitiveservices.speech as speechsdk
import keyboard

class SpeechToTextManager:
    azure_speechconfig = None
    azure_audioconfig = None
    azure_speechrecognizer = None

    def __init__(self):
        # Inserisci qui la tua chiave di sottoscrizione e la regione del servizio
        subscription_key = 'f5b2203ed9d145bc905295de26f54b17'
        region = 'westeurope'

        try:
            self.azure_speechconfig = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
        except TypeError:
            exit("Error in setting up SpeechConfig with the given key and region!")

        self.azure_speechconfig.speech_recognition_language = "it-IT"
        
    def speechtotext_from_mic(self):
        self.azure_audioconfig = speechsdk.audio.AudioConfig(use_default_microphone=True)
        self.azure_speechrecognizer = speechsdk.SpeechRecognizer(speech_config=self.azure_speechconfig, audio_config=self.azure_audioconfig)

        print("Speak into your microphone.")
        speech_recognition_result = self.azure_speechrecognizer.recognize_once_async().get()
        text_result = speech_recognition_result.text

        if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Recognized: {}".format(text_result))
        elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
        elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_recognition_result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")

        print(f"We got the following text: {text_result}")
        return text_result

    def speechtotext_from_file(self, filename):
        self.azure_audioconfig = speechsdk.audio.AudioConfig(filename=filename)
        self.azure_speechrecognizer = speechsdk.SpeechRecognizer(speech_config=self.azure_speechconfig, audio_config=self.azure_audioconfig)

        print("Listening to the file \n")
        speech_recognition_result = self.azure_speechrecognizer.recognize_once_async().get()

        if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Recognized: \n {}".format(speech_recognition_result.text))
        elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
        elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_recognition_result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")

        return speech_recognition_result.text

    def speechtotext_from_file_continuous(self, filename):
        self.azure_audioconfig = speechsdk.audio.AudioConfig(filename=filename)
        self.azure_speechrecognizer = speechsdk.SpeechRecognizer(speech_config=self.azure_speechconfig, audio_config=self.azure_audioconfig)

        done = False
        def stop_cb(evt):
            print('CLOSING on {}'.format(evt))
            nonlocal done
            done = True

        self.azure_speechrecognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
        self.azure_speechrecognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
        self.azure_speechrecognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
        self.azure_speechrecognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))

        self.azure_speechrecognizer.session_stopped.connect(stop_cb)
        self.azure_speechrecognizer.canceled.connect(stop_cb)

        all_results = []
        def handle_final_result(evt):
            all_results.append(evt.result.text)
        self.azure_speechrecognizer.recognized.connect(handle_final_result)

        print("Now processing the audio file...")
        self.azure_speechrecognizer.start_continuous_recognition()

        while not done:
            time.sleep(.5)

        self.azure_speechrecognizer.stop_continuous_recognition()

        final_result = " ".join(all_results).strip()
        print(f"\n\nHere's the result we got from continuous file read!\n\n{final_result}\n\n")
        return final_result

    def speechtotext_from_mic_continuous(self, p='p'):
        self.azure_speechrecognizer = speechsdk.SpeechRecognizer(speech_config=self.azure_speechconfig)

        done = False

        def recognized_cb(evt: speechsdk.SpeechRecognitionEventArgs):
            print('RECOGNIZED: {}'.format(evt))
        self.azure_speechrecognizer.recognized.connect(recognized_cb)

        def stop_cb(evt: speechsdk.SessionEventArgs):
            print('CLOSING speech recognition on {}'.format(evt))
            nonlocal done
            done = True

        self.azure_speechrecognizer.session_stopped.connect(stop_cb)
        self.azure_speechrecognizer.canceled.connect(stop_cb)

        all_results = []
        def handle_final_result(evt):
            all_results.append(evt.result.text)
        self.azure_speechrecognizer.recognized.connect(handle_final_result)

        result_future = self.azure_speechrecognizer.start_continuous_recognition_async()
        result_future.get()
        print('Continuous Speech Recognition is now running, say something.')

        while not done:
            if keyboard.read_key() == stop_key:
                print("\nEnding azure speech recognition\n")
                self.azure_speechrecognizer.stop_continuous_recognition_async()
                break

        final_result = " ".join(all_results).strip()
        print(f"\n\nHere's the result we got!\n\n{final_result}\n\n")
        return final_result

# Tests
# if __name__ == '__main__':
#     TEST_FILE = "D:\\Video Editing\\Misc - Ai teaches me to pass History Exam\\Audio\\Misc - Ai teaches me to pass History Exam - VO 1.wav"
#     
#     speechtotext_manager = SpeechToTextManager()
#
#     while True:
#         # speechtotext_manager.speechtotext_from_mic()
#         # speechtotext_manager.speechtotext_from_file(TEST_FILE)
#         # speechtotext_manager.speechtotext_from_file_continuous(TEST_FILE)
#         result = speechtotext_manager.speechtotext_from_mic_continuous()
#         print(f"\n\nHERE IS THE RESULT:\n{result}")
#         time.sleep(60)
