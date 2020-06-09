FROM python:3.7.3-stretch

## Step 1:
# Create a working directory
WORKDIR /app

## Step 2:
# Copy source code to working directory
COPY /app/app.py /app/app.py
COPY /app/config.py /app/config.py
COPY /app/templates /app/templates
COPY .env .env
COPY requirements.txt /app/requirements.txt

## Step 3:
# Install packages from requirements.txt
# hadolint ignore=DL3013
RUN pip install --upgrade pip && \
    pip install --trusted-host pypi.python.org -r requirements.txt

## Step 4:
# Expose port 80
EXPOSE 8000

## Step 5:
# Run app.py at container launch
CMD [ "python", "app.py" ]