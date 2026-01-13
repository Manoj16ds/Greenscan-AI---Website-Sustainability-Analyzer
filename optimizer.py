# optimizer.py

def simulate_optimization(page_size_kb, image_count):
    # Estimate optimization potential
    # Example: Assume we can reduce image size by 40% and page scripts by 20%

    image_contribution = page_size_kb * 0.6  # assume images are ~60% of page size
    other_contribution = page_size_kb * 0.4

    optimized_image_size = image_contribution * 0.6  # 40% reduction
    optimized_other_size = other_contribution * 0.8  # 20% reduction

    optimized_total = round(optimized_image_size + optimized_other_size, 2)
    return optimized_total
