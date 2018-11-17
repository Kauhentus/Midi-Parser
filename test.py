from midi_parser import song_class

song = song_class.Song('Invention1.mid')
song.convert()
song.tracks_to_event()
# song.tracks_to_time()

for i in range(0, len(song.tracks)):
    for j in range(0, len(song.tracks[i])):
        print(song.tracks[i][j])

print(song.parser.tick_div)
