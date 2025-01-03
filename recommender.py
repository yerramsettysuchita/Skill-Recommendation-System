import json
from math import sqrt
from typing import List, Dict, Tuple, Callable

# Load the dataset
dataFrame = json.load(open("1000DATASET.json"))

def sim_distance(reqirements_json: Dict, prefs: Dict, person1: str, person2: str) -> float:
    """Calculate the Euclidean distance-based similarity score."""
    shared_items = {
        item: 1 for item in reqirements_json[person1] if item in prefs[person2]
    }

    if len(shared_items) == 0:
        return 0

    sum_of_squares = sum(
        (reqirements_json[person1][item] - prefs[person2][item]) ** 2
        for item in shared_items
    )
    return 1 / (1 + sqrt(sum_of_squares))

def sim_pearson(reqirements_json: Dict, prefs: Dict, person1: str, person2: str) -> float:
    """Calculate Pearson correlation coefficient for similarity."""
    shared_items = {
        item: 1 for item in reqirements_json[person1] if item in prefs[person2]
    }

    if len(shared_items) == 0:
        return 0

    n = len(shared_items)

    sum1 = sum(reqirements_json[person1][item] for item in shared_items)
    sum2 = sum(prefs[person2][item] for item in shared_items)

    sum1_sq = sum(reqirements_json[person1][item] ** 2 for item in shared_items)
    sum2_sq = sum(prefs[person2][item] ** 2 for item in shared_items)

    p_sum = sum(
        reqirements_json[person1][item] * prefs[person2][item] for item in shared_items
    )

    num = p_sum - (sum1 * sum2 / n)
    den = sqrt((sum1_sq - (sum1 ** 2) / n) * (sum2_sq - (sum2 ** 2) / n))
    if den == 0:
        return 0

    return num / den

def topMatches(
    reqirements_json: Dict,
    prefs: Dict,
    person: str,
    n: int,
    similarity: Callable[[Dict, Dict, str, str], float] = sim_distance,
) -> List[Tuple[float, str]]:
    """Return the top n matches for a given person."""
    scores = [
        (similarity(reqirements_json, prefs, person, other), other)
        for other in prefs
        if other != person
    ]
    scores.sort(reverse=True)
    return scores[:n]
