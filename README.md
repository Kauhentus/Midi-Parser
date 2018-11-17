# Midi-Parser
Simple MIDI parser implemented in Python 2.7

* Supports most midi files
* Returns all the 'tracks' within a song
* A 'track' is an array with all the MIDI events arranged in chronological order with all the event data

## TO DO:
* Fully support running status
* - Current running status support is glitchy, code tries to skip over it
* Support System messages
* - Current Sys messages are kept in raw hex-code
* Port the code to Python 3.6

## How to use:
* Import the `song_class` to start
* Use `song = song_class.Song('<MIDI_file_path>')` to initialize an instance of the `song_class` and also give it the midi file path for parsing
* Use `song.convert()` to parse the midi file
* The `song_class` has a `tracks` variable that stores all of the MIDI event data
