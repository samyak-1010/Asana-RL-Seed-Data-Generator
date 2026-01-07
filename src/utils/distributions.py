"""
Statistical distribution utilities for realistic data generation.
"""
import random
import numpy as np
from typing import List, Dict, Tuple


def pareto_distribution(
    items: List,
    ratio: float = 0.8,
    top_percentage: float = 0.2
) -> Dict:
    """
    Apply Pareto principle (80/20 rule) to distribute weights.
    
    Args:
        items: List of items to weight
        ratio: Ratio of total weight for top items (default 0.8)
        top_percentage: Percentage of items in top group (default 0.2)
        
    Returns:
        Dictionary mapping items to weights
    """
    n = len(items)
    n_top = max(1, int(n * top_percentage))
    
    # Shuffle to randomize which items are "top"
    shuffled = items.copy()
    random.shuffle(shuffled)
    
    # Assign weights
    weights = {}
    top_items = shuffled[:n_top]
    bottom_items = shuffled[n_top:]
    
    # Top items get 'ratio' of total weight
    top_weight_each = ratio / n_top if n_top > 0 else 0
    for item in top_items:
        weights[item] = top_weight_each
        
    # Bottom items share remaining weight
    bottom_weight_each = (1 - ratio) / len(bottom_items) if bottom_items else 0
    for item in bottom_items:
        weights[item] = bottom_weight_each
        
    return weights


def weighted_choice(items: List, weights: List[float]):
    """
    Choose item based on weights.
    
    Args:
        items: List of items
        weights: List of weights (must sum to 1)
        
    Returns:
        Chosen item
    """
    return random.choices(items, weights=weights, k=1)[0]


def weighted_sample(items: List, weights: List[float], k: int) -> List:
    """
    Sample k items with replacement based on weights.
    
    Args:
        items: List of items
        weights: List of weights
        k: Number of items to sample
        
    Returns:
        List of sampled items
    """
    return random.choices(items, weights=weights, k=k)


def normal_distribution_int(
    mean: float,
    std: float,
    min_val: int = None,
    max_val: int = None
) -> int:
    """
    Generate integer from normal distribution with optional bounds.
    
    Args:
        mean: Mean value
        std: Standard deviation
        min_val: Minimum value (inclusive)
        max_val: Maximum value (inclusive)
        
    Returns:
        Random integer
    """
    value = int(np.random.normal(mean, std))
    
    if min_val is not None:
        value = max(min_val, value)
    if max_val is not None:
        value = min(max_val, value)
        
    return value


def exponential_distribution(
    scale: float,
    min_val: float = None,
    max_val: float = None
) -> float:
    """
    Generate value from exponential distribution with optional bounds.
    
    Args:
        scale: Scale parameter (1/lambda)
        min_val: Minimum value
        max_val: Maximum value
        
    Returns:
        Random float
    """
    value = np.random.exponential(scale)
    
    if min_val is not None:
        value = max(min_val, value)
    if max_val is not None:
        value = min(max_val, value)
        
    return value


def power_law_distribution(
    n: int,
    alpha: float = 2.5
) -> List[float]:
    """
    Generate power law distribution (e.g., for team sizes).
    
    Args:
        n: Number of samples
        alpha: Power law exponent (higher = more unequal)
        
    Returns:
        List of values following power law
    """
    # Generate using inverse transform sampling
    u = np.random.uniform(0, 1, n)
    values = (1 - u) ** (-1 / (alpha - 1))
    
    # Normalize to sum to 1
    values = values / values.sum()
    
    return values.tolist()


def zipf_distribution(n: int, s: float = 1.5) -> List[float]:
    """
    Generate Zipf distribution (e.g., for task assignment).
    
    Args:
        n: Number of items
        s: Distribution parameter (higher = more skewed)
        
    Returns:
        List of probabilities
    """
    ranks = np.arange(1, n + 1)
    frequencies = 1 / (ranks ** s)
    probabilities = frequencies / frequencies.sum()
    return probabilities.tolist()


def beta_distribution(
    alpha: float,
    beta: float,
    size: int = 1
) -> float or List[float]:
    """
    Generate value(s) from beta distribution.
    
    Useful for percentages/rates between 0 and 1.
    
    Args:
        alpha: Alpha parameter
        beta: Beta parameter
        size: Number of samples
        
    Returns:
        Single value or list of values
    """
    values = np.random.beta(alpha, beta, size)
    return float(values[0]) if size == 1 else values.tolist()


def pick_from_distribution(distribution: Dict[str, float]) -> str:
    """
    Pick an item based on a probability distribution.
    
    Args:
        distribution: Dictionary mapping items to probabilities
        
    Returns:
        Chosen item
    """
    items = list(distribution.keys())
    probs = list(distribution.values())
    return random.choices(items, weights=probs, k=1)[0]


def assign_by_capacity(
    items: List,
    capacity_dict: Dict,
    total_needed: int
) -> Dict:
    """
    Assign items to recipients based on capacity.
    
    Args:
        items: Items to assign
        capacity_dict: Dictionary mapping recipients to capacity
        total_needed: Total number of assignments needed
        
    Returns:
        Dictionary mapping recipients to assigned items
    """
    assignments = {k: [] for k in capacity_dict.keys()}
    
    # Normalize capacities to probabilities
    total_capacity = sum(capacity_dict.values())
    probs = [capacity_dict[k] / total_capacity for k in capacity_dict.keys()]
    
    # Assign items
    recipients = list(capacity_dict.keys())
    for _ in range(total_needed):
        if not items:
            break
        item = items.pop(0)
        recipient = weighted_choice(recipients, probs)
        assignments[recipient].append(item)
        
    return assignments


def generate_realistic_percentages(
    n_categories: int,
    target_mean: float = None,
    variance: float = 0.1
) -> List[float]:
    """
    Generate realistic percentages that sum to 1.
    
    Args:
        n_categories: Number of categories
        target_mean: Target mean percentage (default 1/n)
        variance: Variance in distribution
        
    Returns:
        List of percentages summing to 1
    """
    if target_mean is None:
        target_mean = 1.0 / n_categories
        
    # Generate from Dirichlet distribution for realistic variation
    alpha = [1/variance] * n_categories
    percentages = np.random.dirichlet(alpha).tolist()
    
    return percentages