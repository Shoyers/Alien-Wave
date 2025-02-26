import pygame
import numpy as np
from array import array
import os
import wave

class SoundGenerator:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        
    def _create_sound_buffer(self, data):
        # Amplification du son
        data = data * 1.5  # Augmentation de l'amplitude
        # Limitation pour éviter la distorsion
        data = np.clip(data, -32000, 32000)
        buffer = array('h', (int(x) for x in data))
        return pygame.mixer.Sound(buffer=buffer)
    
    def generate_shoot_sound_wave(self):
        duration = 0.1
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        frequency = 880
        decay = np.exp(-t * 15)
        waveform = np.sin(2 * np.pi * frequency * t) * decay
        waveform += np.sin(4 * np.pi * frequency * t) * 0.5 * decay
        return waveform
    
    def generate_enemy_shoot_sound_wave(self):
        duration = 0.15
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        frequency = 440
        decay = np.exp(-t * 10)
        waveform = np.sin(2 * np.pi * frequency * t) * decay
        waveform += np.sin(2 * np.pi * (frequency * 1.5 + t * 500) * t) * 0.5 * decay
        return waveform
    
    def generate_hit_sound_wave(self):
        duration = 0.1  # Durée du son
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        base_frequency = 1200
        frequency_variation = np.sin(2 * np.pi * 5 * t) * 50  # Variation de fréquence plus douce
        frequency = base_frequency + frequency_variation
        decay = np.exp(-t * 15)  # Ajuster le facteur de décroissance pour un son plus court
        waveform = np.sin(2 * np.pi * frequency * t) * decay
        waveform += np.random.normal(0, 0.1, len(t)) * 0.1 * decay  # Réduire le bruit
        return waveform
    
    def generate_enemy_death_sound_wave(self):
        duration = 0.2
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        base_frequency = 200
        decay = np.exp(-t * 10)
        waveform = np.sin(2 * np.pi * base_frequency * t) * decay
        waveform += np.sin(2 * np.pi * (base_frequency * 0.5) * t) * 0.5 * decay
        waveform += np.random.normal(0, 0.05, len(t)) * 0.05 * decay
        waveform = np.clip(waveform, -1, 1)  # Limiter l'amplitude pour éviter la saturation
        return waveform
    
    def generate_player_hurt_sound_wave(self):
        duration = 0.15
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        base_frequency = 300
        decay = np.exp(-t * 20)
        waveform = np.sin(2 * np.pi * base_frequency * t) * decay
        waveform += np.sin(2 * np.pi * (base_frequency * 0.5) * t) * 0.5 * decay
        waveform = np.clip(waveform, -1, 1)  # Limiter l'amplitude pour éviter la saturation
        return waveform
    
    def save_sound(self, waveform, filename):
        """Sauvegarde un son généré dans un fichier WAV"""
        try:
            # Conversion en format 16-bit PCM
            scaled = np.int16(waveform * 32767)
            # Écriture du fichier WAV
            with wave.open(filename, 'wb') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16 bits
                wav_file.setframerate(self.sample_rate)
                wav_file.writeframes(scaled.tobytes())
            print(f"Son sauvegardé : {filename}")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du son {filename}: {e}")

    def generate_all_sounds(self, sound_dir):
        """Génère et sauvegarde tous les sons du jeu"""
        os.makedirs(sound_dir, exist_ok=True)
        
        # Génération des formes d'onde
        sounds = {
            "shoot.wav": self.generate_shoot_sound_wave(),
            "enemy_shoot.wav": self.generate_enemy_shoot_sound_wave(),
            "hit.wav": self.generate_hit_sound_wave(),
            "enemy_death.wav": self.generate_enemy_death_sound_wave(),
            "player_hurt.wav": self.generate_player_hurt_sound_wave()
        }
        
        # Sauvegarde des sons
        for filename, waveform in sounds.items():
            filepath = os.path.join(sound_dir, filename)
            if not os.path.exists(filepath):
                self.save_sound(waveform, filepath) 