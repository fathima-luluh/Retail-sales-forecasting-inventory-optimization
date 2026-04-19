import numpy as np
from scipy.stats import norm

def calculate_inventory(forecast, std, lead_time=7, service_level=0.95):
    z = norm.ppf(service_level)

    demand = sum(forecast[:lead_time])
    safety_stock = z * std * np.sqrt(lead_time)

    reorder_point = demand + safety_stock

    return safety_stock, reorder_point