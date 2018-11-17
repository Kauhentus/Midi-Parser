# Midi-Parser
Simple MIDI parser implemented in Python 2.7

* Supports most midi files
* Returns all the 'tracks' within a song
* A 'track' is an array with all the MIDI events arranged in chronological order with all the event data

# TO DO:
* Fully support running status
* - Current running status support is glitchy, code tries to skip over it
* Support System messages
* - Current Sys messages are kept in raw hex-code
