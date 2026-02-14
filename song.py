import time
import sys

def type_lyrics(text, speed=0.04):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

# (timestamp_in_seconds, lyric)
lyrics_timestamps = [
    (1.0, "Sochu ke milni te bolaanga ki"),
    (5.2, "Teri taan gallaan’ch… shaayari"),
    (9.5, "Vekhegi mainu te sochegi kya tu"),
    (13.8, "Mitti da banda main, tu taan pari..."),
    (18.6, "Ishqe di galiyaan’ch khoya e dil ve"),
    (21.1, "Aas lagaaye ik jaaye tu mil ve"),
    (26.0, "Kol tere mainu aan de soni"),
    (31.2, "Karaan main kitne jatan O soni"),
    (36.0, "Dooron dooron main...")
]

print("\n🎶 Lyrics Sync Started (Virtual Song Clock)\n")
start_time = time.time()

for timestamp, line in lyrics_timestamps:
    while time.time() - start_time < timestamp:
        time.sleep(0.01)
    type_lyrics(line)

print("\n🎵 Lyrics End 🎵")
