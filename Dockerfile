# Use the official Python slim image
FROM python:3.11-slim

# Prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container.
WORKDIR /app

# Copy the requirements file into the container.
COPY requirements.txt .

# Install any needed packages specified in requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your bot's code into the container.
COPY . .

# Use an environment variable for your bot token.
# When running the container, you can pass this with `-e DISCORD_BOT_TOKEN=your_token`
# ENV DISCORD_BOT_TOKEN=""

# Set the command to run your bot.
CMD ["python", "bot.py"]
