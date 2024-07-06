# File-Search Server

## Description

This project is a server-client application that handles requests in parallel, searches for strings in a file, and returns the results. Different search algorithms have been implemented for this purpose, and a general speed report is included in this repo. A `client.py` is included as well for testing purposes. The `reread_on_query` option indicates if the file is to be read for every query (ideal for when the file content is expected to change), or once upon server startup. Follow the instructions below for setting up a self-signed SSL certificate for your development environment or simply turn off SSL in your `.env` file by setting `ssl_enabled=False`. This application can be integrated into larger projects for efficient file searching.

## Setup Instructions

1. Clone the repository, set up a virtual environment and install the requirements in the `requirements.txt` file:

   ```sh
   # Clone the repository
   git clone https://github.com/your-repo/project.git
   
   # Setup and activate your virtual environment
   python -m venv venv
   source venv/bin/activate 
   
   # On Windows use
   venv\Scripts\activate
   
2. Create a .env file with the .env.template in the projects/config directory and adjust to your environment:

   ```sh
   cp projects/config/.env.template projects/config/.env
   
3. Generate an SSL certificate (OPTIONAL - you can simply turn `ssl_enabled=False` for your development environment OR import your own custom certificates) by running the bash script in scripts/generate_certificates.sh:
   
   ```sh
   # Make the script executable
   chmod +x scripts/generate_certificates.sh
   
   # Run the script
   ./scripts/generate_certificates.sh
   
4. Run the server:

   ```sh
   python project/main.py

5. Run the client (you can optionally modify it):

   ```sh
   python project/client.py

## Setting Up SSL for Your Development Environment

To set up a self-signed SSL certificate for your development environment, follow these steps:

1. Install OpenSSL:

   ```sh
   sudo apt-get update
   sudo apt-get install openssl
   
2. Run the provided bash script to generate the certificate:

   ```sh
   sudo apt-get update
   sudo apt-get install openssl
   
## Running Tests

Tests can simply be run using pytest. This repo includes a performance test for the various algorithms, and it exports log reports of the test in the tests/performance/reports folder. The limits of the software are also tested in the tests/performance/test_server_limitation file (this test might take some time to run; it might be better to just run tests/performance/test_performance for the main server).

To run the tests, use the following command:

```sh
   pytest
```

## Performance Tests

To run the performance tests:

```sh
pytest tests/performance/test_performance.py
```

To run the server limitation tests (may take some time and memory):

```sh
pytest tests/performance/test_server_limitation.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
