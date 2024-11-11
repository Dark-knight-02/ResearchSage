# ResearchSage

ResearchSage is a cutting-edge tool designed to enhance text processing and analysis capabilities by leveraging advanced machine learning models and frameworks.


<img width="1470" alt="Screenshot 2024-11-11 at 6 59 40 AM" src="https://github.com/user-attachments/assets/6063360d-d759-4c61-826e-9bddf2bb24a0">


<img width="1469" alt="Screenshot 2024-11-11 at 6 51 08 AM" src="https://github.com/user-attachments/assets/4639c183-d18f-450a-8b16-e43a18e7d5fa">



## Table of Contents

- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Setup](#setup)
- [Running the Application](#running-the-application)
  - [Prerequisites](#prerequisites)
  - [Steps to Run](#steps-to-run)
  - [Accessing the Application](#accessing-the-application)
- [Troubleshooting](#troubleshooting)

## Technologies Used

ResearchSage utilizes the following technologies:
- **Python 3.9.6**: For writing and executing the core application.
- **Streamlit**: To create a user-friendly web interface.
- **OpenAI**: For accessing powerful AI models.
- **Pinecone**: For efficient vector indexing and similarity search.
- **Sentence Transformers**: For generating textual embeddings.

Additional libraries and frameworks are listed in the `requirements.txt` file.

## Installation

To get started with ResearchSage, you'll need to install its dependencies.

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/ResearchSage.git
   cd ResearchSage
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
## Setup
Before running the application, ensure you have the necessary API keys and configurations set:

1. **API Keys**:

- Obtain API keys for OpenAI and Pinecone.
- Set these keys in your environment variables or a configuration file.

2. **Configuration File**:

- Create a config.json file in the root directory and fill it with your API keys and other necessary configurations.


## Running the Application

Running ResearchSage locally involves a few simple steps once you have completed the installation and setup. Here’s how you can get it up and running:

### Prerequisites

Before launching the application, make sure you have the following prerequisites installed and properly configured:

- **Python 3.9.6**: Ensure that Python is installed and working in your development environment.
- **API Keys**: Ensure that you have obtained the necessary API keys and added them to your environment variables or a designated configuration file as outlined in the [Setup](#setup) section.

### Steps to Run

1. **Open Terminal**
   - Open your terminal or command prompt.

2. **Navigate to the Project Directory**
   - Change into the directory where you have cloned the ResearchSage repository.
     ```bash
     cd path/to/ResearchSage
     ```

3. **Activate Python Environment** (Optional)
   - If you are using a virtual environment, activate it:
     ```bash
     source your_env/bin/activate  # On macOS and Linux
     .\your_env\Scripts\activate   # On Windows
     ```

4. **Start the Research Paper Fetcher Application**
   - Run the application using Streamlit:
     ```bash
     streamlit run updated_app.py
     ```
5. **Start the Chatbot Application**
   - Run the application using Streamlit:
     ```bash
     streamlit run app.py
     ```

### Accessing the Application

- **Web Interface**
  - After starting the application, Streamlit will provide you with a local URL in the terminal, typically:
    ```
    Local URL: http://localhost:8501
    Network URL: http://192.168.x.x:8501
    ```
  - Open a web browser of your choice and visit `http://localhost:8501` to interact with ResearchSage.

## Troubleshooting

If you encounter any issues while starting the application, consider the following:

- **Dependencies**: Ensure all dependencies are installed correctly as mentioned in the [Installation](#installation) section.
- **API Keys**: Verify that all required API keys are correctly set in the environment or configuration files.
- **Port Availability**: Streamlit runs on port 8501 by default. Ensure that the port is available and not being used by another application.
- **Logs and Errors**: Pay attention to the console output. Errors or warnings there can provide additional information on what might be going wrong.

Enjoy using ResearchSage to enhance your text processing and analysis projects!




   
   
