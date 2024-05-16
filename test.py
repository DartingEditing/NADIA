import struct
import time
import pvporcupine
import pyaudio


def hotword():
    porcupine=None
    paud=None
    audio_stream=None

    try:
        # Access key from Picovoice Console
        access_key = "2Mj2Ju9oEOiGVFQr1rpkVeeaAv0sSWcDkPUdTcoJgZw5CHtCbGrmHA=="

        #path
        NADIA= "engine\\nadia_windows.ppn"

        # pre trained keywords    
        porcupine=pvporcupine.create(
            access_key=access_key,
            keyword_paths=[NADIA]
        )

        #config pyaudio
        paud=pyaudio.PyAudio()

        # Open audio stream
        audio_stream=paud.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("n")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()
hotword()