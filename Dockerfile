# talkaty — terminal-native TTS voiceover container
FROM python:3.12-slim

WORKDIR /app
ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    TALKATY_DEFAULT_BACKEND=edge-tts

# Runtime deps: libsndfile (soundfile), ffmpeg (edge-tts audio handling)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
RUN pip install --upgrade pip \
    && pip install .

COPY src /app/src

# Working dir for scripts/audio
WORKDIR /data
VOLUME ["/data"]

ENTRYPOINT ["talkaty"]
CMD ["--help"]
