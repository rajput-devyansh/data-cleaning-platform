import yaml


class RecipeLoadError(Exception):
    pass


def load_recipe(path: str) -> dict:
    try:
        with open(path, "r") as f:
            recipe = yaml.safe_load(f)
    except Exception as e:
        raise RecipeLoadError(f"Failed to load recipe: {e}")

    if not isinstance(recipe, dict):
        raise RecipeLoadError("Recipe must be a YAML mapping")

    if "steps" not in recipe or not isinstance(recipe["steps"], list):
        raise RecipeLoadError("Recipe must contain a list of steps")

    return recipe