"""
Seed Batch 3 — Data Science + AI/ML
Run from techpath-backend/:
    PYTHONIOENCODING=utf-8 venv/Scripts/python.exe scripts/seed_courses_batch3.py
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.db.session import AsyncSessionLocal
from app.crud.course import course_crud, course_category_crud, skill_crud
from app.schemas.course import (
    CourseCreate,
    CurriculumModule,
    FAQItem,
    ProjectItem,
    CourseCategoryCreate,
)

# ---------------------------------------------------------------------------
# Skills
# ---------------------------------------------------------------------------

ALL_SKILLS = [
    # Data Science / ML
    ("Pandas", "pandas"),
    ("NumPy", "numpy"),
    ("Matplotlib", "matplotlib"),
    ("Seaborn", "seaborn"),
    ("Scikit-learn", "scikit-learn"),
    ("Machine Learning", "machine-learning"),
    ("Data Science", "data-science"),
    ("Statistics", "statistics"),
    ("Deep Learning", "deep-learning"),
    ("TensorFlow", "tensorflow"),
    ("AI", "ai"),
    ("Data Analysis", "data-analysis"),
    ("EDA", "eda"),
    ("Streamlit", "streamlit"),
    ("Jupyter", "jupyter"),
    ("Kaggle", "kaggle"),
    # Shared (get_or_create skips duplicates)
    ("Python", "python"),
    ("Git", "git"),
    ("GitHub", "github"),
]

# ---------------------------------------------------------------------------
# Course description
# ---------------------------------------------------------------------------

DS_DESCRIPTION = """\
**Data Science + AI/ML** — the course that turns raw data into decisions, predictions, and careers. \
In 6 months, you go from "what is a dataset?" to building machine learning models that predict real \
outcomes — house prices, customer churn, exam results, loan approvals — all with Python.

Available both **offline at our Mughalsarai centre** and **live online** — same instructor, same curriculum, same projects.

---

### Why Data Science in 2026?

Every company in India — from Flipkart to a Varanasi textile exporter — is sitting on data they do \
not know how to use. The person who can clean that data, find patterns, and build predictions from it \
is the most valuable person in the room.

India needs 250,000+ data professionals by 2027 (NASSCOM). The supply is nowhere close. Especially \
from tier-2 and tier-3 cities — almost zero. That gap is your career opportunity.

---

### What does Data Science actually look like?

It is not complicated math on a blackboard. It is Python code that talks to data. Here is a taste:

**Loading and exploring a dataset:**
```python
import pandas as pd

df = pd.read_csv("students.csv")
print(df.shape)          # (500, 8) — 500 students, 8 columns
print(df.head())         # First 5 rows
print(df.describe())     # Mean, median, min, max of every column
print(df.isnull().sum()) # Count of missing values per column
```
In 4 lines, you loaded 500 student records, checked the structure, got a statistical summary, \
and found missing values. This is what data scientists do before breakfast.

**Visualising data — one line of code:**
```python
import matplotlib.pyplot as plt

df["marks"].hist(bins=20, color="teal", edgecolor="white")
plt.title("Distribution of Student Marks")
plt.xlabel("Marks")
plt.ylabel("Number of Students")
plt.show()
```

**Building a Machine Learning model:**
```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

X = df[["study_hours", "attendance", "previous_score"]]
y = df["final_marks"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = LinearRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test)
print(f"Model Accuracy (R2): {r2_score(y_test, predictions):.2f}")
# Output: Model Accuracy (R2): 0.87
```

---

### The 6-month journey

**Phase 1 - Python for Data Science (Month 1)**
Python fundamentals with a data focus. Variables, loops, functions, file handling — everything you \
need before touching data libraries.

**Phase 2 - Statistics & Probability (Month 2)**
The math behind the magic — but taught with data, not textbooks. Mean, median, standard deviation, \
probability, distributions, hypothesis testing, correlation. You will calculate everything in Python.

**Phase 3 - Data Analysis & Visualisation (Month 3)**
Pandas, NumPy, Matplotlib, Seaborn — the four pillars. Load datasets, clean messy data, handle \
missing values, group and aggregate, and create publication-quality charts.

**Phase 4 - Machine Learning (Months 4-5)**
The core. Linear regression, logistic regression, decision trees, random forests, KNN, SVM, \
clustering, model evaluation, cross-validation, hyperparameter tuning. Every algorithm taught \
with real datasets and real code.

**Phase 5 - Deep Learning Basics & Capstone (Month 6)**
Introduction to neural networks, TensorFlow/Keras basics, image classification concept, NLP basics. \
Then: your capstone project — a complete data science solution from raw data to deployed model.

---

### What you will build

- A complete Exploratory Data Analysis (EDA) on a real-world dataset
- Interactive visualisation dashboards with Matplotlib and Seaborn
- A house price prediction model (regression)
- A customer churn classifier (classification)
- A movie recommendation system (collaborative filtering basics)
- A sentiment analyser for product reviews (NLP basics)
- A capstone project: end-to-end ML pipeline on a dataset of your choice

Every project goes on your **GitHub** — your portfolio that recruiters actually check.

---

### Offline + Online — your choice

**Offline (Mughalsarai centre):**
Circus Road, Mughalsarai — walking distance from DDU Junction. Small batches of 25 students. \
Morning, afternoon, and evening batches. Lab access during class hours.

**Live Online:**
Same instructor, same curriculum, same batch timings. Join from Chandauli, Varanasi, Ghazipur, \
Ballia, Bihar, or any city in India. Live interactive classes with screen sharing, live coding, \
and real-time doubt clearing. Not pre-recorded videos.

Both modes include: WhatsApp doubt support, weekend doubt sessions, project reviews, and placement assistance.

---

### Career outcomes

- Data Analyst (Rs 20,000-45,000/month starting)
- Junior Data Scientist (Rs 30,000-60,000/month)
- Machine Learning Engineer (with further practice)
- Business Intelligence Analyst
- Python Data Engineer
- Research Assistant (for M.Tech / PhD applicants)
- Freelance Data Analyst (Rs 5,000-30,000 per project)
- AI/ML roles in startups, banks, e-commerce, healthcare, and edtech

---

### Who is this for?

- Class 12 pass students (Science or Commerce — both welcome)
- BCA, BSc, B.Tech, MCA students who want practical ML skills
- Graduates who enjoy numbers, patterns, and problem-solving
- Working professionals in banking, insurance, or retail who want to move into analytics
- Students from Mughalsarai, Chandauli, Varanasi, Ghazipur, Mirzapur, Ballia, and Bihar border areas
- Remote learners from any city in India joining our live online batch
- Anyone who has completed our Python course and wants the next step

**You do not need an engineering degree. You do not need advanced math. You need curiosity, \
Python basics (we cover them in Month 1), and willingness to practice.**\
"""

# ---------------------------------------------------------------------------
# Courses list
# ---------------------------------------------------------------------------

COURSES = [
    dict(
        category_slug="data-science",
        skill_slugs=[
            "python", "pandas", "numpy", "matplotlib", "seaborn",
            "scikit-learn", "machine-learning", "data-science", "statistics",
            "deep-learning", "tensorflow", "ai", "data-analysis", "eda",
        ],
        data=CourseCreate(
            title="Data Science + AI/ML",
            slug="data-science-ai-ml",
            level="beginner",
            short_description=(
                "Master Data Science, Machine Learning, and AI in 6 months. Learn Python, "
                "Statistics, Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn, and basics of "
                "Deep Learning. Real datasets, real projects, real career outcomes. "
                "Offline in Mughalsarai + live online batches available."
            ),
            description=DS_DESCRIPTION,
            price=20000,
            original_price=30000,
            currency="INR",
            emi_available=True,
            emi_amount=3500,
            duration="6 months",
            duration_hours=144,
            batch_size=25,
            rating=5.0,
            review_count=12,
            enrollment_count=18,
            placement_rate=78,
            instructor_name="TechPath Instructor",
            instructor_title="Senior Data Scientist & ML Trainer",
            instructor_bio=(
                "Experienced in building machine learning models, data pipelines, and analytical "
                "dashboards for real-world business problems. Has trained 150+ students across "
                "Mughalsarai, Chandauli, and Varanasi — both offline and online — in Python, "
                "statistics, and machine learning with a project-first teaching approach."
            ),
            status="published",
            featured=True,
            is_active=True,
            certification_name="Data Science + AI/ML Certificate",
            certification_authority="TechPath",
            meta_title="Data Science + AI/ML Course - 6 Months Offline & Online | TechPath",
            meta_description=(
                "Learn Data Science and Machine Learning in 6 months at TechPath Mughalsarai or "
                "live online. Python, Pandas, Scikit-learn, real projects. EMI available. Enrol now."
            ),
            learning_outcomes=[
                "Write Python code confidently for data loading, cleaning, and transformation",
                "Understand and apply core statistics — mean, median, standard deviation, probability, distributions, hypothesis testing",
                "Load, explore, clean, and manipulate datasets using Pandas and NumPy",
                "Create professional charts and visualisations using Matplotlib and Seaborn",
                "Perform complete Exploratory Data Analysis (EDA) on any real-world dataset",
                "Build and evaluate regression models (Linear Regression, Polynomial Regression)",
                "Build and evaluate classification models (Logistic Regression, Decision Trees, Random Forest, KNN, SVM)",
                "Apply unsupervised learning techniques — K-Means clustering, PCA",
                "Handle real-world data problems — missing values, outliers, feature engineering, encoding categorical variables",
                "Evaluate models using accuracy, precision, recall, F1-score, confusion matrix, and cross-validation",
                "Understand the basics of neural networks and deep learning using TensorFlow/Keras",
                "Build an end-to-end ML pipeline from raw data to trained model with documentation",
                "Present data insights and model results clearly to non-technical audiences",
            ],
            prerequisites=[
                "Basic computer use (browser, file management, typing)",
                "No prior programming experience required (Python is taught from scratch in Month 1)",
                "Class 12 pass — Science or Commerce stream recommended but not mandatory",
                "Basic comfort with numbers (you do not need advanced math — we teach the required statistics)",
                "Laptop with at least 8 GB RAM (required for running Jupyter notebooks and ML libraries)",
                "For online batch: stable internet connection and a quiet study space",
            ],
            curriculum=[
                CurriculumModule(
                    title="Python for Data Science",
                    duration="3 weeks",
                    topics=[
                        "Python setup", "VS Code", "Jupyter Notebook", "Variables", "Data types",
                        "Strings", "Lists", "Tuples", "Dictionaries", "Sets", "Loops", "Functions",
                        "File handling", "CSV and JSON", "pip install", "Virtual environments",
                        "List comprehension",
                    ],
                ),
                CurriculumModule(
                    title="NumPy — Numerical Computing",
                    duration="2 weeks",
                    topics=[
                        "What is NumPy", "ndarray", "Creating arrays", "Shape and reshape",
                        "Indexing and slicing", "Broadcasting", "Mathematical operations",
                        "Statistical functions (mean median std)", "Random module",
                        "Array performance vs lists", "Matrix operations basics",
                    ],
                ),
                CurriculumModule(
                    title="Pandas — Data Manipulation",
                    duration="3 weeks",
                    topics=[
                        "Series and DataFrame", "read_csv read_excel", "head() tail() info() describe()",
                        "Selecting columns rows", "Filtering (boolean indexing)", "Sorting",
                        "Groupby and aggregation", "Merge join concat", "Pivot tables",
                        "Handling missing values (fillna dropna)", "Data type conversion",
                        "apply() and lambda", "String operations in Pandas", "Date and time handling",
                    ],
                ),
                CurriculumModule(
                    title="Statistics & Probability",
                    duration="3 weeks",
                    topics=[
                        "Mean Median Mode", "Variance and Standard Deviation", "Percentiles and Quartiles",
                        "Normal distribution", "Skewness and Kurtosis", "Probability basics",
                        "Bayes theorem (intuition)", "Correlation (Pearson Spearman)",
                        "Hypothesis testing (t-test chi-square)", "p-value and significance",
                        "Central Limit Theorem", "All calculations done in Python",
                    ],
                ),
                CurriculumModule(
                    title="Data Visualisation — Matplotlib & Seaborn",
                    duration="2 weeks",
                    topics=[
                        "Matplotlib basics (line bar scatter hist)", "Subplots and figure size",
                        "Labels titles legends",
                        "Seaborn (countplot barplot boxplot heatmap violinplot pairplot)",
                        "Customising colour palettes", "Visualisation best practices",
                        "Telling a story with charts", "EDA visualisation workflow",
                    ],
                ),
                CurriculumModule(
                    title="Exploratory Data Analysis (EDA) Project",
                    duration="2 weeks",
                    topics=[
                        "Choosing a real dataset (Kaggle)", "Data loading and inspection",
                        "Cleaning and preprocessing", "Univariate and bivariate analysis",
                        "Correlation heatmap", "Outlier detection (IQR Z-score)",
                        "Feature insights and summary", "EDA report writing", "Presenting findings",
                    ],
                ),
                CurriculumModule(
                    title="Machine Learning — Regression",
                    duration="3 weeks",
                    topics=[
                        "What is Machine Learning", "Supervised vs Unsupervised", "Train test split",
                        "Linear Regression (theory + code)", "Multiple Linear Regression",
                        "Polynomial Regression", "Evaluation metrics (MAE MSE RMSE R2)",
                        "Feature scaling (StandardScaler MinMaxScaler)",
                        "Handling categorical variables (LabelEncoder OneHotEncoder)",
                        "Overfitting and underfitting", "Project: House Price Prediction",
                    ],
                ),
                CurriculumModule(
                    title="Machine Learning — Classification",
                    duration="3 weeks",
                    topics=[
                        "Logistic Regression", "Decision Tree Classifier", "Random Forest Classifier",
                        "K-Nearest Neighbours (KNN)", "Support Vector Machine (SVM)",
                        "Evaluation metrics (accuracy precision recall F1 confusion matrix ROC-AUC)",
                        "Cross-validation", "Hyperparameter tuning (GridSearchCV)",
                        "Project: Customer Churn Prediction", "Project: Loan Approval Classifier",
                    ],
                ),
                CurriculumModule(
                    title="Unsupervised Learning & Feature Engineering",
                    duration="2 weeks",
                    topics=[
                        "K-Means Clustering", "Elbow method", "Silhouette score",
                        "PCA (Principal Component Analysis)", "Dimensionality reduction",
                        "Feature engineering techniques",
                        "Feature selection (correlation variance importance)",
                        "Handling imbalanced datasets (SMOTE overview)",
                        "Pipeline concept in Scikit-learn",
                    ],
                ),
                CurriculumModule(
                    title="Deep Learning Basics",
                    duration="2 weeks",
                    topics=[
                        "What are Neural Networks", "Perceptron concept",
                        "Activation functions (ReLU Sigmoid Softmax)", "TensorFlow and Keras setup",
                        "Building a simple neural network", "Training and evaluation",
                        "Image classification (MNIST handwritten digits)",
                        "NLP basics (text preprocessing tokenisation)",
                        "Sentiment analysis with simple model", "GPU vs CPU (awareness)",
                        "What to learn next in deep learning",
                    ],
                ),
                CurriculumModule(
                    title="Git, Deployment & Tools",
                    duration="1 week",
                    topics=[
                        "Git and GitHub for data projects", "Jupyter Notebook best practices",
                        "Saving and loading models (pickle joblib)",
                        "Streamlit basics (build a simple ML web app)",
                        "Deploying a Streamlit app (Streamlit Cloud)",
                        "Kaggle account and competitions overview",
                        "Google Colab for heavy computation",
                    ],
                ),
                CurriculumModule(
                    title="Capstone Project & Career Preparation",
                    duration="3 weeks",
                    topics=[
                        "Capstone project (end-to-end ML pipeline)", "Dataset selection",
                        "EDA and preprocessing", "Model building and comparison",
                        "Model evaluation and selection", "Documentation and README",
                        "GitHub upload", "Streamlit demo app",
                        "Resume building for data roles", "LinkedIn optimisation",
                        "Portfolio presentation", "Mock interviews (technical + HR)",
                        "Freelance data analysis guide",
                        "Career roadmap (analyst to scientist to engineer)",
                    ],
                ),
            ],
            faqs=[
                FAQItem(
                    question="Do I need to know programming before joining this course?",
                    answer=(
                        "No. Month 1 is entirely dedicated to Python programming — starting from zero. "
                        "By the time we reach data libraries in Month 2, you will be comfortable writing "
                        "Python code. If you have already completed our Python course, you will move "
                        "through Month 1 even faster."
                    ),
                ),
                FAQItem(
                    question="Do I need to be good at math?",
                    answer=(
                        "You need basic comfort with numbers — addition, multiplication, percentages. "
                        "We teach all the statistics and probability required for data science from "
                        "scratch inside the course (Module 4). Every formula is implemented in Python "
                        "code, not solved on paper. You do not need calculus or linear algebra."
                    ),
                ),
                FAQItem(
                    question="Is this course available online?",
                    answer=(
                        "Yes. We offer both offline classes at our Mughalsarai centre (Circus Road, "
                        "near DDU Junction) and live online classes with the same instructor and "
                        "curriculum. Online students join via Google Meet or Zoom with live screen "
                        "sharing, real-time coding, and doubt clearing. Both modes include WhatsApp "
                        "support, weekend doubt sessions, and placement assistance."
                    ),
                ),
                FAQItem(
                    question="What is the difference between Data Science and AI/ML?",
                    answer=(
                        "Data Science is the broader field — it includes collecting data, cleaning it, "
                        "analysing it, and communicating insights. Machine Learning (ML) is a part of "
                        "data science where you build models that learn from data and make predictions. "
                        "Artificial Intelligence (AI) is the broader goal that ML serves. This course "
                        "covers all three: you start with data analysis, progress to ML models, and get "
                        "an introduction to deep learning."
                    ),
                ),
                FAQItem(
                    question="What is the fee? Is EMI available?",
                    answer=(
                        "The course fee is Rs 20,000 (discounted from Rs 30,000). EMI is available at "
                        "Rs 3,500 per month for 6 months (approx). The fee is the same for both offline "
                        "and online batches. A free demo class is available — contact us at "
                        "+91 8299708052 to book."
                    ),
                ),
                FAQItem(
                    question="What kind of laptop do I need?",
                    answer=(
                        "A laptop with at least 8 GB RAM is required. 16 GB is recommended for the "
                        "deep learning module. Any operating system works — Windows, macOS, or Linux. "
                        "We also teach you to use Google Colab for heavy computation, so even if your "
                        "laptop is not powerful, you can run ML models on Google's free cloud GPUs."
                    ),
                ),
                FAQItem(
                    question="Can I get a job in Data Science from Mughalsarai?",
                    answer=(
                        "Yes. Most data science and analytics roles in India are remote-friendly. "
                        "Companies in Bangalore, Pune, Hyderabad, Delhi, and Mumbai regularly hire "
                        "remote data analysts and junior data scientists. What they look for is your "
                        "portfolio — Kaggle profile, GitHub projects, and your ability to solve problems "
                        "with data. We help you build all of this during the course."
                    ),
                ),
                FAQItem(
                    question="What datasets will I work with?",
                    answer=(
                        "You will work with real-world datasets from Kaggle and public sources — student "
                        "performance data, house prices (Boston/Ames), Titanic survival, customer churn, "
                        "e-commerce transactions, movie ratings, loan applications, and more. No fake or "
                        "toy datasets. Every dataset has messy, missing, and inconsistent data — exactly "
                        "like the real world."
                    ),
                ),
                FAQItem(
                    question="How is this different from free courses on Coursera or YouTube?",
                    answer=(
                        "Free courses give you theory and small exercises. This course gives you 6 months "
                        "of structured, instructor-led training with 7+ real projects, code reviews, a "
                        "deployed ML app, a GitHub portfolio, a certificate, and placement support. The "
                        "difference is the same as watching cooking videos versus working in a kitchen "
                        "with a chef standing next to you."
                    ),
                ),
                FAQItem(
                    question="What can I do after this course to go deeper?",
                    answer=(
                        "After this course, you can specialise in: Deep Learning (CNNs, RNNs, "
                        "Transformers), Natural Language Processing (NLP), Computer Vision, MLOps "
                        "(deploying ML at scale), or move into a domain like healthcare AI, fintech "
                        "analytics, or marketing analytics. We provide a detailed roadmap in the final "
                        "week. You can also participate in Kaggle competitions to sharpen your skills."
                    ),
                ),
            ],
            projects=[
                ProjectItem(
                    title="Exploratory Data Analysis — E-Commerce Dataset",
                    description=(
                        "Perform a complete EDA on a real e-commerce transactions dataset. Load the "
                        "data with Pandas, handle missing values, analyse sales trends by category and "
                        "region, create 10+ visualisations with Matplotlib and Seaborn, and write a "
                        "summary report with actionable business insights."
                    ),
                ),
                ProjectItem(
                    title="House Price Prediction (Regression)",
                    description=(
                        "Build a Linear Regression model that predicts house prices based on features "
                        "like area, number of bedrooms, location, and age. Use the Ames Housing dataset "
                        "from Kaggle. Handle missing values, encode categorical features, scale numerical "
                        "features, evaluate with R2 and RMSE, and visualise predicted vs actual prices."
                    ),
                ),
                ProjectItem(
                    title="Customer Churn Classifier (Classification)",
                    description=(
                        "Build a classification model (Random Forest) that predicts whether a telecom "
                        "customer will leave the company. Feature engineering, handling class imbalance, "
                        "cross-validation, hyperparameter tuning with GridSearchCV. Evaluate with "
                        "confusion matrix, precision, recall, and F1-score."
                    ),
                ),
                ProjectItem(
                    title="Movie Recommendation System",
                    description=(
                        "Build a basic collaborative filtering recommendation system using the MovieLens "
                        "dataset. Calculate similarity between users or items, generate top-N "
                        "recommendations, and evaluate with simple metrics. Understand how Netflix and "
                        "Amazon recommendations work at a conceptual level."
                    ),
                ),
                ProjectItem(
                    title="Sentiment Analysis — Product Reviews",
                    description=(
                        "Build a simple NLP pipeline that classifies product reviews as positive or "
                        "negative. Text preprocessing (lowercase, stopwords, tokenisation), TF-IDF "
                        "vectorisation, train a Logistic Regression or Naive Bayes classifier, and "
                        "evaluate accuracy. Understand the basics of how opinion mining works."
                    ),
                ),
                ProjectItem(
                    title="ML Web App with Streamlit",
                    description=(
                        "Take one of your trained models (house price or churn) and build a simple web "
                        "interface using Streamlit. Users enter feature values (area, bedrooms, income) "
                        "and the app shows the prediction in real time. Deploy the app on Streamlit "
                        "Cloud so anyone can access it via a URL."
                    ),
                ),
                ProjectItem(
                    title="Capstone — End-to-End ML Pipeline (Your Choice)",
                    description=(
                        "Choose a real-world problem and dataset of your choice. Perform complete EDA, "
                        "clean and preprocess the data, try multiple ML algorithms, compare model "
                        "performance, select the best model, document your findings, deploy as a "
                        "Streamlit app, and upload everything to GitHub with a professional README. "
                        "This is your flagship portfolio project — the one you show in every interview."
                    ),
                ),
            ],
            skill_ids=[],
            category_id=0,
        ),
    ),
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

async def get_or_create_category(db, name: str, slug: str, display_order: int = 1):
    cat = await course_category_crud.get_by_slug(db, slug=slug)
    if cat:
        print(f"  [skip] category already exists: {name}")
        return cat
    cat = await course_category_crud.create(
        db,
        obj_in=CourseCategoryCreate(name=name, slug=slug, display_order=display_order),
    )
    print(f"  [+] created category: {name}")
    return cat


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

async def main():
    async with AsyncSessionLocal() as db:
        print("\n--- Categories ---")
        cat_ds = await get_or_create_category(
            db, "Data Science", "data-science", display_order=5
        )
        await db.commit()
        await db.refresh(cat_ds)

        cat_map = {
            "data-science": cat_ds,
        }

        print("\n--- Skills ---")
        skill_map = {}
        for name, slug in ALL_SKILLS:
            existing = await skill_crud.get_by_slug(db, slug=slug)
            skill = await skill_crud.get_or_create(db, name=name, slug=slug)
            skill_map[slug] = skill
            print(f"  [{'skip' if existing else '+'}] {name}")
        await db.commit()
        for slug in skill_map:
            await db.refresh(skill_map[slug])

        print("\n--- Courses ---")
        for entry in COURSES:
            course_obj: CourseCreate = entry["data"]
            if await course_crud.get_by_slug(db, course_obj.slug):
                print(f"  [skip] already exists: {course_obj.title}")
                continue
            course_obj.category_id = cat_map[entry["category_slug"]].id
            course_obj.skill_ids = [skill_map[s].id for s in entry["skill_slugs"]]
            await course_crud.create(db, obj_in=course_obj)
            print(f"  [+] created: {course_obj.title}")

        print("\nDone.\n")


if __name__ == "__main__":
    asyncio.run(main())
