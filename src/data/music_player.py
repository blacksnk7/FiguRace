import os
from pygame import mixer

class M_Player:
    '''
    This class is used to control the songs and volume of any sound used in the game. The volume itself is stored in a variable in config.jason.
    '''

    def __init__(self, volume=1.0):
        '''
        This function creates an instance of the object M_Player and initializes the mixer object (which is needed for all song related actions).
        It receives the volume of the sounds and the name of a single song it will start playing the first time the object is created. Should no values be given to the builder,
        then the default values will be used instead. The mixer.Song object requires a file to be instanced, so a song must be given when an instance of M_Player is first created,
        that is why we call the play_menu_song() to initialize the object with a song, without it, the mixer.Sound object could not be instanced.
        '''
        mixer.init()
        self.music_path = os.path.join(os.getcwd(), 'src', 'data', 'music')
        self.update_volume(volume)
        self.muted = False
        self.play_menu_song()

    def play_menu_song(self):
        ''' 
        This function simply changes the currently playing song from whatever it was to background_music.mp3. Should the music be currently muted, then the sound will change but
        it will be instantly stopped so that no sounds are heard.
        '''
        self.restart()
        track_path = os.path.join(self.music_path, 'background_music.mp3')
        self.song = mixer.Sound(track_path)
        self.song.play(loops=-1)
        self.update_volume(self.volume)
        if (self.muted == True):
            self.mute()
            
    def play_game_song(self):
        ''' 
        This function simply changes the currently playing song from whatever it was to playing_music.mp3. Should the music be currently muted, then the sound will change but
        it will be instantly stopped so that no sounds are heard.
        '''
        self.restart()
        track_path = os.path.join(self.music_path, 'playing_music.mp3')
        self.song = mixer.Sound(track_path)
        self.song.play(loops=-1)
        self.update_volume(self.volume)
        if (self.muted == True):
            self.mute()
            
    def play_scores_song(self):
        ''' 
        This function simply changes the currently playing song from whatever it was to scores_music.mp3. Should the music be currently muted, then the sound will change but
        it will be instantly stopped so that no sounds are heard.
        '''
        self.restart()
        track_path = os.path.join(self.music_path, 'scores_music.mp3')
        self.song = mixer.Sound(track_path)
        self.song.play(loops=-1)
        self.update_volume(self.volume)
        if (self.muted == True):
            self.mute()
        
    def restart(self):
        ''' 
        When called, this function stops any currently playing sounds and then re-initializes the mixer module. This is used because otherwise you would have multiple mixer
        objects playing different music at the same time. Whenever a song is played, the previous mixer object must be terminated, and a new one with a new song must be created.
        '''
        self.end()
        mixer.init()
        
    def end(self):
        ''' 
        When called, this function stops any currently playing sounds and then un-initializes the mixer module.
        '''
        mixer.stop()
        mixer.quit()
        
    def mute(self):
        ''' 
        When called, this function stops any currently playing sounds. The muted attribute is used by the M_Player class to detect if the sound is currently muted whenever the
        music changes, so that even if the mixer is shut down and a new mixer with a new song is created it will still be muted. Without the muted flag, the newly created mixer
        would start a new song with the current volume value.
        '''
        mixer.pause()
        self.muted = True
        
    def unmute(self):
        ''' 
        When called, this function re-starts any currently playing sounds. The muted attribute is used by the M_Player class to detect if the sound is currently muted whenever the
        music changes, so that even if the mixer is shut down and a new mixer with a new song is created it will still be muted. Without the muted flag, the newly created mixer
        would start a new song with the current volume value.
        '''
        mixer.unpause()
        self.muted = False
        
    #Poner un slider para la musica
    def update_volume(self, new_volume):
        ''' 
        When called, this function changes the volume attribute of the M_Player. The volume must be a float, since the mixer.Song class uses a volume value between 0 and 1.
        '''
        try:
            new_volume = float(new_volume)
            if (new_volume < 0):
                new_volume = 0
            elif (new_volume > 1):
                new_volume = 1
            self.volume = new_volume
            self.song.set_volume(self.volume)
        except ValueError:
            print('The new volume cannot be turned into a float')
        except Exception as e:
            print(e)
        
    def music_controller(self, model, window, event, values):
        """
        When called, this function controlls the events refered to the musisc system.
        """
        match event:
            case _ if event == '-GO_TO--HOME-' and (model.state["current"]["page"] != '-CONFIG-' and model.state["current"]["page"] != '-PROFILE-'):
                self.play_menu_song()
            case _ if event == '-GO_TO--PLAY-':
                self.play_game_song()
            case _ if event == '-GO_TO--SCORE-':
                self.play_scores_song()
            case '-MUTE-':
                self.mute()
            case '-UN_MUTE-':
                self.unmute()
        