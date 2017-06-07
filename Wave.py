import wave


def extract_audio(input, start, end, output, bufsize=1024):
    wav_in = wave.open(input, 'rb')
    wav_out = wave.open(output, 'wb')
    wav_out.setparams(wav_in.getparams())

    start_pos = int(start * wav_in.getframerate() * wav_in.getnchannels())
    nframes = int((end - start) * wav_in.getframerate() * wav_in.getnchannels())

    wav_in.setpos(start_pos)

    while nframes > 0:
        toread = nframes if nframes < bufsize else bufsize
        buf = wav_in.readframes(toread)
        hasread = len(buf)
        if hasread == 0:
            break
        nframes -= hasread
        wav_out.writeframesraw(buf)

    wav_in.close()
    wav_out.close()
