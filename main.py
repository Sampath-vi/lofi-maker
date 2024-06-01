from pydub import AudioSegment, effects

# Function to apply a low-pass filter
def low_pass_filter(audio, cutoff_freq=3000):
    return audio.low_pass_filter(cutoff_freq)

# Function to apply reverb effect
def add_reverb(audio, reverb_amount=0.5):
    reverb_audio = audio
    for _ in range(int(reverb_amount * 10)):
        reverb_audio = reverb_audio.overlay(audio - (6 * _), position=50 * _)
    return reverb_audio

# Function to add background noise
def add_background_noise(audio, noise_file, noise_level=-20):
    noise = AudioSegment.from_file(noise_file)  # Load the specified noise file
    noise = noise - noise.dBFS + noise_level
    
    # Loop the noise to match the length of the audio
    noise_length = len(noise)
    audio_length = len(audio)
    looped_noise = noise * (audio_length // noise_length + 1)
    looped_noise = looped_noise[:audio_length]

    combined = audio.overlay(looped_noise)
    return combined

# Function to slow down the track
def slow_down(audio, speed_factor=0.85):
    return audio._spawn(audio.raw_data, overrides={
         "frame_rate": int(audio.frame_rate * speed_factor)
    }).set_frame_rate(audio.frame_rate)

# Function to add drum loop
def add_drum_loop(audio, drum_file, loop=True):
    drum_loop = AudioSegment.from_file(drum_file)
    if loop:
        drum_loop = drum_loop * (len(audio) // len(drum_loop) + 1)
        drum_loop = drum_loop[:len(audio)]
    combined = audio.overlay(drum_loop)
    return combined

# Function to apply equalization using ffmpeg
def apply_equalization(audio, equalizer_settings):
    # Apply equalizer settings using ffmpeg
    audio.export("temp.wav", format="wav")
    equalized_audio = AudioSegment.from_file("temp.wav")
    for band, gain in equalizer_settings.items():
        equalized_audio = equalized_audio.low_pass_filter(band).apply_gain(gain)
    return equalized_audio

# Function to add vinyl crackle
def add_vinyl_crackle(audio, crackle_file, noise_level=-25):
    crackle = AudioSegment.from_file(crackle_file)  # Load the crackle noise file
    crackle = crackle - crackle.dBFS + noise_level
    
    # Loop the crackle to match the length of the audio
    crackle_length = len(crackle)
    audio_length = len(audio)
    looped_crackle = crackle * (audio_length // crackle_length + 1)
    looped_crackle = looped_crackle[:audio_length]

    combined = audio.overlay(looped_crackle)
    return combined

# Function to apply stereo panning
def apply_stereo_panning(audio):
    return audio.pan(-0.5) + audio.pan(0.5)

# Function to apply tape saturation
def apply_tape_saturation(audio):
    return effects.normalize(audio, headroom=-1.0).apply_gain(2.0)

# Load the input track
input_file = "./OSajniRe.wav"
audio = AudioSegment.from_file(input_file)

# Reduce the volume of the input track
audio = audio - 15  # Reducing the volume by 10dB

# Apply lofi effects
audio = slow_down(audio, speed_factor=0.85)
audio = low_pass_filter(audio)
audio = add_reverb(audio, reverb_amount=0.3)
audio = add_background_noise(audio, "./background_sounds/shopping-square-1.wav", noise_level=-25)
audio = add_background_noise(audio, "./background_sounds/stream-1.wav", noise_level=-35)

# Apply additional effects
equalizer_settings = {
    60: 0,    # Reduce very low frequencies
    230: 0,   # Reduce low frequencies
    910: 0,    # Slightly boost mid frequencies
    3600: 0,  # Reduce high frequencies
    14000: 0  # Reduce very high frequencies
}
# audio = apply_equalization(audio, equalizer_settings)
audio = add_vinyl_crackle(audio, "./background_sounds/vinyl-crackle-33rpm-6065.wav", noise_level=-40)
audio = apply_stereo_panning(audio)
audio = apply_tape_saturation(audio)

# Add hip-hop drum loop
# audio = add_drum_loop(audio, "./background_sounds/shuffle-beat-35198.wav")

# Save the output track
output_file = "lofi_output_track.wav"
audio.export(output_file, format="wav")

print(f"Lofi track saved as {output_file}")
