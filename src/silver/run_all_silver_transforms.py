import sys
from pathlib import Path


project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

from src.silver.transform_customers import transform_customers_to_silver
from src.silver.transform_products import transform_products_to_silver
from src.silver.transform_stores import transform_stores_to_silver
from src.silver.transform_orders import transform_orders_to_silver
from src.silver.transform_order_items import transform_order_items_to_silver


def run_step(step_name, step_function):
    print("=" * 60)
    print(f"Running: {step_name}")

    step_function()

    print(f"Finished: {step_name}")


def run_all_silver_transforms():
    run_step("customers", transform_customers_to_silver)
    run_step("products", transform_products_to_silver)
    run_step("stores", transform_stores_to_silver)
    run_step("orders", transform_orders_to_silver)
    run_step("order_items", transform_order_items_to_silver)


if __name__ == "__main__":
    run_all_silver_transforms()