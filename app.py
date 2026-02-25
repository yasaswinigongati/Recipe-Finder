from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ------------------ Recipe Data ------------------
recipes = {
    {
    "pasta": [
        "Boil water in a large pot and add salt",
        "Add pasta and cook for 8-12 minutes",
        "Drain the water and keep pasta aside",
        "Heat oil in a pan and saute garlic",
        "Add tomato or white sauce and cook for 2-3 minutes",
        "Add boiled pasta and mix well",
        "Add salt, pepper, and herbs",
        "Cook for 2 minutes and serve hot"
    ],

    "fried rice": [
        "Cook rice and let it cool completely",
        "Heat oil in a pan",
        "Add chopped garlic and saute",
        "Add chopped vegetables and stir fry on high flame",
        "Add cooked rice",
        "Add soy sauce, salt, and pepper",
        "Mix everything well",
        "Cook for 2-3 minutes and serve hot"
    ],

    "omelette": [
        "Break eggs into a bowl",
        "Add salt, pepper, and chopped onions or chilies",
        "Beat the mixture well",
        "Heat oil or butter in a pan",
        "Pour egg mixture into the pan",
        "Cook on medium flame",
        "Flip or fold and cook for another minute",
        "Serve hot"
    ],

    "maggi": [
        "Boil 1 and half cups of water in a pan",
        "Add Maggi noodles",
        "Break noodles gently",
        "Add the tastemaker masala",
        "Cook for 2-3 minutes while stirring",
        "Cook until water is absorbed",
        "Serve hot"
    ],

    "sandwich": [
        "Take two slices of bread",
        "Apply butter or mayonnaise",
        "Add sliced vegetables like cucumber, tomato, and onion",
        "Sprinkle salt and pepper",
        "Cover with another bread slice",
        "Toast in a pan or sandwich maker",
        "Cut and serve"
    ],

    "chicken curry": [
        "Heat oil in a pan",
        "Add chopped onions and saute until golden brown",
        "Add ginger garlic paste and cook for 1 minute",
        "Add turmeric, chili powder, coriander powder, and garam masala",
        "Add tomato puree and cook until oil separates",
        "Add chicken pieces and mix well",
        "Add water, cover, and cook for 20-25 minutes",
        "Garnish with coriander leaves",
        "Serve hot with rice or roti"
    ],

    "fruit salad": [
        "Wash all fruits properly",
        "Peel and cut fruits into small pieces",
        "Add fruits to a bowl",
        "Add sugar or honey if needed",
        "Add a few drops of lemon juice",
        "Mix gently",
        "Chill for 30 minutes and serve",
        "You can do this recipe with custard powder."
    ]
    }
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
