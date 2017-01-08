#brew install wxpython
#sudo pip install simplecalculator
#sudo apt install linuxbrew-wrapper
#pip install SpeechRecognition
#sudo apt-get install python-pyaudio python3-pyaudio
#pip install --allow-unverified=pyaudio pyaudio
#sudo apt-get install python-wxtools
#sudo pip install pyttsx
#sudo pip install wikipedia
#sudo apt-get install gcc automake autoconf libtool bison swig python-dev libpulse-dev
#git clone https://github.com/cmusphinx/sphinxbase.git
#git clone https://github.com/cmusphinx/pocketsphinx.git
#svn checkout svn://svn.code.sf.net/p/cmusphinx/code/trunk cmusphinx-code
#git clone https://github.com/cmusphinx/sphinxtrain.git
#SUDO APT INSTALL SUBVERSION
#sudo apt-get install gstreamer1.0-libav
#sudo apt install python3-gi
#sudo apt install python-gi
#sudo apt-get install python-pocketsphinx
#http://jrmeyer.github.io/installation/2016/01/09/Installing-CMU-Sphinx-on-Ubuntu.html
#IF MEMORYERROR = run as sudo pip --no-chache-dir install SpeechRecognition

#DO  sudo pip install --upgrade pocketsphinx
#sudo apt-get install flex

import wx
import wikipedia
import pyttsx
import pyaudio
from calculator.simple import SimpleCalculator

import os, sys
from pocketsphinx import LiveSpeech, get_model_path

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
GObject.threads_init()
Gst.init(None)
gst = Gst



#speech reco



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

        for char in input:
            #need space between each char for it to work: 2 + 2 not 2+2
            if char == '+' or char == '-' or char == '*' or char == '/':
                calculator = SimpleCalculator()
                calculator.run(input)
                engine.runAndWait()
                engine.say(float(''.join(elem for elem in calculator.log[-1] if elem.isdigit() or elem == '.')))
                engine.runAndWait()
                return
        if input == '':

            self.pipeline = gst.parse_launch('autoaudiosrc ! audioconvert ! audioresample ! pocketsphinx name=asr ! fakesink')

            self.pipeline.set_state(gst.State.PLAYING)

            bus = self.pipeline.get_bus()
            bus.add_signal_watch()
            bus.connect('message::element', self.element_message)


    def element_message(self, bus, msg):
        """Receive element messages from the bus."""
        msgtype = msg.get_structure().get_name()
        if msgtype != 'pocketsphinx':
            return
        if msg.get_structure().get_value('final'):
            self.final_result(msg.get_structure().get_value('hypothesis'), msg.get_structure().get_value('confidence'))
            self.pipeline.set_state(gst.State.PAUSED)
            self.button.set_active(False)
        elif msg.get_structure().get_value('hypothesis'):
            self.partial_result(msg.get_structure().get_value('hypothesis'))

    def partial_result(self, hyp, uttid):
        """Delete any previous selection, insert text and select it."""
        # All this stuff appears as one single action
        self.textbuf.begin_user_action()
        self.textbuf.delete_selection(True, self.text.get_editable())
        self.textbuf.insert_at_cursor(hyp)
        ins = self.textbuf.get_insert()
        iter = self.textbuf.get_iter_at_mark(ins)
        iter.backward_chars(len(hyp))
        self.textbuf.move_mark(ins, iter)
        self.textbuf.end_user_action()

    def final_result(self, hyp, uttid):
        """Insert the final result."""
        # All this stuff appears as one single action
        self.textbuf.begin_user_action()
        self.textbuf.delete_selection(True, self.text.get_editable())
        self.textbuf.insert_at_cursor(hyp)
        self.textbuf.end_user_action()




#            speech = LiveSpeech(lm = False, keyphrase = 'forward', kws_threshold=20)
#            for phrase in speech:
#                if phrase.segments(detailed=True):
#                    print YO
    ###Add a tell me more - then more sentences - reads entire summary
#        engine.runAndWait()

#        engine.say(wikipedia.summary(input, sentences = 2))




if __name__ == "__main__":
    app = wx.App(True)
    frame = MyFrame()
app.MainLoop()
