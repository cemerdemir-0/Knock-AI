import os
import numpy as np
import wave
import io

SR = 44100

# Kullanicinin indirdigi ses dosyasi — varsa bu kullanilir, yoksa numpy fallback
MP3_FILE = "dragon-studio-door-opening-454242.mp3"


def _knock(freq, body_decay, n_knocks, gap_s, sr=SR):
    """
    Realistic door knock: short impact transient + long body resonance.
    freq      : door body frequency in Hz (lower = heavier door)
    body_decay: decay rate of resonance (smaller = longer ring)
    n_knocks  : number of knocks
    gap_s     : seconds between knock onsets
    """
    knock_dur = 0.6  # each knock slot (s)
    total_s   = gap_s * (n_knocks - 1) + knock_dur + 0.4  # tail
    n_total   = int(sr * total_s)
    n_knock   = int(sr * knock_dur)
    t         = np.linspace(0, knock_dur, n_knock, endpoint=False)

    # Impact transient: very short noise burst (knuckle hit)
    impact = np.random.randn(n_knock) * np.exp(-350 * t)

    # Body resonance: door vibrating after impact
    body   = np.sin(2 * np.pi * freq * t) * np.exp(-body_decay * t)

    # Second harmonic for richness
    body  += np.sin(2 * np.pi * freq * 2.1 * t) * np.exp(-body_decay * 1.8 * t) * 0.3

    single = impact * 0.35 + body * 1.0

    out = np.zeros(n_total)
    for k in range(n_knocks):
        start = int(k * gap_s * sr)
        end   = start + n_knock
        if end <= n_total:
            out[start:end] += single

    return out


def _add_reverb(sig, delay_s=0.06, decay=0.28, sr=SR):
    """Simple single-echo reverb."""
    delay_samp = int(delay_s * sr)
    out = sig.copy()
    if delay_samp < len(out):
        out[delay_samp:] += sig[:len(out) - delay_samp] * decay
    return out


def _to_wav(signal, sr=SR):
    sig = signal / (np.max(np.abs(signal)) + 1e-9) * 0.88
    pcm = (sig * 32767).astype(np.int16)
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(pcm.tobytes())
    return buf.getvalue()


def _billy():
    """Saloon ahsap kapisi: 3 sert, net vurus, orta frekans."""
    sig = _knock(freq=230, body_decay=5.0, n_knocks=3, gap_s=0.38)
    return _add_reverb(sig, delay_s=0.055, decay=0.22)


def _vietnam():
    """Agir celik sinak kapisi: 2 guclu vurus, derin metalik rezonans."""
    sig = _knock(freq=110, body_decay=3.0, n_knocks=2, gap_s=0.60)
    # Metalik tiz ust ton
    t   = np.linspace(0, len(sig) / SR, len(sig), endpoint=False)
    sig += np.sin(2 * np.pi * 780 * t) * np.exp(-18 * t) * 0.18
    return _add_reverb(sig, delay_s=0.08, decay=0.35)


def _dylan():
    """Apartman kapisi: 3 orta agirlikta vurus, canlı resonans."""
    sig = _knock(freq=310, body_decay=6.0, n_knocks=3, gap_s=0.28)
    return _add_reverb(sig, delay_s=0.04, decay=0.18)


def _survivor():
    """Dev tas/ahsap kapi: 2 cok agir vurus, uzun derin rezonans."""
    sig = _knock(freq=75, body_decay=2.0, n_knocks=2, gap_s=0.75)
    return _add_reverb(sig, delay_s=0.10, decay=0.40)


_SOUND_FNS = {
    "billy":    _billy,
    "vietnam":  _vietnam,
    "dylan":    _dylan,
    "survivor": _survivor,
}


def generate_door_sound(door_title: str) -> tuple:
    """
    Returns (audio_bytes, mime_type).
    MP3 dosyasi varsa onu kullanir, yoksa numpy ile WAV uretir.
    """
    if os.path.exists(MP3_FILE):
        with open(MP3_FILE, "rb") as f:
            return f.read(), "audio/mpeg"

    # Fa