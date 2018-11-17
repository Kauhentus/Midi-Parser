import parser_class
import event_class


class Song:
    def __init__(self, file_path):
        self.file_path = file_path  # Tracks to be parsed\
        self.tracks = []
        self.event_tracks = []
        self.parser = parser_class.Parser(self.file_path)

        self.time_tracks = []

    def convert(self):
        self.parser.load_song()
        self.parser.parse_track_positions()
        self.parser.parse_tracks()

        self.tracks = self.parser.tracks

    def tracks_to_event(self):
        for i in range(0, len(self.tracks)):
            current_event_track = []
            for j in range(0, len(self.tracks[i])):
                current_raw_event = self.tracks[i][j]
                current_event_track.append(event_class.Event(current_raw_event[0], current_raw_event[1], current_raw_event[2:]))
            self.event_tracks.append(current_event_track)

    """ def tracks_to_time(self):
        ticks_per_quarter_note = self.parser.tick_div
        subdivision = ticks_per_quarter_note / 8  # 64 Notes - 16

        print(subdivision)

        longest_track_length = - 1
        for i in range(0, len(self.tracks)):
            if len(self.tracks[i]) >= longest_track_length:
                longest_track_length = len(self.tracks[i])

        self.time_tracks = [[] for i in range(len(self.tracks))]

        for i in range(len(self.tracks)):
            not_finished = True
            current_tick_time = 0
            current_event_running = False
            add_notes = False
            current_note = 0
            current_event_type = 'note_on'
            current_event_time_left = 0
            current_track_index = 0
            current_music_index = 0

            while not_finished:
                print(i, self.tracks[i][current_track_index][1])
                if self.tracks[i][current_track_index][1] == 'midi':
                    if not current_event_running:
                        if self.tracks[i][current_track_index][2] == 'note_on':
                            if self.tracks[i][current_track_index][0] != 0:
                                current_event_running = True
                                current_event_time_left = self.tracks[i][current_track_index][0]
                                current_music_index += 1
                            else:
                                current_event_time_left = 0
                            current_track_index += 1
                            current_event_type = 'note_on'
                            current_note = self.tracks[i][current_track_index][4]

                        elif self.tracks[i][current_track_index][2] == 'note_off':
                            if self.tracks[i][current_track_index][0] != 0:
                                current_event_running = True
                                current_event_time_left = self.tracks[i][current_track_index][0]
                                current_music_index += 1
                            else:
                                current_event_time_left = 0

                            current_track_index += 1
                            current_event_type = 'note_off'
                            current_note = self.tracks[i][current_track_index][4]
                    else:
                        if current_event_time_left <= 0:
                            if current_event_type == 'note_off':
                                add_notes = True
                            elif current_event_type == 'note_on':
                                add_notes = False
                            current_event_running = False

                        else:
                            current_event_time_left -= subdivision
                            current_tick_time += subdivision

                    # print(i, len(self.time_tracks[i]), current_track_index, current_music_index)
                    while len(self.time_tracks[i]) <= current_music_index:
                        empty_list = [0] * 128
                        self.time_tracks[i].append(empty_list)
                        #  print(i, len(self.time_tracks[i]), current_track_index, current_music_index)
                    # print(i, current_track_index, len(self.time_tracks), len(self.time_tracks[i]))
                    current_slice = self.time_tracks[i][current_music_index]

                    print(current_slice, current_tick_time, current_note, current_event_running, current_event_time_left)

                    if add_notes:
                        current_slice[current_note] = 1
                        self.time_tracks[i][current_music_index] = current_slice

                    else:
                        current_slice[current_note] = 0
                        self.time_tracks[i][current_music_index] = current_slice
                else:
                    current_track_index += 1

                if current_track_index >= len(self.tracks[i]):
                    not_finished = False """
