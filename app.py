from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ------------------ Recipe Data ------------------
recipes = {
    "pasta": ["Boil pasta", "Add sauce", "Mix well"],
    "fried rice": ["Cook rice", "Add veggies", "Fry together"],
    "omelette": ["Beat eggs", "Add salt", "Cook on pan"],
    "maggi": ["Boil water", "Add noodles", "Add masala"],
    "sandwich": ["Add veggies", "Apply butter", "Toast it"],
    "chicken curry": ["Cook chicken", "Add curry", "Serve with rice"],
    "fruit salad": ["Cut fruits", "Add sugar", "Mix well"]
}

# ------------------ Simple AI Logic ------------------
def ai_suggest_recipe(user_input):
    suggestions = []
    tips = [
        "Try adding fresh herbs for better taste 🍃",
        "Cook on low flame for richer flavor 🔥",
        "Use fresh ingredients for best results 🥗"
    ]

    for recipe in recipes.keys():
        if user_input in recipe or recipe in user_input:
            suggestions.append(recipe)

    return {
        "suggestions": suggestions[:3],
        "tip": tips[len(user_input) % len(tips)]
    }

# ------------------ Web Page ------------------
@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    query = ""
    ai_data = None

    if request.method == "POST":
        query = request.form.get("recipe").lower()
        result = recipes.get(query)

        if not result:
            ai_data = ai_suggest_recipe(query)

    return render_template(
        "index.html",
        result=result,
        query=query,
        ai_data=ai_data
    )

# ------------------ REST APIs ------------------

@app.route("/api/recipes", methods=["GET"])
def get_all_recipes():
    return jsonify(list(recipes.keys()))

@app.route("/api/recipe/<name>", methods=["GET"])
def get_recipe(name):
    recipe = recipes.get(name.lower())
    if recipe:
        return jsonify({"recipe": name, "steps": recipe})
    return jsonify({"error": "Recipe not found"}), 404

@app.route("/api/suggest", methods=["POST"])
def suggest_recipe():
    data = request.get_json()
    user_input = data.get("query", "")
    return jsonify(ai_suggest_recipe(user_input))


if __name__ == "__main__":
    app.run(debug=True)
