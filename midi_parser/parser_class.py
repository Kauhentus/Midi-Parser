import binascii


class Parser:
    def __init__(self, file_path):
        self.file_path = file_path  # Tracks to be parsed
        
        self.tracks = []
        self.track_positions = []
        self.hex_data = []
        
        self.midi_format = -1
        self.track_count = -1
        self.tick_div = -1

    def load_song(self):
        midi_file = open(self.file_path, "rb")
        with midi_file:
            raw_bin_data = midi_file.read()

            hex_data_string = binascii.hexlify(raw_bin_data).encode('UTF-8')
            self.hex_data = [hex_data_string[i:i + 2] for i in range(0, len(hex_data_string), 2)]

        self.midi_format = int(self.hex_data[8] + self.hex_data[9], 16)
        self.track_count = int(self.hex_data[10] + self.hex_data[11], 16)
        self.tick_div = int(self.hex_data[12] + self.hex_data[13], 16)
    
    def parse_track_positions(self):
        self.track_positions = []

        finding_tracks = True
        i_ft = 14
        while finding_tracks:
            track_start = i_ft
            i_ft += 4
            track_length = int(self.hex_data[i_ft] + self.hex_data[i_ft + 1] + self.hex_data[i_ft + 2] + self.hex_data[i_ft + 3], 16)

            i_ft += track_length + 4
            track_end = i_ft

            self.track_positions.append([track_start, track_end])

            if i_ft >= len(self.hex_data):
                finding_tracks = False

    def parse_tracks(self):
        for i in range(0, len(self.track_positions)):
            current_track = []
            current_track_parsing = True

            i_ctp = self.track_positions[i][0] + 8
            current_track.append(['MTrk', int(
                self.hex_data[i_ctp - 4] + self.hex_data[i_ctp - 3] + self.hex_data[i_ctp - 2] + self.hex_data[i_ctp - 1], 16)])

            while current_track_parsing:
                ###########################################################
                # Find variable value
                var_val_str_arr = []
                var_val_parsing = True
                while var_val_parsing:
                    if int(self.hex_data[i_ctp], 16) > 80:
                        var_val_str_arr.append(self.hex_data[i_ctp])
                        i_ctp += 1
                    else:
                        var_val_str_arr.append(self.hex_data[i_ctp])
                        var_val_parsing = False
                        i_ctp += 1
                var_val_str = ''.join(var_val_str_arr)
                ###########################################################
                var_val = int(var_val_str, 16)

                # Midi Event

                previous_event = ''
                """
                Change previous event to include a possible <length> variable 
                for the text variables
                """

                # Note Off
                if self.hex_data[i_ctp][0] == '8':
                    channel = int(self.hex_data[i_ctp][1], 16)
                    i_ctp += 1

                    note = int(self.hex_data[i_ctp], 16)
                    velocity = int(self.hex_data[i_ctp + 1], 16)
                    previous_event = self.hex_data[i_ctp] + self.hex_data[i_ctp + 1]
                    i_ctp += 2

                    current_track.append([var_val, 'midi', 'note_off', channel, note, velocity])

                # Note On
                elif self.hex_data[i_ctp][0] == '9':
                    channel = int(self.hex_data[i_ctp][1], 16)
                    i_ctp += 1

                    note = int(self.hex_data[i_ctp], 16)
                    velocity = int(self.hex_data[i_ctp + 1], 16)
                    previous_event = self.hex_data[i_ctp] + self.hex_data[i_ctp + 1]
                    i_ctp += 2

                    current_track.append([var_val, 'midi', 'note_on', channel, note, velocity])

                # Polyphonic Pressure
                elif self.hex_data[i_ctp][0] == 'a':
                    channel = int(self.hex_data[i_ctp][1], 16)
                    i_ctp += 1

                    note = int(self.hex_data[i_ctp], 16)
                    pressure = int(self.hex_data[i_ctp + 1], 16)
                    previous_event = self.hex_data[i_ctp] + self.hex_data[i_ctp + 1]
                    i_ctp += 2

                    current_track.append([var_val, 'midi', 'polyphonic_pressure', channel, note, pressure])

                # Controller
                elif self.hex_data[i_ctp][0] == 'b':
                    channel = int(self.hex_data[i_ctp][1], 16)
                    i_ctp += 1

                    controller = int(self.hex_data[i_ctp], 16)
                    value = int(self.hex_data[i_ctp + 1], 16)
                    previous_event = self.hex_data[i_ctp] + self.hex_data[i_ctp + 1]
                    i_ctp += 2

                    current_track.append([var_val, 'midi', 'controller', channel, controller, value])

                # Program Change
                elif self.hex_data[i_ctp][0] == 'c':
                    channel = int(self.hex_data[i_ctp][1], 16)
                    i_ctp += 1

                    program = int(self.hex_data[i_ctp], 16)
                    previous_event = self.hex_data[i_ctp]
                    i_ctp += 1

                    current_track.append([var_val, 'midi', 'program_change', channel, program])

                # Channel Pressure
                elif self.hex_data[i_ctp][0] == 'd':
                    channel = int(self.hex_data[i_ctp][1], 16)
                    i_ctp += 1

                    pressure = int(self.hex_data[i_ctp], 16)
                    previous_event = self.hex_data[i_ctp]
                    i_ctp += 1

                    current_track.append([var_val, 'midi', 'channel_pressure', channel, pressure])

                # Pitch Bend
                elif self.hex_data[i_ctp][0] == 'e':
                    channel = int(self.hex_data[i_ctp][1], 16)

                    i_ctp += 1

                    lsb = int(self.hex_data[i_ctp], 16)
                    msb = int(self.hex_data[i_ctp + 1], 16)
                    previous_event = self.hex_data[i_ctp] + self.hex_data[i_ctp + 1]

                    i_ctp += 2

                    current_track.append([var_val, 'midi', 'program_change', channel, lsb, msb])

                # Meta Event
                elif self.hex_data[i_ctp] == 'ff':
                    i_ctp += 1

                    # Sequence Number
                    if self.hex_data[i_ctp] == '00':
                        i_ctp += 1
                        if self.hex_data[i_ctp] == '02':
                            i_ctp += 1
                            current_track.append([var_val, 'meta', 'sequence_number', int(self.hex_data[i_ctp] + self.hex_data[i_ctp + 1], 16)])
                            previous_event = self.hex_data[i_ctp] + self.hex_data[i_ctp + 1]
                            i_ctp += 2

                    # Text-Based Events 01 - 09
                    elif self.hex_data[i_ctp] == '01' or self.hex_data[i_ctp] == '02' or self.hex_data[i_ctp] == '03' or self.hex_data[i_ctp] == '04' or self.hex_data[i_ctp] == '05' or self.hex_data[i_ctp] == '06' or self.hex_data[i_ctp] == '07' or self.hex_data[i_ctp] == '08' or self.hex_data[i_ctp] == '09':
                        i_ctp += 1
                        event_id = self.hex_data[i_ctp - 1]

                        ###########################################################
                        # Find variable value
                        txt_var_val_str_arr = []
                        txt_var_val_parsing = True
                        while txt_var_val_parsing:
                            if int(self.hex_data[i_ctp], 16) > 80:
                                txt_var_val_str_arr.append(self.hex_data[i_ctp])
                                i_ctp += 1
                            else:
                                txt_var_val_str_arr.append(self.hex_data[i_ctp])
                                txt_var_val_parsing = False
                                i_ctp += 1
                        txt_var_val_str = ''.join(txt_var_val_str_arr)
                        ###########################################################
                        txt_var_val = int(txt_var_val_str, 16)

                        txt_str = ''
                        for txt_i in range(i_ctp, i_ctp + txt_var_val):
                            txt_str += chr(int(self.hex_data[i_ctp], 16))
                            i_ctp += 1

                        switcher = {
                            '01': "text",
                            '02': "copyright",
                            '03': "track_name",
                            '04': "instrument_name",
                            '05': "lyric",
                            '06': "marker",
                            '07': "cue_point",
                            '08': "program_name",
                            '09': "device_name"
                        }
                        event_type = switcher.get(event_id, "text")
                        current_track.append([var_val, 'meta', event_type, txt_str])
                        previous_event = str(var_val) + txt_str

                    # Midi Channel Prefix
                    elif self.hex_data[i_ctp] == '20':
                        i_ctp += 1
                        if self.hex_data[i_ctp] == '01':
                            i_ctp += 1

                            current_track.append([var_val, 'meta', 'midi_channel_prefix', int(self.hex_data[i_ctp], 16)])
                            previous_event = self.hex_data[i_ctp]

                            i_ctp += 1

                    # Midi Port
                    elif self.hex_data[i_ctp] == '21':
                        i_ctp += 1
                        if self.hex_data[i_ctp] == '01':
                            i_ctp += 1

                            current_track.append([var_val, 'meta', 'midi_port', int(self.hex_data[i_ctp], 16)])
                            previous_event = self.hex_data[i_ctp]

                            i_ctp += 1

                    # End of Track
                    elif self.hex_data[i_ctp] == '2f':
                        i_ctp += 1
                        if self.hex_data[i_ctp] == '00':
                            i_ctp += 1

                            current_track.append([var_val, 'meta', 'end_track'])
                            current_track_parsing = False

                    # Tempo
                    elif self.hex_data[i_ctp] == '51':
                        i_ctp += 1
                        if self.hex_data[i_ctp] == '03':
                            i_ctp += 1

                            tempo = int(self.hex_data[i_ctp] + self.hex_data[i_ctp + 1] + self.hex_data[i_ctp + 2], 16)
                            previous_event = self.hex_data[i_ctp] + self.hex_data[i_ctp + 1] + self.hex_data[i_ctp + 2]

                            i_ctp += 3

                            current_track.append([var_val, 'meta', 'tempo', tempo])

                    # SMPTE Offset
                    elif self.hex_data[i_ctp] == '57':
                        i_ctp += 1
                        if self.hex_data[i_ctp] == '05':
                            i_ctp += 1

                            hr = int(self.hex_data[i_ctp], 16)
                            mn = int(self.hex_data[i_ctp + 1], 16)
                            ss = int(self.hex_data[i_ctp + 2], 16)
                            fr = int(self.hex_data[i_ctp + 3], 16)
                            ff = int(self.hex_data[i_ctp + 4], 16)
                            previous_event = self.hex_data[i_ctp] + self.hex_data[i_ctp + 1] + self.hex_data[i_ctp + 2] + self.hex_data[i_ctp + 3] + self.hex_data[i_ctp + 4]
                            i_ctp += 5

                            current_track.append([var_val, 'meta', 'smpte_offset', hr, mn, ss, fr, ff])

                    # Time Signature
                    elif self.hex_data[i_ctp] == '58':
                        i_ctp += 1
                        if self.hex_data[i_ctp] == '04':
                            i_ctp += 1

                            nn = int(self.hex_data[i_ctp], 16)
                            dd = int(self.hex_data[i_ctp + 1], 16)
                            cc = int(self.hex_data[i_ctp + 2], 16)
                            bb = int(self.hex_data[i_ctp + 3], 16)
                            previous_event = self.hex_data[i_ctp + 0] + self.hex_data[i_ctp + 1] + self.hex_data[i_ctp + 2] + self.hex_data[i_ctp + 3]
                            i_ctp += 4

                            current_track.append([var_val, 'meta', 'time_signature', nn, dd, cc, bb])

                    # Key Signature
                    elif self.hex_data[i_ctp] == '59':
                        i_ctp += 1
                        if self.hex_data[i_ctp] == '02':
                            i_ctp += 1

                            sf = int(self.hex_data[i_ctp], 16)
                            mi = int(self.hex_data[i_ctp + 1], 16)
                            previous_event = self.hex_data[i_ctp] + self.hex_data[i_ctp + 1]
                            i_ctp += 2

                            current_track.append([var_val, 'meta', 'key_signature', sf, mi])

                    # Sequencer Specific Event
                    elif self.hex_data[i_ctp] == '7f':
                        i_ctp += 1

                        ###########################################################
                        # Find variable value
                        sys_var_val_str_arr = []
                        sys_var_val_parsing = True
                        while sys_var_val_parsing:
                            if int(self.hex_data[i_ctp], 16) > 80:
                                sys_var_val_str_arr.append(self.hex_data[i_ctp])
                                i_ctp += 1
                            else:
                                sys_var_val_str_arr.append(self.hex_data[i_ctp])
                                sys_var_val_parsing = False
                                i_ctp += 1
                        sys_var_val_str = ''.join(sys_var_val_str_arr)
                        ###########################################################
                        sys_var_val = int(sys_var_val_str, 16)

                        sys_str = ''
                        for sys_i in range(i_ctp, i_ctp + sys_var_val):
                            sys_str += self.hex_data[i_ctp]
                            i_ctp += 1

                        current_track.append([var_val, 'meta', 'sequencer_specific_event', sys_str])
                        previous_event = sys_str

                # System Event (WIP)
                elif self.hex_data[i_ctp] == 'f7' or self.hex_data[i_ctp] == 'f0':
                    i_ctp += 1

                    sys_event_data_hex = [self.hex_data[i_ctp - 1]]
                    parsing_sys_event = True

                    while parsing_sys_event:
                        if self.hex_data[i_ctp] == 'f7' or self.hex_data[i_ctp] == 'f0':
                            # print(self.hex_data[i_ctp])
                            parsing_sys_event = False
                        sys_event_data_hex.append(self.hex_data[i_ctp])
                        i_ctp += 1

                    sys_event_data_hex_str = ''.join(sys_event_data_hex)
                    current_track.append([var_val, 'system_event', sys_event_data_hex_str])

                # Running Status
                else:
                    if previous_event != '':
                        i_ctp += len(previous_event) / 2
                        print(previous_event)

            self.tracks.append(current_track)
