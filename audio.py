import google.generativeai as genai
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv


def main(key):
  
  freq = 44100
  duration = 5
  
  recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)
  print("recording")
  sd.wait()
  
  wv.write("./recording.wav", recording, freq, sampwidth=2)
  
  genai.configure(api_key=key)
  model = genai.GenerativeModel("gemini-2.0-flash-exp")
  
  myfile = genai.upload_file("./recording.wav")
  prompt = "take this audio file and make it into a text command only write the command itself and nothing else before or after"
  result = model.generate_content([myfile, prompt])
  
  return(result.text)
  
  
  
  
  
  


if __name__ == "__main__":
    main()