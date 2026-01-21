AutoML Pipeline Builder

A full-stack AutoML Pipeline Builder designed to simplify how machine learning models are created and used. The platform allows users to upload datasets, define what they want to predict, and automatically receive a complete machine learning workflow without requiring deep technical knowledge of data science or machine learning.

Behind the scenes, the system automatically handles data preparation, selects an appropriate machine learning model, evaluates its performance, and generates a reusable Python pipeline. This abstraction enables non-technical and semi-technical users to benefit from machine learning while allowing advanced users to further modify and extend the generated pipelines.

This project was developed as part of the Project Software Engineering (PSE) course and emphasizes robust system design, modular architecture, usability, and real-world deployability.

⸻

🚀 Key Features
	•	📂 Upload CSV datasets via a web interface
	•	🎯 Specify a target column for prediction
	•	🤖 Automatic ML task detection (classification / regression)
	•	🧠 Automatic model selection based on evaluation metrics
	•	⚙️ End-to-end pipeline execution (preprocessing + training + evaluation)
	•	📊 View pipeline status and results in the UI
	•	⬇️ Download a fully generated Python ML pipeline (.py)
	•	🌐 Deployed frontend and backend (production-ready)

⸻

🏗️ System Architecture

The system follows a layered architecture:
	1.	Presentation Layer – React-based frontend UI
	2.	Application Layer – FastAPI routing and API layer
	3.	Service Layer – Pipeline logic, model selection, execution
	4.	Artifact Layer – Generated ML pipelines and trained models

Communication between layers happens via RESTful APIs.

⸻

🧑‍💻 Technology Stack

Layer	Technology	Description
Frontend	React (Vite)	Builds a fast, component-based user interface with optimized development and production performance.
Backend	Python 3.13	Core programming language offering strong support for data processing and machine learning.
Backend	Scikit-learn	Machine learning library used for automated model training, selection, and evaluation.
Backend	Pandas	Enables efficient loading, preprocessing, and manipulation of CSV datasets.

⸻

▶️ Running the Project Locally

Backend

cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

Backend runs at:

http://127.0.0.1:8000


⸻

Frontend

cd frontend
npm install
npm run dev

Frontend runs at:

http://localhost:5173


⸻

🌐 Deployment
	•	Frontend: Vercel
	•	Backend: Render

AutoMLPipelineBuilder : https://automlpipelinebuilder.vercel.app/

⸻

👨‍🎓 Academic Context

Developed by Yash Manohar Chaudhari as part of the Project Software Engineering course.

Supervisor: Prof. Holger Klus

⸻
