import os
import json
import wave
import noisereduce as nr
import soundfile as sf
from vosk import Model, KaldiRecognizer
from elevenlabs.client import ElevenLabs
import tempfile
import uuid
from scipy import signal
from app.config import Settings


class AudioProcessor:
    def __init__(self, settings: Settings):
        self.model = Model(settings.VOSK_MODEL_PATH)
        print(f"VOSK model loaded from {settings.VOSK_MODEL_PATH}")
        self.sample_rate = 16000  # VOSK sample rate
        self.elevenlabs = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)
        print("ElevenLabs client initialized")

    def enhance_audio(self, input_path: str) -> str:
        # Read audio
        data, samplerate = sf.read(input_path)

        # Convert sample rate to 16kHz if needed
        if samplerate != 16000:
            number_of_samples = round(len(data) * float(16000) / samplerate)
            data = signal.resample(data, number_of_samples)
            samplerate = 16000

        # Convert to mono if needed
        if len(data.shape) > 1:
            data = data.mean(axis=1)

        # Perform noise reduction
        reduced_noise = nr.reduce_noise(y=data, sr=samplerate)

        # Save enhanced audio
        output_path = input_path.replace(".wav", "_enhanced.wav")
        sf.write(output_path, reduced_noise, samplerate, subtype="PCM_16")
        return output_path

    def transcribe_audio(self, audio_path: str) -> str:
        wf = wave.open(audio_path, "rb")
        samplerate = wf.getframerate()
        print(f"Transcribing audio from {samplerate}")
        if (
            wf.getnchannels() != 1
            or wf.getsampwidth() != 2
            or wf.getframerate() != self.sample_rate
        ):
            raise ValueError(
                "Audio file must be WAV format mono PCM with 16kHz sample rate"
            )

        recognizer = KaldiRecognizer(self.model, self.sample_rate)
        recognizer.SetWords(True)

        transcription = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                if "text" in result:
                    transcription.append(result["text"])

        final_result = json.loads(recognizer.FinalResult())
        if "text" in final_result:
            transcription.append(final_result["text"])

        return " ".join(transcription)

    def text_to_speech(self, text: str) -> str:
        # Generate unique temporary file path
        temp_file = os.path.join(tempfile.gettempdir(), f"tts_{uuid.uuid4()}.mp3")

        # Convert text to speech
        audio = self.elevenlabs.text_to_speech.convert(
            text=text,
            voice_id="9BWtsMINqrJLrRacOk9x",  # Aria voice
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )

        # Save audio to temporary file
        with open(temp_file, "wb") as f:
            for chunk in audio:
                if chunk:
                    f.write(chunk)

        return temp_file
