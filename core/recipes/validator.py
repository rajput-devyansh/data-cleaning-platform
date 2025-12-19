class RecipeValidationError(Exception):
    pass


SUPPORTED_ACTIONS = {
    "drop_nulls": ["column"],
    "fill_nulls": ["column", "method"],
    "remove_duplicates": ["subset"],
    "normalize_case": ["column", "case"],
}


def validate_recipe(recipe: dict, dataset_columns: list[str]):
    for idx, step in enumerate(recipe["steps"], start=1):
        if "action" not in step:
            raise RecipeValidationError(f"Step {idx}: missing action")

        action = step["action"]

        if action not in SUPPORTED_ACTIONS:
            raise RecipeValidationError(
                f"Step {idx}: unsupported action '{action}'"
            )

        for field in SUPPORTED_ACTIONS[action]:
            if field not in step:
                raise RecipeValidationError(
                    f"Step {idx}: missing field '{field}'"
                )

        # Column existence checks
        if "column" in step and step["column"] not in dataset_columns:
            raise RecipeValidationError(
                f"Step {idx}: column '{step['column']}' does not exist"
            )

        if "subset" in step:
            for col in step["subset"]:
                if col not in dataset_columns:
                    raise RecipeValidationError(
                        f"Step {idx}: column '{col}' does not exist"
                    )