# FastAPI Authentication Setup

This document provides instructions for setting up the FastAPI Authentication project, including environment setup, server configuration, and SSH key generation.

## Table of Contents
- [Setup Environment](#setup-environment)
- [Setup VS Code](#setup-vs-code)
- [Setup Server](#setup-server)
- [Test Coverage](#test-coverage)
- [Create SSH Key for Existing Server](#create-ssh-key-for-existing-server)
- [CI/CD](#ci-cd)

## Setup Environment

To set up the Python environment, follow these steps:

1. Create a virtual environment:
<code>python3.10 -m venv venv</code>

2. Activate the virtual environment:
<code>source venv/bin/activate</code>

3. Install required packages:
<code>pip install -r requirements.txt</code>

## Setup VS Code

To configure Visual Studio Code to use the correct Python interpreter:

1. Open the command palette by pressing CMD + SHIFT + P.
2. Type and select Python: Select Interpreter.
3. Enter the path to the interpreter: ./venv/bin/python3.10

## Setup Server

To set up the server, perform the following steps:

1. Clone the repository:
<code> git clone URL </code>

2. Install docker
Read [there](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)

2. Build the Docker image:
<code>docker build -t fastapi_auth:latest . </code>

3. Run the Docker container:
<code>docker run -p 127.0.0.1:4500:4500 fastapi_auth:latest</code>


## Test Coverage

To check test coverage, follow these steps:

1. Install the coverage package:
<code>pip install pytest-cov</code>

2. Run tests with coverage:
<code>coverage run -m pytest</code>

3. Generate an HTML report and open it:
<code>coverage html & open htmlcov/index.html</code>


## Create SSH Key for Existing Server

To create and set up an SSH key for accessing an existing server:

1. Log in to the server as root using your password.

2. Generate a new SSH key:
   
<code>ssh-keygen -t rsa -b 4096 -C "your_email@example.com"</code>

3. Read and copy the public key:
<code>
 cat ~/.ssh/id_rsa.pub

 echo "yourpublickey" >> ~/.ssh/authorized_keys
</code>

4. Ensure that the authorized_keys file has the correct permissions:
<code>chmod 600 ~/.ssh/authorized_keys</code>

5. Save the files ~/.ssh/id_rsa.pub and ~/.ssh/id_rsa to your local machine using an SFTP client like Termius.

6. To connect via SSH using your private key, run:
<code>ssh -i /path/to/your/private/key/id_rsa username@hostname</code>


## CI/CD
git push --force origin deploy
git checkout deploy
git pull origin main
git push origin deploy
git checkout main


git checkout deploy && git pull origin main && git push origin deploy && git checkout main