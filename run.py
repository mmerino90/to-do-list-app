"""Application entry point."""
from app import create_app

app = create_app()

import os

if __name__ == "__main__":
    # Enable Prometheus metrics in development
    os.environ["DEBUG_METRICS"] = "1"
    app.run(host="0.0.0.0", port=8080)