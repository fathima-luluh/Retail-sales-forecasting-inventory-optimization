import numpy as np
from scipy.stats import norm

def calculate_inventory(forecast, std, lead_time):
    import numpy as np

    forecast = list(forecast)  # safety

    demand = sum(forecast[:int(lead_time)])

    z = 1.65  # 95% service level
    safety_stock = z * std * (lead_time ** 0.5)

    reorder_point = demand + safety_stock

    return safety_stock, reorder_point