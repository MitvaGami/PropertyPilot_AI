# Real Estate AI Assistant: Automated Lead Qualification & Property Inquiry System

## 🌟 Project Overview

This project introduces a foundational AI-powered conversational agent designed to significantly enhance the operational efficiency of a small to medium-sized real estate firm, particularly within the dynamic Indian market. Moving beyond the scope of a full CRM, this solution targets a critical business pain point: automating the initial stages of lead qualification and providing instant, accurate responses to common property inquiries.

By serving as the primary digital touchpoint, this AI assistant empowers human agents to reallocate their valuable time from repetitive tasks to high-value interactions and core sales activities, ultimately driving productivity and improving customer response times.

**Key Capabilities:**

*   **Intelligent Property Inquiry Handling:** Answers questions about properties by ID, location, BHK, price range, or amenities.
*   **Automated Lead Qualification:** Engages users in a structured dialogue to gather essential requirements (preferred location, desired BHK, budget), pre-qualifying leads for sales teams.
*   **24/7 Availability:** Provides immediate responses around the clock, improving client experience and reducing lead response time.
*   **Seamless Human Handoff:** Collects contact details and facilitates a warm handover for complex queries requiring human intervention.

This project demonstrates a practical application of AI, built entirely using robust, open-source technologies to showcase a highly relevant and impressive technical skillset.

## 🚀 Key Features

*   **Conversational Interface:** Engages users naturally to understand their needs.
*   **Dynamic Data Retrieval:** Queries an SQLite database in real-time to provide up-to-date property information based on user-specified criteria.
*   **Contextual Understanding:** Utilizes Natural Language Understanding (NLU) to interpret user intents (`ask_property_details`, `inform_location_bhk_budget`) and extract critical entities (`location`, `bhk`, `price`, `property_id`).
*   **Guided Information Collection (Forms):** Implements Rasa Forms for structured multi-turn conversations to efficiently gather required lead details.
*   **Flexible Search Parameters:** Supports searching by various criteria including property ID, location, number of bedrooms (BHK), budget, and specific amenities.
*   **Basic Price Normalization:** Logic to interpret common Indian real estate budget formats (e.g., "1.5 crore", "90 lakhs").
*   **Out-of-Scope Management:** Gracefully redirects queries outside its domain, maintaining a professional and helpful persona.

## 📊 Data Flow & Architecture

The AI assistant operates on a modular architecture, ensuring clear separation of concerns and efficient processing of user interactions:

1.  **User Interaction (Flask UI / Rasa Shell):**
    *   The user initiates a conversation through the Flask web interface or directly via the Rasa command-line shell.
    *   User messages are captured and sent to the Rasa Core/NLU server.

2.  **Rasa NLU (Natural Language Understanding):**
    *   The core of understanding. Rasa NLU takes the raw user message and transforms it into structured data:
        *   **Intent Prediction:** Determines the user's goal (e.g., `ask_property_details`).
        *   **Entity Extraction:** Identifies and extracts key pieces of information (e.g., `property_id: "P001"`, `location: "Koramangala"`).
    *   This structured information is added to the `Tracker`, which maintains the conversation's state.

3.  **Rasa Core (Dialogue Management):**
    *   The "brain" of the assistant. Based on the current `Tracker` state (history of intents, entities, and filled slots) and its trained dialogue policies (`MemoizationPolicy`, `RulePolicy`, `TEDPolicy`, `UnexpecTEDIntentPolicy`), Rasa Core decides the most appropriate next action.
    *   This action could be:
        *   **Uttering a predefined response** (e.g., `utter_greet`).
        *   **Activating a Form** (e.g., `property_form`) to collect multiple pieces of information sequentially.
        *   **Triggering a Custom Action** for complex logic or external integrations.

4.  **Rasa Action Server:**
    *   When a `custom action` is chosen by Rasa Core (e.g., `action_search_properties`, `validate_property_form`), Rasa Core sends an HTTP request to the Action Server (running independently on `http://localhost:5055`).
    *   The Action Server executes the corresponding Python code (`actions/actions.py`). This is where the core business logic resides:
        *   **Database Querying:** Connects to the SQLite database (`db/properties.db`).
        *   **Data Processing:** Filters, processes, and formats retrieved property data.
        *   **Validation:** Custom logic to validate user inputs (e.g., ensuring BHK is a valid number, parsing prices).
        *   **Response Formulation:** Constructs the specific text response to send back to the user.

5.  **SQLite Database (`db/properties.db`):**
    *   A lightweight, file-based database storing all property listings, including details like `property_id`, `location`, `bhk`, `price_lacs`, `amenities`, `status`, and `contact_info`.
    *   The Action Server interacts with this database to fetch relevant property data.

6.  **Response Delivery:**
    *   The Action Server sends its formulated response back to Rasa Core.
    *   Rasa Core then relays this response to the client (Flask UI or Rasa Shell), which displays it to the user.
    *   The process then loops, awaiting the user's next input.

## 🛠️ Tech Stack & Professional Relevance

This project demonstrates proficiency across a diverse and highly in-demand set of technologies:

*   **Python:**
    *   **Relevance:** The industry standard for AI, Machine Learning, and Data Science. Its versatility and extensive ecosystem (NumPy, Pandas, etc.) make it ideal for developing intelligent systems. Highlights core programming, scripting, and backend development skills.
*   **Rasa Open Source (NLU & Core):**
    *   **Relevance:** A leading open-source framework for building scalable, contextual AI assistants. Experience with Rasa is direct evidence of practical skills in Conversational AI, Natural Language Processing (NLP), dialogue management, custom action development, and an understanding of advanced chatbot architectures. It's a significant asset for roles in AI Engineering, NLP, or Product Development.
*   **SQLite:**
    *   **Relevance:** A lightweight, self-contained, serverless relational database. Demonstrates fundamental database management skills, including SQL querying, data modeling, and local data persistence – essential for almost any software application. Its simplicity makes it perfect for rapid prototyping and deployment.
*   **Pandas:**
    *   **Relevance:** The go-to library for data manipulation and analysis in Python. Used for efficient data loading and processing from CSV to SQLite. Showcases skills in data wrangling, a crucial step in preparing data for AI models.
*   **Flask:**
    *   **Relevance:** A minimalist yet powerful Python micro-web framework. Employed to create a simple, interactive web-based chat interface. This demonstrates basic full-stack development capabilities, API integration, and front-end interaction, highlighting the ability to deliver a user-facing application.
*   **Git & GitHub:**
    *   **Relevance:** Indispensable tools for modern software development. Their usage demonstrates adherence to professional version control best practices, collaborative development readiness, and effective project documentation and sharing.

## 📈 Performance & Limitations

This project provides a robust proof-of-concept. Its "accuracy" is a function of:
*   **NLU Model Performance:** How well `nlu.yml` (intent recognition and entity extraction) generalizes to unseen user utterances. Performance is optimized through the `DIETClassifier` and careful training data design.
*   **Dialogue Management:** The effectiveness of `stories.yml` and `rules.yml` in guiding the conversation.
*   **Data Quality:** The comprehensiveness and consistency of the `properties.csv` and `properties.db` data.

**Current Limitations:**
*   **Limited Data Volume:** The project uses hypothetical, small datasets. Real-world performance scales with larger, more diverse training data and property listings.
*   **Basic Price & BHK Parsing:** While some heuristics are implemented, highly nuanced or ambiguous numerical inputs might require more advanced NLP techniques or dedicated libraries.
*   **No External API Integration:** Currently, all data is local. A production system would integrate with live property listing APIs or CRMs.
*   **Simple UI:** The Flask UI is functional but deliberately minimalist, focusing on core chatbot logic.

## 🚀 How to Run the Project

Follow these steps to set up and launch the Real Estate AI Assistant locally.

### Prerequisites

*   **Python 3.8+:** Ensure it's installed and added to your system's PATH.
*   **VS Code:** Your preferred IDE for this project.
*   **VS Code Extensions:** Install "Python", "YAML", and "GitLens" from the VS Code Extensions Marketplace.

### Setup Instructions

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/your_github_username/real_estate_ai_agent.git # Replace with your repo URL
    cd real_estate_ai_agent
    ```

2.  **Create & Activate Virtual Environment:**
    ```bash
    python -m venv venv
    ```
    *   **Windows:** `.\venv\Scripts\activate`
    *   **macOS/Linux:** `source venv/bin/activate`

3.  **Install Project Dependencies:**
    ```bash
    pip install rasa "rasa[full]" "SQLAlchemy==1.4.46" pandas Flask
    ```

4.  **Initialize Rasa Project Structure:**
    ```bash
    rasa init --no-prompt
    ```
    *   *Note: This creates default Rasa files which will be overwritten by our custom project files.*

5.  **Prepare Database (`properties.db`):**
    *   Ensure the `db` folder exists in your project root.
    *   Create `db/properties.csv` and populate it with your property data (as provided in project instructions).
    *   Create `db/create_db.py` and paste the Python script for database creation (as provided in project instructions).
    *   Run the script:
        ```bash
        cd db
        python create_db.py
        cd .. # Return to project root
        ```
    *   Verify `db/properties.db` has been created.

6.  **Configure Rasa Files:**
    *   **Crucially, replace the content of the following files with the custom project code provided in the project instructions:**
        *   `data/nlu.yml`
        *   `data/stories.yml`
        *   `data/rules.yml`
        *   `domain.yml`
        *   `config.yml`
        *   `endpoints.yml`
        *   `actions/actions.py`

7.  **Train the Rasa Model:**
    *   From the project root directory in your active virtual environment terminal:
        ```bash
        rasa train
        ```
    *   This process compiles your NLU, dialogue, and response data into a single model.

### Launching the AI Assistant (Simultaneous Server Execution)

To run the complete system, you need **three separate terminal instances** concurrently. Each terminal must have the virtual environment activated.

1.  **Terminal 1: Start Rasa Action Server**
    ```bash
    rasa run actions
    ```
    *   This server executes your custom Python logic defined in `actions/actions.py`.
    *   Expected output: "Action endpoint is up and running on `http://0.0.0.0:5055`"

2.  **Terminal 2: Start Rasa Core/NLU Server (API Mode)**
    ```bash
    rasa run --enable-api --cors "*"
    ```
    *   This server handles the core AI logic (NLU & Dialogue Management) and exposes a REST API for clients (like your Flask UI).
    *   `--enable-api` exposes the API. `--cors "*"` allows your Flask app (on a different port) to communicate.
    *   Expected output: "The Rasa server is listening on `http://0.0.0.0:5005`"

3.  **Terminal 3: Start Flask Web UI**
    *   Navigate to the Flask application directory:
        ```bash
        cd flask_ui
        ```
    *   Ensure `flask_ui/templates` folder exists and `flask_ui/app.py` and `flask_ui/templates/index.html` contain the provided code.
    *   Launch the Flask web server:
        ```bash
        python app.py
        ```
    *   Expected output: "* Running on `http://127.0.0.1:5000`"

### Interact with Your AI Assistant!

Once all three terminals are running without errors, open your web browser and navigate to:

**`http://127.0.0.1:5000`**

You will now see the chat interface ready for interaction!

## 🧪 Testing the Agent

Feel free to experiment with a variety of queries:

*   **Greetings:** `Hi`, `Hello`, `Good morning`
*   **Direct Property Search:** `Tell me about P003`, `Details for P005`
*   **Filtered Search:** `I'm looking for a 2BHK in Indiranagar`, `My budget is around 1.5 crore`, `Any properties with a pool?`
*   **Guided Search (Form):** `I want to find a property` (the bot should then ask for details sequentially)
*   **Contact Handoff:** `How can I talk to someone?`, `I want to connect to an agent`
*   **Out of Scope:** `Tell me a joke`, `What's the weather like?`

## 🚀 Future Enhancements

This project lays a robust groundwork. Potential avenues for further development include:

*   **Advanced Data Parsing:** Integrate more sophisticated NLP for highly nuanced numerical and location entities (e.g., "between X and Y", "apartments near X park").
*   **Rich UI Components:** Incorporate interactive elements like quick reply buttons, carousels for property listings, and embedded images within the chat interface.
*   **Lead Management Integration:** Develop API integration with mock CRM systems or simple lead export functionality (e.g., to CSV).
*   **External Service Integration:** Integrate with real-time property APIs, mapping services (e.g., Google Maps), or scheduling tools.
*   **User Authentication:** Implement basic user login for personalized experiences.
*   **Deployment:** Containerize the application using Docker and deploy to cloud platforms (AWS, GCP, Azure, Heroku) for public access.
*   **Monitoring & Analytics:** Integrate tools to track bot performance, user engagement, and conversation trends.

## 📄 License

This project is open-source and available under the MIT License.

## 📧 Contact

For any inquiries, feedback, or collaborations, please feel free to reach out:

[Your Name]
[Your Email Address]
[Your LinkedIn Profile URL (Optional)]

---