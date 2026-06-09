import math

def calculate_drone_metrics(area_acres, spray_type, tank_capacity, speed_mps, battery_ah):
    """
    Computes precise spraying flight mechanics, refills, and metrics.
    """
    # Resource consumption configurations per acre
    spray_configs = {
        "Pesticide": {"volume_per_acre": 15, "cost_per_liter": 12.5},   # Liters
        "Fertilizer": {"volume_per_acre": 25, "cost_per_liter": 6.0},  # Liters
        "Water": {"volume_per_acre": 50, "cost_per_liter": 0.5}        # Liters
    }
    
    config = spray_configs.get(spray_type, spray_configs["Water"])
    total_volume_needed = area_acres * config["volume_per_acre"]
    
    # Drone Flight Calculation Simulations
    # Assumed standard swath width = 5 meters (~16.4 feet)
    swath_width = 5 
    sq_meters_per_acre = 4046.86
    total_area_sqm = area_acres * sq_meters_per_acre
    
    # Flight path distance
    flight_distance_m = total_area_sqm / swath_width
    flight_time_sec = flight_distance_m / speed_mps
    flight_time_min = flight_time_sec / 60
    
    # Refill logistics
    num_refills = math.ceil(total_volume_needed / tank_capacity) - 1
    if num_refills < 0: num_refills = 0
        
    # Battery consumption simulation based on capacity (Ah) and flight load time
    # Baseline power drain model
    base_drain_per_min = 1.5 # Ah per minute flight
    total_battery_consumed = flight_time_min * base_drain_per_min
    batteries_required = math.ceil(total_battery_consumed / (battery_ah * 0.8)) # 80% safety margin
    
    # Financial projections
    resource_cost = total_volume_needed * config["cost_per_liter"]
    operational_cost = (flight_time_min * 2.5) + (num_refills * 15) # Energy costs + labor delay factor
    total_cost = resource_cost + operational_cost
    
    # Traditional comparisons models
    traditional_water_per_acre = config["volume_per_acre"] * 3.5 # Flood / Boom systems waste more
    traditional_time_per_acre = 45 # Minutes per acre manually
    traditional_cost_per_acre = (config["cost_per_liter"] * traditional_water_per_acre) + 35
    
    trad_total_water = traditional_water_per_acre * area_acres
    trad_total_time = traditional_time_per_acre * area_acres
    trad_total_cost = traditional_cost_per_acre * area_acres

    return {
        "total_volume": round(total_volume_needed, 2),
        "flight_distance_km": round(flight_distance_m / 1000, 2),
        "flight_time_min": round(flight_time_min, 1),
        "refills": num_refills,
        "batteries": batteries_required,
        "drone_cost": round(total_cost, 2),
        "savings_water": round(((trad_total_water - total_volume_needed)/trad_total_water)*100, 1) if spray_type == "Water" else 40.0,
        "savings_time": round(((trad_total_time - flight_time_min)/trad_total_time)*100, 1),
        "savings_cost": round(((trad_total_cost - total_cost)/trad_total_cost)*100, 1),
        "trad_water": round(trad_total_water, 2),
        "trad_time": round(trad_total_time, 1),
        "trad_cost": round(trad_total_cost, 2)
    }
