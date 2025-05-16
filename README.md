Application Settings
You can customize how the application works through simple web browser access:

View Current Settings

Open your browser
Visit: https://your-app-name.fly.dev/config


Change Settings

Using Postman (see previous instructions for setting up Postman)
Set request type to POST
Enter URL: https://your-app-name.fly.dev/config
Go to Body tab, select "raw" and "JSON"
Enter the settings you want to change:
json{
  "base_prompt": "You are a blood glucose optimization assistant. Provide specific recommendations to improve meals and minimize glucose spikes.",
  "top_k_results": 5
}

Click Send



Available Settings

base_prompt: The instructions that guide the AI's responses
top_k_results: Number of information chunks used for each response (1-10)
token_limit: Maximum length of responses (default: 8000)
similarity_threshold: How closely information must match to be included (0.1-1.0)

Note: These settings are optional to change - the application comes with good default settings.# Meal Optimization Assistant: Client Documentation
This document provides instructions for running, maintaining, and using the Meal Optimization Assistant API.
Deployment Instructions
The application is designed to run on your Fly.io infrastructure. This section provides simple steps to deploy the application to your account.
Deploying to Your Fly.io Account (Non-Technical Guide)
I've prepared the application so you can easily deploy it to your Fly.io account with minimal technical knowledge.
Prerequisites:

Your Fly.io account credentials
The Fly.io CLI installed on your computer (if not installed, see note below)

Simplified Deployment Steps:

Login to Fly.io

Open your terminal/command prompt
Type: flyctl auth login
Follow the browser prompts to log in to your Fly.io account


Set Your OpenAI API Key

In the terminal, type:

flyctl secrets set OPENAI_API_KEY=your-api-key-here

Replace your-api-key-here with your actual OpenAI API key


Deploy the Application

Navigate to the folder containing the application
Type: flyctl deploy
This will use the included fly.toml file to set up everything automatically


After Deployment

Once complete, you'll see a URL where your application is available
Example: https://your-app-name.fly.dev



Note About Fly.io CLI:
If you don't have the Fly.io CLI installed, please contact your IT support person to help with the installation, or I can assist with a scheduled support call.
Important: The Application Will Stay Running
The application is configured to stay running at all times, even when not actively used. This ensures it responds immediately when needed without any "wake-up" delay.
If you would like to change this behavior to save resources (and potentially costs), please let me know, and I can guide you through adjusting the configuration.
API Usage
Key Endpoints
EndpointMethodDescription/askPOSTSubmit a meal for analysis/uploadPOSTUpload PDF documents to the knowledge base/filesGETList all uploaded PDF files/delete/{filename}DELETERemove a PDF file/configGET/POSTView or update configuration
/ask Endpoint
The /ask endpoint is the core of the application, providing meal optimization recommendations.
Input
json{
  "query": "I'm having white rice with chicken curry and a glass of orange juice"
}
Output
json{
  "response": "I see you're having white rice with chicken curry and orange juice. Here are some simple optimizations to help manage your blood glucose:\n\n1. Try swapping white rice for brown rice or adding more protein and vegetables to slow digestion\n2. Consider diluting the orange juice with water (1:1) or replacing with whole fruit to reduce sugar impact\n3. Start your meal with the chicken curry before the rice to improve glycemic response\n\nThese small changes can make a significant difference in how your body processes the meal!"
}
Sample API Calls
Once your application is deployed, you can interact with it using the following examples.
Example 1: Ask for meal recommendations
Using your web browser:

Open your browser
Visit: https://your-app-name.fly.dev/ask?query=chicken pasta with garlic bread and soda

Using Postman:

Download and install Postman (free software for testing APIs)
Create a new request
Set request type to POST
Enter URL: https://your-app-name.fly.dev/ask
Go to Body tab, select "raw" and "JSON"
Enter:
json{
  "query": "chicken pasta with garlic bread and soda"
}

Click Send

Example 2: Upload a new PDF to the knowledge base
Using Postman:

Open Postman
Create a new request
Set request type to POST
Enter URL: https://your-app-name.fly.dev/upload
Go to Body tab, select "form-data"
Add key "file" of type "File" and select your PDF from your computer
Click Send

Example 3: View all uploaded PDF files
Using your web browser:

Open your browser
Visit: https://your-app-name.fly.dev/files

Updating the Knowledge Base
The application uses PDF documents as its knowledge base for meal recommendations. These documents should be structured with clear "Section:" markers to allow proper processing.
PDF Format Requirements

The PDF should be structured with sections marked by "Section:" followed by the section title
The first section should contain general rules or principles
Each subsequent section should contain specific information about food categories, strategies, etc.

Example of a properly formatted PDF:
Section: General Rules for Blood Glucose Management
[General content about principles of blood glucose management]

Section: High Glycemic Foods
[Content about high glycemic foods and their impacts]

Section: Optimal Meal Sequencing
[Content about the ideal order to consume different foods]
Steps to Update Knowledge Base

Prepare your PDF following the format requirements above
Upload using the /upload endpoint
Verify the upload was successful by checking the /files endpoint
Test the new knowledge with some sample queries

Removing Documents
If you need to remove a document from the knowledge base:
bashcurl -X DELETE "https://meal-optimization-assistant.fly.dev/delete/document_name"
Note: Use the filename without the .pdf extension.
Application Configuration File (fly.toml)
The application includes a configuration file called fly.toml that controls how it runs on Fly.io. I've already configured it to:

Stay running at all times - The application will not go to sleep due to inactivity
Use appropriate resources - The configuration allocates 1GB of memory
Persist your data - Your uploaded PDFs and their processed data are stored safely

Here's what the key parts of the configuration look like:
[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = false
  auto_start_machines = true
  min_machines_running = 1

[[vm]]
  memory = '1gb'
  cpu_kind = 'shared'
  cpus = 1

[mounts]
  source = "data"
  destination = "/app/data"
Note: You don't need to modify this file unless you want to change these settings. If you do want changes, please contact me for assistance.
Running Locally (Optional)
If you have technical support or would like to run the application on your computer for testing, here are the instructions:
Prerequisites

Docker installed on your computer
Your OpenAI API key

Steps

Download the application files from the provided link
Open a terminal/command prompt in the downloaded folder
Create a text file named .env with your OpenAI API key:
OPENAI_API_KEY=your-api-key-here

Run these commands:
docker build -t meal-optimization-assistant .
docker run -p 8000:8000 --env-file .env meal-optimization-assistant

Access the application at http://localhost:8000

Note: Running locally is completely optional and not required for normal use.
Access Credentials
Once deployed, your application will be available at:
https://your-app-name.fly.dev
You should keep secure:

Your Fly.io account credentials
Your OpenAI API key

For any questions or assistance with deployment, please contact me directly at [your-contact-information].# meal-optimization-assistant