#include Strands Dependencies
from strands import Agent
from strands import tool
from strands.models import BedrockModel
import os

from strands_tools import current_time


#TODO:Uncomment the following line and add the tool you want to include
#Use this to include build_in tools from Strands
#from strands_tools import

region = os.environ['region']

#Step:1 Model Initialization
model_id = "amazon.nova-lite-v1:0"   #Fill Model ID here
model = BedrockModel(
    region_name = region,
    model_id=model_id,
    temperature=0.1,
    top_p=0.1
)

#Include code for Custom Tools here with @tool decorator
@tool
def get_recipe(ingredients: str) -> str:
    """
    Get a recipe suggestion based on available ingredients.
    Args:
        ingredients (str): Comma-separated list of ingredients
    Returns:
        str: A recipe using the available ingredients with preparation time
    """
    # Convert ingredients to list and clean up
    ingredient_list = [i.strip().lower() for i in ingredients.split(',')]
    
    # Recipe database with preparation times (in minutes)
    recipes = {
        "pasta,tomato,garlic": {
            "recipe": "Quick Pasta Arrabbiata:\n1. Boil pasta\n2. Sauté garlic in olive oil\n3. Add chopped tomatoes\n4. Season with red pepper flakes\n5. Mix with pasta",
            "prep_time": 15
        },
        
        "rice,egg,carrot": {
            "recipe": "Simple Fried Rice:\n1. Cook rice\n2. Dice carrots\n3. Scramble eggs\n4. Stir-fry everything together\n5. Season with soy sauce",
            "prep_time": 20
        },
        
        "potato,onion,cheese": {
            "recipe": "Cheesy Hash Browns:\n1. Grate potatoes and onion\n2. Mix and drain excess water\n3. Form into patties\n4. Pan-fry until golden\n5. Top with cheese",
            "prep_time": 25
        },
        
        "chicken,lemon,garlic": {
            "recipe": "Lemon Garlic Chicken:\n1. Season chicken\n2. Sauté garlic\n3. Add chicken and lemon juice\n4. Cook until done\n5. Garnish with herbs",
            "prep_time": 30
        }
    }
    
    # Find matching recipe
    for recipe_ingredients, recipe_data in recipes.items():
        required = set(recipe_ingredients.split(','))
        available = set(ingredient_list)
        if required.issubset(available):
            return f"{recipe_data['recipe']}\n\nPreparation time: {recipe_data['prep_time']} minutes"
            
    return "No recipe found for these ingredients. Try different combinations!"

#Step:2 Agent Initialization
agent = Agent(
    system_prompt=(
    "You're a helpful cooking assistant. Use the get_recipe tool to suggest "
    "recipes based on available ingredients. When providing recipes, also use "
    "Also use current_time tool to get the current time and add the preparation time to it, and tell when user can expect"
    "their order based on current time if you have the time tool or else just return the recipe"),
    tools=[get_recipe, current_time],
    model=model
)


def lambda_handler(event, context):

    
    #TODO: Update the query to check the updated response for each task.
    query = "Can you suggest me some recipe based on rice, egg, carrot and tell me when can I get it ready?"
    
    
    print(model_id)
    
    
    
    response = agent(query)
    response = str(response)

    print()
    print("Agent Working")
    

    return {
        'statusCode': 200,
        'body': 'Hello from Strands-Agent!'
    }
