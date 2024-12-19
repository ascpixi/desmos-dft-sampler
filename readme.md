# Desmos DFT Sampler
This is a demonstration of using the Discrete Fourier Transform (DFT) to allow for playback of any sound under Desmos via its `tone` feature.

The `gen-partials.py` script generates a LaTeX expression that you can paste into Desmos to import your audio of choice. You can use [this graph](https://www.desmos.com/calculator/9x25z32j5c) as the audio player. There are two parameters that determine the quality of the audio: `--window` (`-w`) and `--resolution` (`-R`).
- the `--window` parameter determines the size of a single audio frame, in seconds - the higher the window size, the more blurry the sound becomes. This determines the size of the FFT used to check for the most audible frequencies in the signal. (sane range: `0.025` to `0.0625`)
- the `--resolution` parameter determines the amount of partials (individual frequencies) in each audio frame. For example, a value of `1` will cause the signal to be composed of only a single sine wave. (sane range: `4` to `64`)

> [!WARNING]
> Copying extremely large LaTeX expressions will slow down Desmos considerably, sometimes to the point of hanging it entirely. Try experimenting with the quality settings to find the sweet-spot.

You can see the script in action [in this video](https://www.youtube.com/watch?v=rZkUCJyyAKE).