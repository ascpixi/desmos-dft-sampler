import numpy as np
import argparse
from scipy.io import wavfile

parser = argparse.ArgumentParser()
parser.add_argument("-w", "--window", type=float, required=True)
parser.add_argument("-R", "--resolution", type=int, required=True)
parser.add_argument("-i", "--input", type=str, required=True)
args = parser.parse_args()

window_size: float = args.window
resolution: int = args.resolution
input_path: str = args.input

if window_size < 0.016:
    print(f"warning: window size of {window_size}s requires an update rate faster than 60Hz")
    print("warning: most clients are clamped to 60Hz, meaning Desmos may not catch up!")

sample_rate, audio = wavfile.read(input_path)
N = audio.shape[0]

spw = int(window_size * sample_rate) # samples per window

def spectrum(window_index):
    start_index = window_index * spw
    windowed_signal = audio[start_index:start_index + spw]
    fftr = np.fft.fft(windowed_signal)

    frequencies = np.fft.fftfreq(spw, 1 / sample_rate)[:spw // 2]
    amplitudes = np.abs(fftr[:spw // 2])

    return frequencies, amplitudes

def top(arr, n):
    return np.argpartition(arr, -n)[-n:]

full_fftr = np.fft.fft(audio)
full_amps = np.abs(full_fftr) // 2
max_amp = max(full_amps)

flattened = []
for i in range(N // spw):
    freqs, amps = spectrum(i)
    amps /= max_amp

    top_indices = top(amps, resolution)

    for j in top_indices:
        flattened.append((freqs[j], amps[j]))

result = R"A_{partials}=["
for i in range(len(flattened)):
    frame = flattened[i]

    freq = round(frame[0], 1)
    amp = round(frame[1], 3)

    if amp == 0:
        result += R"("
        result += f"0,0"
        result += R")"
    else:
        freq_str = str(freq).removesuffix(".0")
        amp_str = str(amp).removesuffix(".0")

        result += R"("
        result += f"{freq_str},{amp_str}"
        result += R")"

    if i != len(flattened) - 1:
        result += ","

result += R"]"

with open("result.txt", "w") as file:
    file.write(result)

print("LATEX result written to 'result.txt'")
print(f"Amount of frames: {len(flattened) / resolution}")