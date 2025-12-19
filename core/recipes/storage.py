import os
import yaml

BASE_RECIPE_DIR = "data/recipes"


def save_recipe(dataset_id: str, name: str, recipe: dict):
    path = os.path.join(BASE_RECIPE_DIR, dataset_id)
    os.makedirs(path, exist_ok=True)

    full_path = os.path.join(path, f"{name}.yaml")

    with open(full_path, "w") as f:
        yaml.safe_dump(recipe, f)

    return full_path


def list_recipes(dataset_id: str):
    path = os.path.join(BASE_RECIPE_DIR, dataset_id)
    if not os.path.exists(path):
        return []

    return [
        f.replace(".yaml", "")
        for f in os.listdir(path)
        if f.endswith(".yaml")
    ]