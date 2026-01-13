def estimate_carbon(page_size_kb, monthly_visitors=1000, factor=0.81):
    return round(page_size_kb * monthly_visitors * factor / 1000, 2)  # in kg/month
