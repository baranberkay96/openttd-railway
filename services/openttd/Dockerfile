FROM debian:bookworm-slim@sha256:734a72b3d6142a71993b4bc580ca01d8ca687f77a2c422d96a961d3376b179bc AS download
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl xz-utils unzip && rm -rf /var/lib/apt/lists/*
WORKDIR /download
RUN curl -fL --retry 5 --retry-all-errors https://cdn.openttd.org/openttd-releases/15.3/openttd-15.3-linux-generic-amd64.tar.xz -o openttd.tar.xz \
 && echo 'f49eb25d61b00f8f4d332fee02b530ad75552d1efb8f2bb01e7ca5e6540fe059  openttd.tar.xz' | sha256sum -c - \
 && mkdir /opt/openttd && tar -xJf openttd.tar.xz -C /opt/openttd --strip-components=1 \
 && curl -fL --retry 5 --retry-all-errors https://cdn.openttd.org/opengfx-releases/8.0/opengfx-8.0-all.zip -o opengfx.zip \
 && echo '43a0c1dabf39cb865394f3a6cc36d4da5c10ecfaaf55652043104806810903be  opengfx.zip' | sha256sum -c - \
 && unzip opengfx.zip && tar -xf opengfx-8.0.tar -C /opt/openttd/baseset
FROM debian:bookworm-slim@sha256:734a72b3d6142a71993b4bc580ca01d8ca687f77a2c422d96a961d3376b179bc
RUN apt-get update && apt-get install -y --no-install-recommends python3 libglib2.0-0 libgomp1 ca-certificates \
 && rm -rf /var/lib/apt/lists/* && useradd --uid 10001 --home-dir /data --no-create-home openttd
COPY --from=download /opt/openttd /opt/openttd
COPY server.py /opt/server.py
ENV HOME=/data XDG_DATA_HOME=/data/.local/share XDG_CONFIG_HOME=/data/.config
WORKDIR /data
EXPOSE 3979/tcp 8080/tcp
STOPSIGNAL SIGTERM
ENTRYPOINT ["python3", "-u", "/opt/server.py"]
