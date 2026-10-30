"""Build the 134.3 s music and effects track from licensed local sources."""
from array import array
from pathlib import Path
import math
import shutil
import subprocess
import tempfile
import wave

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
RATE = 48000
DURATION = 134.3
FRAMES = round(RATE * DURATION)
FFMPEG = shutil.which("ffmpeg") or r"C:\Users\Yixiang Zou\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe"


def decode(source: Path, target: Path, duration=None):
    command = [FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-i", str(source)]
    if duration:
        command += ["-t", str(duration)]
    command += ["-ac", "2", "-ar", str(RATE), "-c:a", "pcm_s16le", str(target)]
    subprocess.run(command, check=True)
    with wave.open(str(target), "rb") as wav:
        raw = array("h")
        raw.frombytes(wav.readframes(wav.getnframes()))
    return raw


# Each row: asset, starting second, level. Long source files are windowed below
# so their audible action ends with the on-screen action.
EVENTS = [
    ("impact-bass-1", 0.00, 0.82), ("whoosh", 0.00, 0.50),
    ("whoosh-short", 1.22, 0.40), ("whoosh-short", 1.68, 0.40),
    ("impact-bass-1", 4.25, 0.72), ("whoosh", 4.25, 0.48),
    ("pop", 7.15, 0.50),
    ("glitch-2", 9.60, 0.62), ("error", 12.45, 0.65),
    ("riser", 8.25, 0.20), ("whoosh-cinematic", 11.65, 0.40),
    ("impact-bass-2", 17.03, 0.90), ("whoosh", 17.03, 0.72),
    ("impact-bass-1", 19.10, 0.43), ("impact-bass-1", 21.15, 0.43),
    ("impact-bass-1", 25.50, 0.77), ("whoosh", 25.50, 0.60),
    ("ping", 29.03, 0.38), ("ping", 29.53, 0.38),
    ("impact-bass-1", 34.00, 0.73), ("whoosh", 34.00, 0.50),
    ("glitch-1", 38.25, 0.81), ("impact-bass-2", 38.25, 0.78),
    ("whoosh-cinematic", 37.55, 0.31),
    ("impact-bass-1", 42.50, 0.82), ("whoosh", 42.50, 0.60),
    ("ping", 44.10, 0.43), ("ping", 45.40, 0.43),
    ("whoosh-short", 46.40, 0.40), ("impact-bass-1", 48.05, 0.45),
    ("impact-bass-1", 51.00, 0.67), ("whoosh", 51.00, 0.47),
    ("click", 53.00, 0.44), ("whoosh-short", 55.20, 0.56),
    ("impact-bass-1", 55.20, 0.35),
    ("impact-bass-1", 59.50, 0.70), ("whoosh", 59.50, 0.50),
    ("click", 61.10, 0.42), ("click", 62.15, 0.42),
    ("glitch-1", 64.00, 0.52), ("impact-bass-2", 64.00, 0.42),
    ("impact-bass-1", 68.00, 0.70), ("whoosh", 68.00, 0.48),
    ("ping", 70.55, 0.38), ("ping", 72.80, 0.38),
    ("whoosh-short", 75.00, 0.42),
    ("whoosh", 76.00, 0.38), ("impact-bass-1", 76.00, 0.38),
    ("click", 79.05, 0.38), ("click", 80.40, 0.38),
    ("whoosh", 84.50, 0.42), ("impact-bass-1", 84.50, 0.38),
    ("click", 87.15, 0.38), ("impact-bass-1", 89.70, 0.46),
    ("riser", 92.18, 0.21), ("whoosh-cinematic", 89.00, 0.35),
    ("impact-bass-2", 93.36, 0.67), ("impact-bass-1", 93.56, 0.88),
    ("glitch-1", 93.56, 0.62), ("whoosh", 93.56, 0.66),
    ("ping", 96.00, 0.42), ("whoosh-short", 97.25, 0.46),
    ("impact-bass-1", 102.06, 0.70), ("whoosh", 102.06, 0.52),
    ("whoosh-short", 104.50, 0.48), ("ping", 105.65, 0.36),
    ("impact-bass-2", 110.56, 0.76), ("whoosh", 110.56, 0.54),
    ("click", 112.55, 0.44), ("click", 114.25, 0.44),
    ("whoosh-short", 115.40, 0.42),
    ("impact-bass-1", 119.06, 0.82), ("whoosh", 119.06, 0.56),
    ("click", 121.10, 0.46), ("click", 123.00, 0.46),
    ("click", 124.90, 0.46),
    ("impact-bass-2", 127.56, 0.72), ("whoosh", 127.56, 0.48),
    ("ping", 130.85, 0.38),
]

# source offset, kept length, fade-in, fade-out (seconds). The original riser
# and cinematic whoosh peak well inside their files; choose the energetic slice
# rather than keeping their 10 s / 5.5 s source tails.
WINDOWS = {
    "impact-bass-1": (0.00, .92, .01, .30),
    "impact-bass-2": (1.42, 1.00, .02, .30),
    "glitch-1": (.24, .88, .01, .22),
    "glitch-2": (.52, 1.02, .01, .25),
    "error": (.33, .82, .01, .23),
    "riser": (2.12, 1.38, .16, .05),
    "whoosh-cinematic": (1.92, 1.18, .05, .30),
    "ping": (.06, .59, .01, .21),
    "pop": (0.00, .44, .01, .16),
}

# Brief music reductions leave room for impacts and longer effects.
DUCKS = [(0, .56), (4.25, .62), (9.6, .58), (12.45, .60),
         (17.03, .36), (19.1, .55), (21.15, .55), (25.5, .42),
         (34, .48), (38.25, .34), (42.5, .42), (48.05, .52),
         (51, .55), (55.2, .65), (59.5, .55), (64, .50),
         (68, .52), (75, .75), (76, .68), (84.5, .67),
         (89.7, .58), (93.56, .33), (96, .58),
         (102.06, .52), (104.5, .64), (110.56, .43),
         (119.06, .39), (127.56, .48)]


def duck_at(t):
    factor = 1.0
    for center, low in DUCKS:
        dt = t - center
        if -.08 <= dt < 0:
            g = 1 - (1 - low) * ((dt + .08) / .08)
        elif 0 <= dt < .16:
            g = low
        elif .16 <= dt < .70:
            g = low + (1 - low) * ((dt - .16) / .54)
        else:
            continue
        factor = min(factor, g)
    return factor


with tempfile.TemporaryDirectory() as tempdir:
    temp = Path(tempdir)
    music = decode(ASSETS / "bgm.mp3", temp / "bgm.wav", DURATION)
    music.extend([0] * (FRAMES * 2 - len(music)))
    mix = array("f", [0.0]) * (FRAMES * 2)
    for frame in range(FRAMES):
        gain = .73 * duck_at(frame / RATE)
        p = frame * 2
        mix[p] = music[p] / 32768 * gain
        mix[p + 1] = music[p + 1] / 32768 * gain

    decoded = {}
    for name, start, gain in EVENTS:
        if name not in decoded:
            decoded[name] = decode(ASSETS / "sfx" / f"{name}.mp3", temp / f"{name}.wav")
        source = decoded[name]
        offset, duration, fade_in, fade_out = WINDOWS.get(name, (0, len(source)/(RATE*2), 0, 0))
        sound = source[round(offset * RATE) * 2:round((offset + duration) * RATE) * 2]
        begin = round(start * RATE) * 2
        count = min(len(sound), len(mix) - begin)
        for i in range(count):
            t = i / (RATE * 2)
            fade = min(1.0, t / fade_in if fade_in else 1.0,
                       (duration - t) / fade_out if fade_out else 1.0)
            mix[begin + i] += sound[i] / 32768 * gain * .55 * max(0, fade)

    # Gentle saturation keeps the layered impacts distinct without hard clipping.
    output = array("h")
    for value in mix:
        limited = math.tanh(value * .9)
        output.append(round(max(-1, min(1, limited)) * 32767))
    wav_out = temp / "film-mix.wav"
    with wave.open(str(wav_out), "wb") as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(RATE)
        wav.writeframes(output.tobytes())
    subprocess.run([FFMPEG, "-hide_banner", "-loglevel", "error", "-y", "-i", str(wav_out),
                    "-c:a", "libmp3lame", "-b:a", "320k", str(ASSETS / "film-mix.mp3")], check=True)
print(ASSETS / "film-mix.mp3")
