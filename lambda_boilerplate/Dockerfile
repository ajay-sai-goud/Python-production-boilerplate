# Use the official AWS Lambda base image for Python 3.11
FROM public.ecr.aws/lambda/python:3.11

# Set environment variables for best practices in containers
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install uv, the fast Python package installer
RUN pip install --no-cache-dir uv

# Set the working directory in the container
# /var/task is the default directory where Lambda executes the code
WORKDIR /var/task

# Copy only the files needed for dependency installation first
# This leverages Docker's layer caching.
COPY pyproject.toml ./

# Install project dependencies into the system's site-packages
# This makes them available to the Lambda runtime.
RUN uv pip install --system --no-cache-dir .

# Copy the application source code
COPY ./src ./src

# Set the CMD to your handler
# The format is <file_name>.<handler_function_name>
# Since our handler is in src/app.py, the path is src.app.handler
CMD [ "src.app.handler" ]
