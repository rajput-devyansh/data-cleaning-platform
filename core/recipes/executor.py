from core.recipes.validator import validate_recipe
from core.versioning.version_manager import VersionManager
from core.cleaning.engine import CleaningEngine
from core.schema.columns import get_dataset_columns
from core.cleaning import rules

ACTION_RULE_MAP = {
    "drop_nulls": {
        "sql": rules.drop_nulls_sql,
        "operation": "drop_nulls",
        "params": ["column"],
    },
    "fill_nulls": {
        "sql": rules.fill_nulls_sql,
        "operation": "fill_nulls",
        "params": ["column", "value"],
    },
    "remove_duplicates": {
        "sql": rules.drop_duplicates_sql,
        "operation": "remove_duplicates",
        "params": ["subset"],
    },
}

class RecipeExecutionError(Exception):
    pass

class RecipeExecutor:
    def __init__(self, dataset_id: str):
        self.dataset_id = dataset_id
        self.vm = VersionManager()
        self.engine = CleaningEngine()

    def execute(self, recipe: dict, dry_run: bool = False):
        active = self.vm.get_active_version(self.dataset_id)
        # sqlite3.Row or dict-like
        current_version = active["version"]
        dataset_columns = get_dataset_columns(
            dataset_id=self.dataset_id,
            version=current_version,
        )

        validate_recipe(recipe, dataset_columns)

        planned_steps = []

        for step in recipe["steps"]:
            action = step["action"]

            if dry_run:
                planned_steps.append(
                    {
                        "action": action,
                        "parameters": {k: v for k, v in step.items() if k != "action"},
                        "source_version": current_version,
                        "target_version": current_version + 1,
                    }
                )
                current_version += 1
                continue

            try:
                current_version = self._execute_step(
                    action,
                    step,
                    current_version,
                )
            except Exception as e:
                raise RecipeExecutionError(
                    f"Failed at action '{action}': {e}"
                )
        if dry_run:
            return planned_steps
        
        return current_version
        
    def _execute_step(self, action, params, version):
        if action not in ACTION_RULE_MAP:
            raise RecipeExecutionError(f"Unsupported action '{action}'")

        spec = ACTION_RULE_MAP[action]
        sql_builder = spec["sql"]

        # Build SQL
        if action == "drop_nulls":
            rule_sql = sql_builder(
                source_table="{source_table}",
                target_table="{target_table}",
                column=params["column"],
            )

        elif action == "fill_nulls":
            rule_sql = sql_builder(
                source_table="{source_table}",
                target_table="{target_table}",
                column=params["column"],
                value=params["value"],
            )

        elif action == "remove_duplicates":
            rule_sql = sql_builder(
                source_table="{source_table}",
                target_table="{target_table}",
                columns=params["subset"],
            )

        else:
            raise RecipeExecutionError(f"Unhandled action '{action}'")

        return self.engine.apply_rule(
            dataset_id=self.dataset_id,
            source_version=version,
            rule_sql=rule_sql,
            operation=spec["operation"],
            parameters=params,
        )