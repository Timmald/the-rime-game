from playsound3 import playsound
import re
from collections import defaultdict
import random
import threading
import os
from time import sleep,time


NUM_SYLLABLES = 2
FIRST_RHYME = True
LOOKAHEAD = 4# How many measures can you see at once
HARD_MODE = False #rn just controls whether you go over 135 BPM


vowels = "iɪeɛæɑouəaɔɝ" #used for syllable counts

def count_sylls(word:str):
    return len(re.findall(f"[{vowels}]+",word))#how many vowel clusters?


syll_buckets = defaultdict(lambda: [])
eng2IPA = {}
IPA2eng = {}
for pair in open("en_US.txt").readlines():
    pair = pair.strip().split("\t")
    pair[1] = re.sub("[/ˈˌ]","",pair[1])#remove slashes and stress markers
    eng2IPA[pair[0]] = pair[1]
    IPA2eng[pair[1]] = pair[0]
    syll_buckets[count_sylls(pair[1])].append(pair[0])


def sample_word(num_syllables):
    return random.choice(syll_buckets[num_syllables])


print(f"Fetching {NUM_SYLLABLES} syllable words for the {"first" if FIRST_RHYME else "last"} rhymes")
print(f"{len(syll_buckets[NUM_SYLLABLES])} possible words")
rhymes = [sample_word(NUM_SYLLABLES) for i in range(32)]

def play_that_funky_music_white_boy(filename):
    return playsound(filename,block=False)
    #threading.Thread(target=playsound, args=(filename,), daemon=True).start()

#song_path = os.path.join("beats",random.choice(os.listdir("beats")))
song_path = os.path.join("beats","rapgod_74.mp3") #for tempo consistency tests
print(f"Your beat: {song_path[song_path.index("/"):]}")
bpm = float(song_path[song_path.index("_")+1:song_path.index(".mp3")])
if bpm > 135 and not HARD_MODE:
    bpm /= 2
time_betwixt_beats = 60/bpm #time in seconds
sleep(4)#read intro info before it gets cleared

rhymes = rhymes
sound = play_that_funky_music_white_boy(song_path)#you can check its status and stop it with the sound object
window = (["[Get Ready!]","????"]*2 if FIRST_RHYME
          else ["????","[Get Ready!]"]*2)
try:
    rhyme_idx = 0
    for i in range(32 - LOOKAHEAD):
        for beat_count in range(1,5):#1234
            start = time()
            print("\033c", end="")#clears output
            
            cur_bar = "🔵"*beat_count + "🔴"*(4-beat_count) + f"| {window[0]}"
            other_bars = ["🔴"*(4) + f"| {r}" for r in window[1:]]
            print(cur_bar)
            print("\n".join(other_bars))
            if not beat_count  == 4: #not a bar line
                sleep(time_betwixt_beats - (time()-start))
        
        old_window = window[1:]
        if old_window[-1] == "????":
            new_row = [rhymes[rhyme_idx]]
            rhyme_idx += 1
        else:
            new_row = ["????"]
        window = old_window + new_row
        sleep(time_betwixt_beats - (time() - start)) #if it's a bar line, subtract this computation time too
    sound.stop()

except Exception as e: #Lurene Grenier crying and screaming rn
    print(e)
    sound.stop() #can't have a phantom audio thread if it fails








