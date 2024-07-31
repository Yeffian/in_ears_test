import threading
import time

import librosa
import numpy as np
import simpleaudio as sa


DRUM_TRACK = r'/Users/yeffian/development/in_ears_at_home/stems/hysteria_drum_track.wav'
VOCAL_TRACK = r'/Users/yeffian/development/in_ears_at_home/stems/hysteria_vocal_track.wav'

SONG = r'/Users/yeffian/development/in_ears_at_home/hystera_kids.wav'
STRONG_BEAT = r'/Users/yeffian/development/in_ears_at_home/strong_beat.wav'
WEAK_BEAT = r'/Users/yeffian/development/in_ears_at_home/weak_beat.wav'


def get_tempo():
    # TODO: The BPM doesn't feel right to me, dragging slightly(?)
    y, sr = librosa.load(SONG)

    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    bpm = np.round(tempo[0]).astype(int)
    interval_sec = 60.0 / bpm

    print(f"BPM: {bpm}")

    count = 0
    while True:
        count += 1
        if count == 1:
            wave_obj = sa.WaveObject.from_wave_file(STRONG_BEAT)
        else:
            wave_obj = sa.WaveObject.from_wave_file(WEAK_BEAT)

        play_obj = wave_obj.play()

        if count == 4:
            count = 0

        time.sleep(interval_sec)


def play_beat():
    song_obj = sa.WaveObject.from_wave_file(DRUM_TRACK)
    _ = song_obj.play()


def play_vocals():
    # TODO: Vocal track doesn't line up, figure out timing issues
    song_obj = sa.WaveObject.from_wave_file(VOCAL_TRACK)
    _ = song_obj.play()

# TODO: Install songs programatically using yt-dlp


t1 = threading.Thread(target=get_tempo, daemon=True)
t2 = threading.Thread(target=play_beat, daemon=True)
t3 = threading.Thread(target=play_vocals, daemon=True)

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()

