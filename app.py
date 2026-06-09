try:
    from flask import Flask, render_template, request, jsonify  # type: ignore[import]
except ImportError as exc:
    raise ImportError(
        "Missing dependency 'flask'. Install it with 'pip install flask'."
    ) from exc
try:
    import google.generativeai as genai  # type: ignore[import]
except ImportError as exc:
    raise ImportError(
        "Missing dependency 'google-generativeai'. Install it with 'pip install google-generativeai'."
    ) from exc
try:
    from dotenv import load_dotenv  # type: ignore[import]
except ImportError:
    load_dotenv = None

import os

# Load environment variables if python-dotenv is installed
if load_dotenv:
    load_dotenv()

app = Flask(__name__)

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


# ---------------------------
# Carbon Footprint Calculator
# ---------------------------

def calculate_carbon_score(travel, electricity, food, shopping):
    """
    Simple carbon footprint estimation.
    Values are weighted for demonstration purposes.
    """

    score = (
        (travel * 2.5)
        + (electricity * 1.8)
        + (food * 1.5)
        + (shopping * 1.2)
    )

    return round(score, 2)


def get_footprint_level(score):
    if score < 100:
        return "Low"
    elif score < 250:
        return "Moderate"
    else:
        return "High"


# ---------------------------
# Routes
# ---------------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    try:

        data = request.get_json()

        travel = float(data.get("travel", 0))
        electricity = float(data.get("electricity", 0))
        food = float(data.get("food", 0))
        shopping = float(data.get("shopping", 0))

        score = calculate_carbon_score(
            travel,
            electricity,
            food,
            shopping
        )

        level = get_footprint_level(score)

        return jsonify({
            "success": True,
            "carbon_score": score,
            "impact_level": level
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/ai-insights", methods=["POST"])
def ai_insights():

    try:

        data = request.get_json()

        score = data.get("carbon_score")
        level = data.get("impact_level")

        prompt = f"""
        You are a sustainability expert and climate coach.

        User Carbon Score: {score}
        Impact Level: {level}

        Provide:

        1. Short analysis of their footprint.
        2. Top 3 reasons why emissions may be high.
        3. 5 personalized suggestions.
        4. One weekly sustainability challenge.
        5. Motivational closing message.

        Keep the response concise,
        professional,
        beginner-friendly,
        and action-oriented.
        """

        response = model.generate_content(prompt)

        return jsonify({
            "success": True,
            "insights": response.text
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/future-simulation", methods=["POST"])
def future_simulation():

    try:

        data = request.get_json()

        score = data.get("carbon_score")

        prompt = f"""
        You are an environmental analyst.

        User Carbon Score: {score}

        Generate:

        Scenario A:
        If current habits continue for 5 years.

        Scenario B:
        If eco-friendly recommendations are followed.

        Compare:

        - Environmental impact
        - Lifestyle benefits
        - Carbon reduction potential

        Keep response under 250 words.
        """

        response = model.generate_content(prompt)

        return jsonify({
            "success": True,
            "simulation": response.text
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ---------------------------
# Health Check Route
# ---------------------------

@app.route("/health")
def health():
    return jsonify({
        "status": "running",
        "project": "EarthMirror AI"
    })


# ---------------------------
# Run App
# ---------------------------

if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )