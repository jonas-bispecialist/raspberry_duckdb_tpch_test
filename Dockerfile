# Base Jupyter Development Environment
FROM python:3.11-slim

# Set working directory
WORKDIR /workspace

# Copy requirements
COPY requirements.txt .

# Install base packages first
RUN pip install --no-cache-dir jupyter notebook ipykernel

# Install project requirements
RUN pip install --no-cache-dir -r requirements.txt

# Set up the Python kernel
RUN python -m ipykernel install --name 'python3' --display-name 'raspberry_duckdb_tpch_test'

# Configure Jupyter with password
RUN jupyter notebook --generate-config && \
    echo "from jupyter_server.auth import passwd; \
    c.ServerApp.password = passwd('jupyter')" >> /root/.jupyter/jupyter_notebook_config.py && \
    echo "c.ServerApp.password_required = True" >> /root/.jupyter/jupyter_notebook_config.py

# Start Jupyter
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"] 
