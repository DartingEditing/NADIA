import pvporcupine # type: ignore
import pyaudio
import struct

# Access key from Picovoice Console
access_key = "2Mj2Ju9oEOiGVFQr1rpkVeeaAv0sSWcDkPUdTcoJgZw5CHtCbGrmHA=="

# Path to the .ppn file
wake_word_path = "engine\\nadia_windows.ppn"

# Initialize Porcupine with your access key and wake word file
porcupine = pvporcupine.create(
    access_key=access_key,
    keyword_paths=[wake_word_path]
)

# Configure PyAudio
pa = pyaudio.PyAudio()

# Open audio stream
audio_stream = pa.open(
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length
)

print("Listening for wake word...")

try:
    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
        
        keyword_index = porcupine.process(pcm)
        if keyword_index >= 0:
            print("Wake word detected!")
            # Add your logic here when wake word is detected
except KeyboardInterrupt:
    print("Stopping...")
finally:
    # Clean up resources
    audio_stream.close()
    pa.terminate()
    porcupine.delete()
