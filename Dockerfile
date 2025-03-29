FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    xvfb \
    x11vnc \
    fluxbox \
    novnc \
    websockify \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set up VNC
RUN mkdir -p /root/.vnc && \
    x11vnc -storepasswd 1234 /root/.vnc/passwd

EXPOSE 8080

CMD ["sh", "-c", \
     "Xvfb :0 -screen 0 1024x768x16 & \
     fluxbox & \
     x11vnc -display :0 -forever -usepw -rfbport 5900 & \
     websockify -D --web=/usr/share/novnc/ 8080 localhost:5900 & \
     python snake.py"]
