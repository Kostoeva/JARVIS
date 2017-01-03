#brew install wxpython
#sudo apt install linuxbrew-wrapper
#pip install SpeechRecognition
#sudo apt-get install python-pyaudio python3-pyaudio
#pip install --allow-unverified=pyaudio pyaudio
import wx
import wikipedia
import pyttsx
import pyaudio
import speech_recognition as sr



#voices = engine.getProperty('voices')
#for voice in voices:
#    print "Using voice: ", repr(voice)
#    engine.setProperty('voice', voices[2].id)
    #engine.say("I'm a little teapot; the big brown fox jumped over the lazy dog")


engine = pyttsx.init()
engine.setProperty('rate', 65)
#engine.say("I'm a little teapot; the big brown fox jumped over the lazy dog")
#engine.runAndWait()


class MyFrame(wx.Frame):
    def __init__(self):
        #GUI
        wx.Frame.__init__(self, None,
            pos=wx.DefaultPosition,
            size = wx.Size(450, 100),
            style = wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX
            | wx.CLIP_CHILDREN,
            title = "J.A.R.V.I.S.")
        panel = wx.Panel(self)
        my_sizer = wx.BoxSizer(wx.VERTICAL)
        lbl = wx.StaticText(panel, label = "Hello. How may I assist you today?")
        my_sizer.Add(lbl, 0, wx.ALL, 5)
        self.txt = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER, size=(400,30))
        self.txt.SetFocus()
        self.txt.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
        my_sizer.Add(self.txt, 0, wx.ALL, 5)
        panel.SetSizer(my_sizer)
        self.Show()
        engine.say("Hello.")#" How may I assist you today?")
        engine.runAndWait()



    def OnEnter(self, event):
        input = self.txt.GetValue()
        input = input.lower()

        if input == '':
            print "Entered loop"
            r = sr.Recognizer()
            with sr.Microphone(device_index=2) as source:
                print "Entered mic"
                audio = r.listen(source)
            try:
                print "Entered try"
                self.txt.SetValue(r.recognize_google(audio))
                input = self.txt.GetValue()
            except sr.UnknownValueError:
                print"Google Speech Recognition could not understand audio"
            except sr.RequestError as e:
                print"Could not request results from Google Speech Recognition service; {0}".format(e)
        #input = input.split(' ')
        #input = " ".join(input[2:])
        #Continually asks a question for wiki searches
        #while True:
        #    input = raw_input("Q: ")
            #change languages for wiki article queries: wikipedia.set_lang("ru")
    ###Add a tell me more - then more sentences - reads entire summary

        engine.runAndWait()

        engine.say(wikipedia.summary(input, sentences = 2))

if __name__ == "__main__":
    app = wx.App(True)
    frame = MyFrame()
    app.MainLoop()
