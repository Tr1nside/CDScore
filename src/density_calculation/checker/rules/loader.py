import importlib
import pkgutil
from pathlib import Path

from loguru import logger


def rule_loader() -> None:
    """
    Automatically import all Python modules from the rules package.

    This function iterates through all modules in the 'rules' package
    to ensure that all rules decorated with `@rule` are registered
    within `CommentChecker`. This is typically called once upon
    the first access to `CommentChecker`.
    """
    package = "src.density_calculation.checker.rules"
    package_path = Path(__file__).parent

    logger.debug("Starting automatic rule loading from {}", package_path)

    imported_count = 0
    for module_info in pkgutil.iter_modules([package_path]):
        if module_info.name.startswith("_"):
            continue  # Skip __init__.py, __pycache__, etc.

        full_name = f"{package}.{module_info.name}"
        try:
            if full_name:
                importlib.import_module(full_name)
                imported_count += 1
                logger.debug("Loaded rule module: {}", module_info.name)
        except Exception as error:
            logger.error("Failed to load rule module {}: {}", module_info.name, error)

    logger.info("Rule loading complete. Imported {} module(s).", imported_count)
