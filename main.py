from flask import Flask, render_template, request, jsonify
import logging
from recommender import topMatches, dataFrame

# Initialize the Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    """Main route for skill recommendation."""
    if request.method == 'POST':
        try:
            result = request.form
            requirement = {
                "REQUIREMENT": {
                    "HTML": int(result.get('html', 0)),
                    "Python": int(result.get('python', 0)),
                    "Java": int(result.get('java', 0)),
                    "C": int(result.get('c', 0)),
                    "JavaScript": int(result.get('javascript', 0))
                }
            }
            num_of_candidate = int(result.get('candidate', 5))
            recommendations = topMatches(requirement, dataFrame, "REQUIREMENT", num_of_candidate)
            logger.info("Recommendations generated successfully.")
            return render_template("index.html", result=recommendations)
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            return render_template("index.html", result=[], error="An error occurred. Please try again.")

    # For GET requests, render the form
    return render_template("index.html", result=[(1.0, "ExampleName")]) 

@app.route('/api/recommend', methods=['POST'])
def api_recommend():
    """API endpoint for skill recommendation."""
    try:
        data = request.json
        requirement = data.get("requirement", {})
        num_of_candidate = data.get("num_of_candidate", 5)
        recommendations = topMatches({"REQUIREMENT": requirement}, dataFrame, "REQUIREMENT", num_of_candidate)
        return jsonify({"status": "success", "data": recommendations})
    except Exception as e:
        logger.error(f"Error in API: {e}")
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
