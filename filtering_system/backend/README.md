# AI-Powered Activity Suggestion System

## Project Overview
This project is a web application that utilizes AI and Natural Language Processing (NLP) to analyze user-submitted activity suggestions. The backend includes a pipeline that processes data using advanced AI techniques to ensure only the most unique and useful ideas are accepted.

## Features
Our solution uses AI-powered language models to compare new activity suggestions with existing ones through a six-step pipeline:

1. **Preprocessing** – Removes exact duplicates to maintain data cleanliness.
2. **Bad Word Filtering** – Ensures content is respectful by filtering inappropriate words.
3. **Removing Similar Suggestions** – Eliminates duplicate activity suggestions.
4. **Checking Against Existing Activities** – Rejects suggestions too similar to existing ones.
5. **Business Activity Filtering** – Removes commercial suggestions based on a business list in Algeria.
6. **Artisanal Activity Filtering** – Filters out traditional craftsmanship listings.

At the end, the system ranks suggestions using a custom algorithm, prioritizing the most unique and diverse ideas. Users have the final say and can accept or reject AI recommendations.

## How to Run the Project
### 1. Clone the repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Running the Frontend
```bash
cd front-end
npm install
npm start
```

### 3. Running the Backend
```bash
python app2.py
```

## Project Requirements
### Frontend Dependencies (from package.json)
- React
- React-DOM
- React-Scripts

### Backend Dependencies (from app2.py)
- streamlit
- pandas

### Installing Backend Dependencies
Create a `requirements.txt` file and add:
```bash
streamlit
pandas
```
Then install dependencies with:
```bash
pip install -r requirements.txt
```

## Additional Notes
- Ensure you have **Node.js** and **npm** installed for the frontend.
- Ensure you have **Python 3** installed along with **pip** for the backend.
- The system is designed to handle NLP-based filtering and ranking of activities efficiently.

## License
This project is open-source and available for use under the [MIT License](LICENSE).

## Contact
For any inquiries or contributions, feel free to reach out to the project maintainers.

