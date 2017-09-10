
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst


player = None
playing = False


def on_tag(bus, msg):
    taglist = msg.parse_tag()
    print('on_tag:')
    for key in taglist.keys():
        print('\t%s = %s' % (key, taglist[key]))


def init_player():
    global player
    Gst.init([])

    player = Gst.ElementFactory.make("playbin", "player")

    bus = player.get_bus()
    bus.enable_sync_message_emission()
    bus.add_signal_watch()
    bus.connect('message::tag', on_tag)


def set_uri(uri):
    global player
    player.set_property('uri', uri)


def set_playing(bool_playing):
    global playing
    if bool_playing:
        playing = True
    playing = False


def is_playing():
    return playing


def play():
    global player
    set_playing(1)
    player.set_state(Gst.State.PLAYING)


def null():
    global player
    set_playing(0)
    player.set_state(Gst.State.NULL)
