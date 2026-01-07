"""
Date and time generation utilities.
"""
import random
from datetime import datetime, date, timedelta
from typing import Optional, Tuple
import numpy as np
import config


def random_date_between(start: date, end: date) -> date:
    """Generate a random date between start and end."""
    delta = (end - start).days
    random_days = random.randint(0, delta)
    return start + timedelta(days=random_days)


def random_datetime_between(start: datetime, end: datetime) -> datetime:
    """Generate a random datetime between start and end."""
    delta = (end - start).total_seconds()
    random_seconds = random.uniform(0, delta)
    return start + timedelta(seconds=random_seconds)


def avoid_weekend(target_date: date, probability: float = 0.85) -> date:
    """
    Adjust date to avoid weekends with given probability.
    
    Args:
        target_date: Original date
        probability: Probability of avoiding weekend (0-1)
        
    Returns:
        Adjusted date
    """
    if random.random() > probability:
        return target_date
        
    # If weekend, move to Monday
    weekday = target_date.weekday()
    if weekday == 5:  # Saturday
        return target_date + timedelta(days=2)
    elif weekday == 6:  # Sunday
        return target_date + timedelta(days=1)
    
    return target_date


def generate_due_date(
    created_at: datetime,
    distribution: dict,
    now: datetime = None
) -> Optional[date]:
    """
    Generate realistic due date based on distribution.
    
    Args:
        created_at: Task creation datetime
        distribution: Due date distribution config
        now: Current time (defaults to config.END_DATE)
        
    Returns:
        Due date or None
    """
    if now is None:
        now = config.END_DATE
        
    # Select bucket based on distribution
    rand = random.random()
    cumulative = 0
    
    for bucket, prob in distribution.items():
        cumulative += prob
        if rand <= cumulative:
            if bucket == 'within_1_week':
                days = random.randint(1, 7)
            elif bucket == 'within_1_month':
                days = random.randint(8, 30)
            elif bucket == 'within_3_months':
                days = random.randint(31, 90)
            elif bucket == 'no_due_date':
                return None
            elif bucket == 'overdue':
                # Due date in the past
                days = -random.randint(1, 30)
            else:
                days = random.randint(7, 30)
                
            due = created_at + timedelta(days=days)
            
            # Ensure due date doesn't exceed simulation end
            if due.date() > now.date():
                due = now - timedelta(days=random.randint(1, 7))
                
            # Avoid weekends
            return avoid_weekend(due.date(), config.WEEKEND_AVOIDANCE_RATE)
    
    # Default
    return (created_at + timedelta(days=14)).date()


def generate_completion_time(
    created_at: datetime,
    due_date: Optional[date],
    now: datetime = None
) -> datetime:
    """
    Generate realistic completion time using log-normal distribution.
    
    Based on cycle time benchmarks: median 3-7 days, with long tail.
    
    Args:
        created_at: Task creation datetime
        due_date: Task due date (if any)
        now: Current time (defaults to config.END_DATE)
        
    Returns:
        Completion datetime
    """
    if now is None:
        now = config.END_DATE
        
    # Log-normal distribution: median ~5 days, long tail
    # Parameters: mu=1.5, sigma=0.8 gives median ~4.5 days
    days_to_complete = np.random.lognormal(mean=1.5, sigma=0.8)
    
    # Clip between 1 and 14 days
    days_to_complete = max(1, min(14, days_to_complete))
    
    completed = created_at + timedelta(days=days_to_complete)
    
    # Ensure completion is after creation and before now
    if completed > now:
        completed = now - timedelta(hours=random.randint(1, 48))
        
    # If there's a due date, bias toward completing near due date
    if due_date:
        due_datetime = datetime.combine(due_date, datetime.min.time())
        # 60% chance to complete within 2 days of due date
        if random.random() < 0.6 and due_datetime < now:
            completed = due_datetime + timedelta(
                days=random.uniform(-2, 1)
            )
            # Ensure still after creation
            if completed < created_at:
                completed = created_at + timedelta(hours=random.randint(2, 48))
                
    return completed


def cluster_around_sprint_boundaries(
    created_at: datetime,
    sprint_duration: int = 14
) -> date:
    """
    Generate due dates clustered around sprint boundaries.
    
    Args:
        created_at: Task creation datetime
        sprint_duration: Sprint length in days
        
    Returns:
        Due date aligned to sprint boundary
    """
    # Find next sprint boundary
    days_since_start = (created_at.date() - config.START_DATE.date()).days
    sprints_elapsed = days_since_start // sprint_duration
    next_sprint_end = config.START_DATE.date() + timedelta(
        days=(sprints_elapsed + 1) * sprint_duration
    )
    
    # Add some variance (±2 days)
    variance = random.randint(-2, 2)
    due = next_sprint_end + timedelta(days=variance)
    
    return avoid_weekend(due)


def generate_created_at(
    start: datetime,
    end: datetime,
    weekday_bias: bool = True
) -> datetime:
    """
    Generate creation timestamp with realistic patterns.
    
    Higher creation rates Mon-Wed, lower Thu-Fri.
    
    Args:
        start: Start of time range
        end: End of time range
        weekday_bias: Whether to bias toward weekdays
        
    Returns:
        Creation datetime
    """
    created = random_datetime_between(start, end)
    
    if weekday_bias:
        # Bias toward Mon-Wed (60% of tasks)
        if random.random() < 0.6:
            # Find a Mon-Wed in the range
            while created.weekday() not in [0, 1, 2]:
                created = random_datetime_between(start, end)
                
    # Set time to business hours (9 AM - 6 PM)
    hour = random.randint(9, 18)
    minute = random.randint(0, 59)
    created = created.replace(hour=hour, minute=minute, second=0, microsecond=0)
    
    return created


def is_overdue(due_date: Optional[date], now: datetime = None) -> bool:
    """Check if a task is overdue."""
    if now is None:
        now = config.END_DATE
    if due_date is None:
        return False
    return due_date < now.date()


def generate_modified_at(
    created_at: datetime,
    completed_at: Optional[datetime],
    now: datetime = None
) -> datetime:
    """
    Generate last modified timestamp.
    
    Args:
        created_at: Creation time
        completed_at: Completion time (if completed)
        now: Current time
        
    Returns:
        Last modified datetime
    """
    if now is None:
        now = config.END_DATE
        
    if completed_at:
        # Modified at completion time
        return completed_at
    else:
        # Random time between creation and now
        if (now - created_at).days > 1:
            return random_datetime_between(created_at, now)
        else:
            return created_at