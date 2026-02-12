from datetime import date
import warnings

import yaml

from schemas import RiskRegister


def _load_review_date() -> date:
    with open("data/risks.yaml") as f:
        data = yaml.safe_load(f)
    register = RiskRegister.model_validate(data)
    return register.metadata.review_date


def test_review_schedule_warns_if_overdue():
    """Test always passes but emits a warning if review date has passed."""
    review_date = _load_review_date()
    today = date.today()
    
    if today > review_date:
        days_overdue = (today - review_date).days
        warnings.warn(
            f"⚠️  Risk assessment review is {days_overdue} days overdue! "
            f"Was due: {review_date.isoformat()}",
            UserWarning,
        )
    # Test always passes - warning is just for visibility
