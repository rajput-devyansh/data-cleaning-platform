import streamlit as st
import yaml

from core.recipes.loader import load_recipe
from core.recipes.executor import RecipeExecutor
from core.recipes.storage import save_recipe, list_recipes

st.header("🧾 Cleaning Recipes")

dataset_id = st.text_input("Dataset ID")

if not dataset_id:
    st.stop()

st.subheader("Create / Edit Recipe")

recipe_text = st.text_area(
    "Recipe YAML",
    height=250,
    value="steps:\n  - action: drop_nulls\n    column: Ticket_ID\n",
)

recipe_name = st.text_input("Recipe name")

col1, col2 = st.columns(2)

with col1:
    if st.button("Validate (Dry-Run)"):
        try:
            recipe = yaml.safe_load(recipe_text)
            executor = RecipeExecutor(dataset_id)
            plan = executor.execute(recipe, dry_run=True)

            st.success("Recipe is valid")
            st.json(plan)

        except Exception as e:
            st.error(str(e))

with col2:
    if st.button("Save Recipe"):
        try:
            recipe = yaml.safe_load(recipe_text)
            path = save_recipe(dataset_id, recipe_name, recipe)
            st.success(f"Saved to {path}")
        except Exception as e:
            st.error(str(e))

st.divider()

st.subheader("Saved Recipes")

recipes = list_recipes(dataset_id)
if recipes:
    st.write(recipes)
else:
    st.info("No saved recipes yet.")