import numpy as np
import wave
import subprocess
import os
import tempfile
from scipy.signal import resample

def read_wav_file(file_path):
    """Read WAV file and return the data and sample rate."""
    with wave.open(file_path, 'rb') as wf:
        sample_rate = wf.getframerate()
        n_frames = wf.getnframes()
        data = wf.readframes(n_frames)
        samples = np.frombuffer(data, dtype=np.int16)
    return samples, sample_rate

def resample_audio(samples, original_rate, target_rate):
    """Resample audio to the target sample rate."""
    num_samples = int(len(samples) * (target_rate / original_rate))
    resampled_samples = resample(samples, num_samples)
    return resampled_samples

def transmit_wav_file_continuous(file_path, frequency=150500000, tx_gain=20, target_sample_rate=2000000):
    """Continuously transmit WAV file using hackrf_transfer."""
    samples, sample_rate = read_wav_file(file_path)
    
    # Resample the audio to the target sample rate
    resampled_samples = resample_audio(samples, sample_rate, target_sample_rate)
    
    # Normalize the samples
    normalized_samples = resampled_samples.astype(np.float32) / np.iinfo(np.int16).max
    
    # Convert normalized samples to uint8 for HackRF
    hackrf_samples = ((normalized_samples + 1) * 127.5).astype(np.uint8)
    
    # Create a temporary file with the resampled data
    with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
        tmpfile.write(hackrf_samples.tobytes())
        tmpfile_path = tmpfile.name

    try:
        while True:
            # Create the command for hackrf_transfer
            hackrf_cmd = [
                'hackrf_transfer',
                '-t', tmpfile_path,
                '-f', str(frequency),
                '-s', str(target_sample_rate),
                '-a', '1',
                '-x', str(tx_gain),
                '-R'  # Repeat mode
            ]

            # Execute the command
            subprocess.run(hackrf_cmd, check=True)
    except KeyboardInterrupt:
        print("Transmission stopped by user")
    finally:
        # Clean up temporary file
        os.remove(tmpfile_path)

def main():
    input_wav = '/home/ew/Desktop/dial_tone.wav'  # Path to your input WAV file

    # Transmit the WAV file continuously
    transmit_wav_file_continuous(input_wav)

if __name__ == "__main__":
    main()
