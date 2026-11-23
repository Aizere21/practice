import pygame


class MusicPlayer:
    def __init__(self):
        self.playlist = [
            {
                "name": "Song 1",
                "file": "music/song1.mp3",
                "duration": 180
            },
            {
                "name": "Song 2",
                "file": "music/song2.mp3",
                "duration": 200
            },
            {
                "name": "Song 3",
                "file": "music/song3.mp3",
                "duration": 150
            }
        ]

        self.current_track = 0
        self.is_playing = False

    def play(self):
        track = self.playlist[self.current_track]

        print("Playing:", track["file"])

        pygame.mixer.music.load(track["file"])
        pygame.mixer.music.play()

        self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self):
        self.current_track += 1

        if self.current_track >= len(self.playlist):
            self.current_track = 0

        self.play()

    def previous_track(self):
        self.current_track -= 1

        if self.current_track < 0:
            self.current_track = len(self.playlist) - 1

        self.play()

    def get_track_name(self):
        return self.playlist[self.current_track]["name"]

    def get_progress(self):
        if self.is_playing:
            position = pygame.mixer.music.get_pos() // 1000
            duration = self.playlist[self.current_track]["duration"]
            return position, duration

        return 0, self.playlist[self.current_track]["duration"]