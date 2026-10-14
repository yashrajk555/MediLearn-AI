import os
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

app.secret_key = os.environ.get(
    "MEDILEARN_SECRET_KEY",
    "medilearn-local-development-key"
)

# SYMPTOM DATABASE

SYMPTOMS = {
    "Headache": {
        "questions": [
            {
                "question": "How severe is your headache?",
                "options": [
                    "Mild",
                    "Moderate",
                    "Severe",
                    "Sudden and extremely severe"
                ]
            },
            {
                "question": "How long have you had the headache?",
                "options": [
                    "Less than one day",
                    "1–3 days",
                    "More than 3 days",
                    "It started suddenly"
                ]
            },
            {
                "question": "Do you have any other symptoms?",
                "options": [
                    "Nausea",
                    "Fever",
                    "Blurred vision",
                    "No other symptoms"
                ]
            }
        ],
        "care": [
            "Rest in a quiet, comfortable room.",
            "Drink water regularly.",
            "Take breaks from screens and bright lights."
        ],
        "remedies": [
            "Rest in a quiet, dimly lit room.",
            "Drink water if you may be dehydrated.",
            "A cool cloth on the forehead may provide comfort."
        ],
        "medicine": (
            "MEDICINE : Paracetamol, ibuprofen may be appropriate for some adults."
            "WHEN TO TAKE : Take at the very first sign of onset pain.\n"
            "Waiting until a headache becomes severe makes it harder to manage with over-the-counter options.\n"
            "Why to Take It: They block the localized chemical messengers (prostaglandins) responsible for sending pain signals from nerve endings to the brain.\n"
        )
    },

    "Fever": {
        "questions": [
            {
                "question": "What is your measured temperature?",
                "options": [
                    "Below 38°C",
                    "38–39°C",
                    "Above 39°C",
                    "I have not measured it"
                ]
            },
            {
                "question": "How long have you had the fever?",
                "options": [
                    "Less than one day",
                    "1–2 days",
                    "3 days or longer",
                    "It keeps returning"
                ]
            },
            {
                "question": "Do you have any other symptoms?",
                "options": [
                    "Cough or cold",
                    "Body aches",
                    "Rash",
                    "Breathing difficulty"
                ]
            }
        ],
        "care": [
            "Rest and drink fluids regularly.",
            "Monitor your temperature.",
            "Wear comfortable clothing and avoid overheating."
        ],
        "remedies": [
            "Drink water regularly.",
            "Rest in a comfortably cool room.",
            "Use a lukewarm cloth if it helps you feel comfortable."
        ],
        "medicine": (
            "MEDICINE : Acetaminophen (Paracetamol) or Ibuprofen. \n"
            "When to Take It: Take when body temperature rises above 38°C (100.4°F) or causes physical distress. Repeat every 4 to 6 hours as needed, not exceeding safe daily dosage maximums on the package.\n "
            "Why to Take It: These agents lower the hypothalamus set point (the body's internal thermostat) in the brain to reduce body temperature and alleviate accompanying chills.\n"
        )
   
    },

    

    "Cough": {
        "questions": [
            {
                "question": "What type of cough do you have?",
                "options": [
                    "Dry cough",
                    "Cough with mucus",
                    "Cough mostly at night",
                    "Cough with blood"
                ]
            },
            {
                "question": "How long have you been coughing?",
                "options": [
                    "Less than 3 days",
                    "3–7 days",
                    "1–3 weeks",
                    "More than 3 weeks"
                ]
            },
            {
                "question": "Do you have any other symptoms?",
                "options": [
                    "Sore throat",
                    "Fever",
                    "Runny nose",
                    "Breathing difficulty"
                ]
            }
        ],
        "care": [
            "Drink fluids regularly.",
            "Avoid smoke, dust, and other irritants.",
            "Seek medical advice if your cough persists or worsens."
        ],
        "remedies": [
            "Warm fluids may soothe throat irritation.",
            "Honey may help relieve coughing in people older than one year.",
            "Avoid smoking and exposure to second-hand smoke."
        ],
        "medicine": (
            "Medicine Required: Dextromethorphan (for dry coughs) or Guaifenesin (for wet/chesty coughs).\n"
            "Why to Take It: Dextromethorphan calms an over-stimulated cough reflex center in the brain. Guaifenesin works locally in the lungs to thin down thick, sticky mucus so it can be cleared easily.\n"
            "When to Take It: Take every 4 to 8 hours (depending on the chosen drug type). Expectorants are best taken during waking hours with plenty of water.\n"
        )
    },

    "Cold": {
        "questions": [
            {
                "question": "Which cold symptoms do you have?",
                "options": [
                    "Runny nose",
                    "Sneezing",
                    "Blocked nose",
                    "Sore throat"
                ]
            },
            {
                "question": "How long have you had these symptoms?",
                "options": [
                    "1–2 days",
                    "3–5 days",
                    "6–10 days",
                    "More than 10 days"
                ]
            },
            {
                "question": "Do you also have a fever?",
                "options": [
                    "No fever",
                    "Mild fever",
                    "High fever",
                    "Not sure"
                ]
            }
        ],
        "care": [
            "Get sufficient rest.",
            "Drink fluids regularly.",
            "Wash your hands and avoid sharing personal items."
        ],
        "remedies": [
            "Saline nasal spray may help with nasal congestion.",
            "Warm drinks may soothe throat discomfort.",
            "A clean humidifier may help if the air is dry."
        ],
        "medicine": (
            "Medicine Required: Dextromethorphan (for dry coughs) or Guaifenesin (for wet/chesty coughs).\n"
            "Why to Take It: Dextromethorphan calms an over-stimulated cough reflex center in the brain. Guaifenesin works locally in the lungs to thin down thick, sticky mucus so it can be cleared easily.\n"
            "When to Take It: Take every 4 to 8 hours (depending on the chosen drug type). Expectorants are best taken during waking hours with plenty of water.\n"
 )
    },

    "Stomach Pain": {
        "questions": [
            {
                "question": "Where is the pain located?",
                "options": [
                    "Upper abdomen",
                    "Lower abdomen",
                    "Around the belly button",
                    "Pain throughout the abdomen"
                ]
            },
            {
                "question": "How severe is the pain?",
                "options": [
                    "Mild",
                    "Moderate",
                    "Severe",
                    "Sudden or rapidly worsening"
                ]
            },
            {
                "question": "Do you have other symptoms?",
                "options": [
                    "Nausea",
                    "Vomiting",
                    "Diarrhea",
                    "Blood in stool"
                ]
            }
        ],
        "care": [
            "Pay attention to whether the pain is worsening.",
            "Drink small amounts of water if you can keep fluids down.",
            "Seek medical advice for persistent or unexplained pain."
        ],
        "remedies": [
            "Rest in a comfortable position.",
            "Take small sips of water if tolerated.",
            "Avoid foods that clearly worsen your discomfort."
        ],
        "medicine": (
            "Medicine Required: Dicyclomine (for intestinal cramps) or Antacids (for burning upper stomach pain).\n"
            "Why to Take It: Antispasmodics relax hyperactive smooth muscles in the gut walls. Antacids chemically neutralize excess gastric acid causing irritation.\n"
            "When to Take It: Antispasmodics are typically taken 30 minutes before meals. Antacids are taken after meals or immediately when burning acid reflux flares up.\n"    
        )
    },

    "Nausea": {
        "questions": [
            {
                "question": "Are you vomiting?",
                "options": [
                    "No vomiting",
                    "Vomited once",
                    "Vomiting repeatedly",
                    "Unable to keep fluids down"
                ]
            },
            {
                "question": "When did the nausea begin?",
                "options": [
                    "Today",
                    "1–2 days ago",
                    "More than 2 days ago",
                    "It keeps returning"
                ]
            },
            {
                "question": "Do you have other symptoms?",
                "options": [
                    "Stomach pain",
                    "Fever",
                    "Dizziness",
                    "Severe headache"
                ]
            }
        ],
        "care": [
            "Take small, frequent sips of fluids.",
            "Rest and avoid strong smells if they worsen nausea.",
            "Seek help if vomiting continues or dehydration develops."
        ],
        "remedies": [
            "Try small sips of water or oral rehydration solution.",
            "Eat small portions of simple foods if tolerated.",
            "Avoid greasy meals if they worsen your symptoms."
        ],
        "medicine": (
            "Medicine Required: Ginger Extract Supplements or Bismuth Subsalicylate.\n"
            "Why to Take It: These line and protect the gastric mucosal walls while calming mild hyper-motility rhythms inside the stomach.\n"
            "When to Take It: Take 30 to 60 minutes prior to travel or at the immediate onset of any stomach queasiness.\n"
        )
    },

    "Sore Throat": {
        "questions": [
            {
                "question": "How severe is your throat pain?",
                "options": [
                    "Mild irritation",
                    "Pain while swallowing",
                    "Severe pain",
                    "Difficulty swallowing saliva"
                ]
            },
            {
                "question": "How long have you had the sore throat?",
                "options": [
                    "Less than 2 days",
                    "2–4 days",
                    "5–7 days",
                    "More than 7 days"
                ]
            },
            {
                "question": "Do you have other symptoms?",
                "options": [
                    "Cough",
                    "Fever",
                    "Runny nose",
                    "Neck swelling"
                ]
            }
        ],
        "care": [
            "Drink fluids regularly.",
            "Avoid smoke and other throat irritants.",
            "Seek medical advice if symptoms persist or worsen."
        ],
        "remedies": [
            "Warm drinks may soothe throat discomfort.",
            "Gargling with warm salt water may help adults who can gargle safely.",
            "Rest your voice if speaking causes discomfort."
        ],
        "medicine": (
            "Medicine Required: Benzocaine Lozenges, Amylmetacresol, or mild oral analgesics."
            "Why to Take It: Topical lozenges act as local anesthetics to temporarily deaden pain receptors on the surface of your throat, making swallowing comfortable.\n"
            "When to Take It: Allow a lozenge to dissolve slowly in the mouth every 2 to 3 hours as needed for localized raw irritation.\n"
        )
    },

    "Fatigue": {
        "questions": [
            {
                "question": "How long have you felt unusually tired?",
                "options": [
                    "Today",
                    "Several days",
                    "Several weeks",
                    "More than a month"
                ]
            },
            {
                "question": "How has your sleep been?",
                "options": [
                    "Good sleep",
                    "Less sleep than usual",
                    "Poor-quality sleep",
                    "Still tired despite enough sleep"
                ]
            },
            {
                "question": "Do you have other symptoms?",
                "options": [
                    "Dizziness",
                    "Fever",
                    "Shortness of breath",
                    "No other symptoms"
                ]
            }
        ],
        "care": [
            "Maintain a regular sleep schedule.",
            "Eat balanced meals and drink enough water.",
            "Arrange a medical assessment if fatigue persists."
        ],
        "remedies": [
            "Allow yourself time to rest.",
            "Eat regular, balanced meals.",
            "Try gentle activity if you feel well enough."
        ],
        "medicine": (
            "Medicine Required: Supportive care via Electrolyte Solutions (No active OTC chemical drug treats basic fatigue).\n"
            "Why to Take It: Replacing depleted hydration and resting restores basic metabolic cellular functionality, letting your immune pathways mend naturally.\n"
            "When to Take It: Administer fluids steadily over the course of the day and balance with extensive physical rest periods.\n"          )
    },

    "Body Pain": {
        "questions": [
            {
                "question": "Where do you feel the pain?",
                "options": [
                    "Arms or legs",
                    "Back or neck",
                    "All over the body",
                    "One joint"
                ]
            },
            {
                "question": "How severe is the pain?",
                "options": [
                    "Mild",
                    "Moderate",
                    "Severe",
                    "Sudden with weakness"
                ]
            },
            {
                "question": "Do you have other symptoms?",
                "options": [
                    "Fever",
                    "Swelling",
                    "Recent injury",
                    "Numbness"
                ]
            }
        ],
        "care": [
            "Rest from activities that aggravate the pain.",
            "Stay hydrated.",
            "Seek medical advice for persistent, unexplained, or worsening pain."
        ],
        "remedies": [
            "A comfortable resting position may help.",
            "Gentle movement may be useful if it does not worsen pain.",
            "Do not massage an area with a suspected serious injury."
        ],
        "medicine": (
           "Medicine Required: Ibuprofen or Naproxen (NSAIDs).\n"
            "Why to Take It: They function directly at the site of inflammation to minimize tissue swelling, target aching joints, and soothe sore muscles.\n"
            "When to Take It: Take with a meal or a glass of milk every 6 to 12 hours as needed to safeguard the stomach lining from direct drug irritation.\n"

        )
    },

    "Diarrhea": {
        "questions": [
            {
                "question": "How often have you had loose stools today?",
                "options": [
                    "1–2 times",
                    "3–5 times",
                    "More than 5 times",
                    "Very frequent watery stools"
                ]
            },
            {
                "question": "How long has this been happening?",
                "options": [
                    "Started today",
                    "1–2 days",
                    "3 days or longer",
                    "It keeps returning"
                ]
            },
            {
                "question": "Do you have other symptoms?",
                "options": [
                    "Stomach cramps",
                    "Fever",
                    "Blood in stool",
                    "Dizziness or very little urine"
                ]
            }
        ],
        "care": [
            "Replace lost fluids and electrolytes.",
            "Monitor urination and signs of dehydration.",
            "Seek medical advice if symptoms are severe or persistent."
        ],
        "remedies": [
            "Use commercially prepared oral rehydration solution according to its instructions.",
            "Take small, frequent sips of fluid.",
            "Eat simple foods as tolerated."
        ],
        "medicine": (
            "Medicine Required: Oral Rehydration Salts (ORS) and Loperamide.\n",
            "Why to Take It: ORS replaces essential lost minerals and water to protect heart and cellular function. Loperamide slows down over-speeding intestinal movement to let the colon absorb fluids.\n",
            "When to Take It: Sip ORS steadily throughout the day following every loose movement. Take Loperamide only after clear non-bacterial loose stools start. Stop completely if a fever or bloody stools develop.\n"
        )
    }
}



# WARNING SIGNS


EMERGENCY_ANSWERS = {
    "Sudden and extremely severe",
    "Breathing difficulty",
    "Cough with blood",
    "Sudden or rapidly worsening",
    "Blood in stool",
    "Unable to keep fluids down",
    "Difficulty swallowing saliva",
    "Shortness of breath",
    "Sudden with weakness",
    "Dizziness or very little urine"
}


def has_warning_signs(answers):
    """Check answers for possible warning signs."""
    for symptom_answers in answers.values():
        for answer in symptom_answers.values():
            if answer in EMERGENCY_ANSWERS:
                return True
    return False



# HOME PAGE


@app.route("/", endpoint="home")
@app.route("/index", endpoint="index")
def home():
    return render_template(
        "index.html",
        page="home",
        symptoms=list(SYMPTOMS.keys())
    )



# START QUIZ


@app.route("/start_assessment", methods=["GET", "POST"])
def start_assessment():

    if request.method == "POST":
        selected_symptoms = request.form.getlist("symptoms")

        # Also support a single-select HTML field.
        if not selected_symptoms:
            single_symptom = request.form.get("symptom", "")
            if single_symptom:
                selected_symptoms = [single_symptom]

        # Only accept symptoms in our database.
        selected_symptoms = [
            symptom for symptom in selected_symptoms
            if symptom in SYMPTOMS
        ]

        if not selected_symptoms:
            flash(
                "Please select at least one symptom to continue.",
                "error"
            )
            return redirect(url_for("home") + "#quiz")

        session["selected_symptoms"] = selected_symptoms
        session["answers"] = {}
        session["current_symptom_index"] = 0

        return redirect(url_for("questions"))

    return redirect(url_for("home") + "#quiz")



# FOLLOW-UP QUESTIONS


@app.route("/questions", methods=["GET", "POST"])
def questions():

    selected_symptoms = session.get("selected_symptoms", [])

    if not selected_symptoms:
        flash(
            "Please start your symptom assessment first.",
            "error"
        )
        return redirect(url_for("home"))

    index = int(session.get("current_symptom_index", 0))

    if index < 0 or index >= len(selected_symptoms):
        return redirect(url_for("result"))

    symptom = selected_symptoms[index]
    questions_list = SYMPTOMS[symptom]["questions"]

    if request.method == "POST":

        submitted_answers = {}

        for question_index, question_data in enumerate(questions_list):
            field_name = f"question_{question_index}"
            answer = request.form.get(field_name, "").strip()

            if answer not in question_data["options"]:
                flash(
                    "Please answer every question before continuing.",
                    "error"
                )
                return redirect(url_for("questions"))

            submitted_answers[question_data["question"]] = answer

        all_answers = session.get("answers", {})
        all_answers[symptom] = submitted_answers
        session["answers"] = all_answers

        index += 1
        session["current_symptom_index"] = index

        if index >= len(selected_symptoms):
            return redirect(url_for("result"))

        return redirect(url_for("questions"))

    return render_template(
        "index.html",
        page="questions",
        symptom=symptom,
        questions=questions_list,
        current_number=index + 1,
        total_symptoms=len(selected_symptoms),
        symptoms=selected_symptoms
    )



# RESULTS


@app.route("/result")
def result():

    selected_symptoms = session.get("selected_symptoms", [])
    answers = session.get("answers", {})

    if not selected_symptoms:
        flash(
            "Please complete the symptom assessment first.",
            "error"
        )
        return redirect(url_for("home"))

    results = []

    for symptom in selected_symptoms:
        symptom_data = SYMPTOMS[symptom]

        results.append({
            "symptom": symptom,
            "answers": answers.get(symptom, {}),
            "care": symptom_data["care"],
            "remedies": symptom_data["remedies"],
            "medicine": symptom_data["medicine"]
        })

    emergency_warning = has_warning_signs(answers)

    return render_template(
        "index.html",
        page="result",
        results=results,
        emergency_warning=emergency_warning,
        symptoms=selected_symptoms,
        answers=answers
    )



# RESTART QUIZ


@app.route("/restart")
def restart():

    session.pop("selected_symptoms", None)
    session.pop("answers", None)
    session.pop("current_symptom_index", None)

    return redirect(url_for("home"))



# RUN APPLICATIONs


if __name__ == "__main__":
    app.run(debug=True)
