import webview
import audiotools.player
import audiotools
# def load_css(window):
#     window.load_css('body { background: red !important; }')

class Api:
    def play(self):
        # audiotools.player.available_outputs()
        audio_file = audiotools.open('/home/dhruv/Music/Music/Aisha (2010) ~ 320 VBR/04 - Behke Behke [DoReGaMa].mp3')

        audio_output = audiotools.player.open_output('ALSA')
        replay_gain = audiotools.player.RG_NO_REPLAYGAIN

        player = audiotools.player.Player(audio_output, replay_gain)

        player.open(audio_file)
        player.play()
        # player.pause()


if __name__ == '__main__':
    webview.create_window('Load CSS Example', 'index.html',frameless=True,js_api=Api)
    # webview.start(gui='cef')
    webview.start()

