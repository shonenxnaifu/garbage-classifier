# FROM python:3.10-slim
#
# WORKDIR /app
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
#
# COPY ./app ./app
#
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8123"]

# Stage 1: Build Environment
FROM python:3.10 as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2: Runtime Environment
FROM python:3.10-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

# Ensure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8123"]

# Stage 1: Build Environment
# FROM python:3.10-slim as builder
#
# RUN python -m venv /vgarbage
# ENV PATH="/vgarbage/bin:$PATH"
#
# WORKDIR /app
# COPY requirements.txt .
#
# RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime Environment
# FROM python:3.10-slim
# COPY --from=builder /vgarbage /vgarbage
# ENV PATH="/vgarbage/bin:$PATH"
#
# WORKDIR /app
# COPY . .
#
# RUN rm -rf /root/.cache/pip
#
# CMD [ "uvcorn", "main.app", "--host", "0.0.0.0", "--port", "8123" ]
