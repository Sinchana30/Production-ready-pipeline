#-----------------BUILD STAGE----------------------
FROM python:3.9-slim AS builder

# Set up a virtual environment. 

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app
COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


#----------------FINAL STAGE--------------------------

FROM python:3.9-slim

COPY --from=builder  /opt/venv /opt/venv

WORKDIR /app
COPY . .

# Set the path to include the virtual environment's binaries.
ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 5000
CMD ["python", "app.py"] 
