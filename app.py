from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness.db'
db = SQLAlchemy(app)

# Set up Watson Assistant
authenticator = IAMAuthenticator('eindvguW_wj4OvhY8taGcG5wQxKN5t4abMr9IrxaF8V8')
assistant = AssistantV2(
    version='2021-06-14',
    authenticator=authenticator
)
assistant.set_service_url(
    'https://api.us-south.assistant.watson.cloud.ibm.com/instances/e73a3236-f19b-4a60-8b25-354ad97dc89f')
assistant_id = '3b7edfa7-5137-4cfa-8528-7294a0ba50a5'


# Define your database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    day = db.Column(db.String(20), nullable=False)
    workout = db.Column(db.String(200), nullable=False)


def get_meal_plan(goal):
    meal_plans = {
        "muscle_gain": {
            "description": "Meal plan for muscle gain:",
            "foods": [
                "Lean proteins: Chicken breast, turkey, lean beef, fish, eggs",
                "Complex carbohydrates: Brown rice, quinoa, sweet potatoes, oatmeal",
                "Healthy fats: Avocado, nuts, olive oil, fatty fish",
                "Vegetables: Broccoli, spinach, kale, bell peppers",
                "Fruits: Bananas, berries, apples",
                "Dairy: Greek yogurt, cottage cheese, milk"
            ]
        },
        "vegetarian": {
            "description": "Vegetarian meal plan:",
            "foods": [
                "Plant-based proteins: Tofu, tempeh, seitan, legumes, quinoa",
                "Whole grains: Brown rice, whole grain bread, oats, barley",
                "Vegetables: Leafy greens, broccoli, cauliflower, carrots, tomatoes",
                "Fruits: Berries, citrus fruits, apples, bananas",
                "Healthy fats: Avocado, nuts, seeds, olive oil",
                "Dairy alternatives: Plant-based milk, yogurt, and cheese"
            ]
        },
        "beginner": {
            "description": "General healthy eating plan for beginners:",
            "foods": [
                "Lean proteins: Chicken breast, fish, lean beef, eggs",
                "Complex carbohydrates: Brown rice, sweet potatoes, oatmeal",
                "Vegetables: Broccoli, spinach, mixed salad greens, carrots",
                "Fruits: Apples, bananas, berries, oranges",
                "Healthy fats: Avocado, nuts, olive oil",
                "Dairy: Low-fat milk, yogurt, cheese"
            ]
        },
        "healthy_snacks": {
            "description": "Healthy snack options:",
            "foods": [
                "Fresh fruits: Apples, berries, bananas",
                "Raw vegetables with hummus",
                "Greek yogurt with nuts and berries",
                "Hard-boiled eggs",
                "Whole grain crackers with cheese or nut butter",
                "Trail mix (nuts, seeds, and dried fruits)",
                "Edamame",
                "Air-popped popcorn"
            ]
        },
        "brain_health": {
            "description": "Foods for maintaining a healthy mind:",
            "foods": [
                "Fatty fish: Salmon, mackerel, sardines (rich in omega-3 fatty acids)",
                "Berries: Blueberries, strawberries, blackberries",
                "Nuts and seeds: Walnuts, almonds, pumpkin seeds",
                "Dark chocolate (70% cocoa or higher)",
                "Leafy greens: Spinach, kale, collard greens",
                "Whole grains: Quinoa, brown rice, oats",
                "Avocados",
                "Green tea"
            ]
        },
        "weight_loss": {
            "description": "Meal plan for weight loss:",
            "foods": [
                "Lean proteins: Grilled chicken, fish, tofu, egg whites",
                "Non-starchy vegetables: Broccoli, spinach, cauliflower, zucchini",
                "Complex carbohydrates (in moderation): Quinoa, brown rice, sweet potatoes",
                "Fruits (in moderation): Berries, apples, grapefruit",
                "Healthy fats (in moderation): Avocado, nuts, olive oil",
                "Low-fat dairy: Greek yogurt, cottage cheese",
                "Legumes: Lentils, chickpeas, black beans"
            ]
        },
        "bulk": {
            "description": "General healthy eating plan for bulking:",
            "foods": [
                "Lean proteins: Chicken breast, turkey, fish, lean beef, eggs, tofu",
                "Complex carbohydrates: Brown rice, sweet potatoes, quinoa, whole wheat pasta, oats",
                "Vegetables: Broccoli, spinach, bell peppers, mixed salad greens, zucchini",
                "Fruits: Bananas, berries, apples, mangoes, pineapples",
                "Healthy fats: Avocado, nuts, seeds, olive oil, coconut oil",
                "Dairy: Whole milk, Greek yogurt, cheese, cottage cheese"
            ]
        },
        "lean": {
            "description": "General healthy eating plan for staying lean:",
            "foods": [
                "Lean proteins: Chicken breast, turkey, fish, lean beef, egg whites",
                "Complex carbohydrates: Quinoa, brown rice, sweet potatoes, whole wheat bread",
                "Vegetables: Broccoli, kale, spinach, mixed salad greens, cucumbers",
                "Fruits: Apples, berries, oranges, grapefruit",
                "Healthy fats: Avocado, almonds, chia seeds, olive oil",
                "Dairy: Low-fat yogurt, cottage cheese, skim milk"
            ]
        },
        "vegan": {
            "description": "General healthy eating plan for vegans:",
            "foods": [
                "Plant-based proteins: Tofu, tempeh, lentils, chickpeas, black beans",
                "Complex carbohydrates: Quinoa, brown rice, sweet potatoes, whole wheat pasta",
                "Vegetables: Broccoli, spinach, bell peppers, mixed salad greens, kale",
                "Fruits: Bananas, berries, apples, mangoes, pineapples",
                "Healthy fats: Avocado, nuts, seeds, olive oil, coconut oil",
                "Dairy substitutes: Almond milk, soy milk, coconut yogurt, nutritional yeast"
            ]
        }

    }
    return meal_plans.get(goal, meal_plans["beginner"])


with app.app_context():
    db.create_all()


def get_user_schedule(user_id):
    schedule = Schedule.query.filter_by(user_id=user_id).all()
    return "\n".join([f"{s.day}: {s.workout}" for s in schedule])


@app.route('/', methods=['GET'])
def home():
    return "Welcome to the Gym Trainer API!"


@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        app.logger.info(f"Received data: {data}")  # Log the incoming data

        intent = data.get('intent', '')
        if not intent:
            return jsonify({"error": "Intent is missing"}), 400

        if intent == 'get_schedule':
            default_schedule = "Monday: Cardio\nTuesday: Strength Training\nWednesday: Yoga\nThursday: HIIT\nFriday: Rest"
            return jsonify({"schedule": default_schedule})

        elif intent == 'get_nutritional_value':
            user_input = data.get('user_input', '').lower()

            if 'muscle gain' in user_input:
                meal_plan = get_meal_plan('muscle_gain')
            elif 'vegetarian' in user_input:
                meal_plan = get_meal_plan('vegetarian')
            elif 'healthy snacks' in user_input:
                meal_plan = get_meal_plan('healthy_snacks')
            elif 'healthy mind' in user_input:
                meal_plan = get_meal_plan('brain_health')
            elif 'lose weight' in user_input:
                meal_plan = get_meal_plan('weight_loss')
            elif 'bulk' in user_input:
                meal_plan = get_meal_plan('bulk')
            elif 'lean' in user_input:
                meal_plan = get_meal_plan('lean')
            elif 'vegan' in user_input:
                meal_plan = get_meal_plan('vegan')
            else:
                meal_plan = get_meal_plan('beginner')

            response = f"{meal_plan['description']}\n\n"
            response += "\n".join(f"• {food}" for food in meal_plan['foods'])

            return jsonify({"response": response})

        elif intent == 'set_workout_schedule':
            return jsonify({"message": "Workout schedule update request received"})

        else:
            return jsonify({"error": "Unknown intent"}), 400

    except Exception as e:
        app.logger.error(f"Webhook error: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
