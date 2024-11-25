FROM python:3.9-alpine

WORKDIR /app

# Copy all machine code into the image
COPY machine1 /app/machine1
COPY machine2 /app/machine2
COPY machine3 /app/machine3

# Install dependencies (if any)
RUN apk add --no-cache build-base

# Define a startup script to orchestrate services
COPY orchestrate.sh /app/orchestrate.sh
RUN chmod +x /app/orchestrate.sh

CMD ["/app/orchestrate.sh"]
