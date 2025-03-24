# Use a Python image WITH uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim
LABEL authors="IngeniumUAHub"

# Set default enviroment to production, can be overriden
ENV enviroment=production

# Working directory in docker
WORKDIR /dashboard

# -- Installing uv --
# The installer requires curl (and certificates) to download the release archive
# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
COPY . /dashboard

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Place executables in the environment at the front of the path
ENV PATH="/dashboard/.venv/bin:$PATH"
ENV PYTHONPATH="/dashboard"

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []

# Run the Streamlit application
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]