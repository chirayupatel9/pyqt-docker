FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3-pyqt5 \
    libx11-xcb1 \
    libxcb-render0 \
    libxcb-shape0 \
    libxcb-xfixes0 \
    x11-apps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV DISPLAY=:0
ENV QT_X11_NO_MITSHM=1

# Copy your application files to the container
WORKDIR /app
COPY . /app

# Install any additional Python packages
RUN pip install -r requirements.txt
# Command to run your PyQt5 application
CMD ["python", "datafed-qt.py"]
