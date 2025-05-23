# raspberry_duckdb_tpch_test

# 1. Introduction

This repository helps you setup and run TPC-H analytics test on a Raspberry Pi. Ny goal was to see how large volumes of data DuckDB would be able to handle on this limited hardware.

## 1.1 DuckDb
DuckDB, created in 2019, brought OLAP (Online Analytical Processing) to laptops by running efficiently inside applications without a server. Its columnar design and vectorized execution make analytics on local data (e.g., CSV, Parquet) very fast. 

## 1.2 Hardware
To test this out I bought a tiny Raspberry Pi 2W that is a low-cost credit card sized computer with 512 MB ram and a quad-core CPU. The test will run on other versions of Raspberry Pi.

## 1.3 TPC-H Benchmark
To test this I used the TPC-H benchmark which is an industry-standard test for database performance using 22 analytics queries. 

The benchmark has a scale factor that allow you to test different sizes of data. Each scale factor adds 1GB of data or 6M rows to the largest lineitems table.

# 2. Setup Raspberry Pi

Follow this [guide](https://pypi.org/project/duckdb/#files) to setup your Raspberry Pi. To get the most out of the Raspberry Pi i used the Raspberry Pi OS Lite (64-bit).

## 2.1 Install Python packages
Python is installed already we only need to add a few things:

Create virtual env:  
```Python3 -m venv venv```

Activate venv:  
```source venv/bin/activate```

Install the package manager:  
```sudo apt install python3-pip```

## 2.2 DuckDB installation

The pip install DuckDB was very slow on Raspberry Py since pip could not find a precompiled version of DuckDB to install. To make installation much faster we will point pip to the correct pre-compiled version.

Check python 3 version:  
```python3 --version```

Check cpu architecture:  
```uname -m```

Find the correct wheel file at https://pypi.org/project/duckdb/#files

Then pick the .whl with cp3XY matching your Python version and the correct CPU architecture.

*Example - Python 3.11.2 and aarch64 (Raspberry Pi Zero 2W use):   
duckdb-1.3.0-cp311-cp311-manylinux_2_27_aarch64.whl*

Copy the url and add it to the pip install command. For the example above the command becomes:

```pip install https://files.pythonhosted.org/packages/43/21/ffe5aeb9d32a49d2de6d368b3fe3e53c2246eccec916375d65c45dc58339/duckdb-1.3.0-cp311-cp311-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl```

Verify that duckdb installed correctly:  
```python -c "import duckdb; print(duckdb.__version__)"```

## 2.3 Optional: Free up memory on the Raspberry Pi

Running queries RAM intensive and the Raspberry Pi Zero has only 512 MB of ram. Below are some steps you can take to limit the RAM used by the operating system and services that may not be used:

Disable GUI: Boots to command line only, skips desktop to save RAM/CPU:  
```sudo systemctl set-default multi-user.target```

Disable bluetooth background service:  
```sudo systemctl disable bluetooth```

Disables mDNS (Bonjour/Zeroconf), often unused.  
```sudo systemctl disable avahi-daemon```

Disables serial Bluetooth device.  
```sudo systemctl disable hciuart```

Removes leftover dependencies.  
```sudo apt autoremove -y```

Reduce GPU memory by assign only 16MB RAM to GPU (minimum):

1. Open the config file: sudo nano /boot/firmware/config.txt

2. Add a line to the end and save:
```gpu_mem=16```

3. Restart raspberry Pi when done:
```Sudo reboot```

# 3. Generate test data and queries

The notebook \notebook\generate_data_and_queries.ipynb will use DuckDB to generate test data and queries for the TPC-H test.

When running the notebook set the scale_factor variable to test different sizes for the tables. 

Default scale_factor is 1 (runs in about one minute on Raspberry Pi Zero 2W).

The notebook creates parquet files for each table in \src\raw\\<scale_factor>

TPC-H qury 1 to 22 gets created in \src\raw\query.

If you wish to run the test with various scale factors change the variable and rerun the Notebook cell again.

# 4. Running the test

Before running the test on Raspberry Pi transfer the src folder to the SD storage (using terminal or e.g. WinSCP). Note the src folder must contain generated queries and parquet files!

To run the test run \src\run_tpch_test.py either on your machine or run it on the Raspberry Pi using ```python run_tpch_test.py```

Before the test start you must enter the scale factor. To run a certain scale factor those parquet files must have been generated and transfered to the Raspberry Pi.

You can monitor the cpu and RAM on Raspberry Pi using the ```htop``` command from another window.

Example output:

*(venv) pi@raspberrypi2w:~/src $ python run_tpch_test.py
Enter scale factor: 5
Connected to DuckDB
--------- START TCP-H with scale factor  05 ---------
Query 01 finished in 21.1s
Query 02 finished in 3.9s
Query 03 finished in 29.5s
Query 04 finished in 20.6s
Query 05 finished in 25.3s
Query 06 finished in 16.6s
Query 07 finished in 30.3s
Query 08 finished in 38.4s
Query 09 finished in 82.8s
Query 10 finished in 35.2s
Query 11 finished in 4.5s
Query 12 finished in 25.0s
Query 13 finished in 33.9s
Query 14 finished in 33.4s
Query 15 finished in 21.2s
Query 16 finished in 4.1s
Query 17 finished in 38.3s
Query 18 finished in 95.0s
Query 19 finished in 30.2s
Query 20 finished in 33.6s
Query 21 finished in 160.3s
Query 22 finished in 7.2s
--------- END TCP-H in 0:13:11 ---------*

# 5. Links

See [this](https://duckdb.org/2025/01/17/raspberryi-pi-tpch.html) blog post for another more extensive test of TPC-H on a Raspberry Pi.

Also using the [DuckDB TPC-H extension](https://duckdb.org/docs/stable/core_extensions/tpch.html) is probably an easier way to get queries and generate data!
