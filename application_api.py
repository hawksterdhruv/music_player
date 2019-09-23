import audiotools.player
import audiotools

class PlayerApi:
    def play(self):
        # audiotools.player.available_outputs()
        audio_file = audiotools.open('/home/dhruv/Music/Music/Aisha (2010) ~ 320 VBR/04 - Behke Behke [DoReGaMa].mp3')

        audio_output = audiotools.player.open_output('ALSA')
        replay_gain = audiotools.player.RG_NO_REPLAYGAIN

        player = audiotools.player.Player(audio_output, replay_gain)

        player.open(audio_file)
        player.play()

class LibraryApi:
    pass