from datetime import date
import warnings

import yaml

from model.schemas import RiskRegister


def _load_review_date() -> date:
    with open("model/risks.yaml") as f:
        data = yaml.safe_load(f)
    register = RiskRegister.model_validate(data)
    return register.metadata.review_date


def test_review_schedule_warns_if_overdue():
    """Test always passes but emits a warning if review date has passed (or unset)."""
    review_date = _load_review_date()

    if review_date is None:
        warnings.warn("\u26a0\ufe0f  Risk assessment has no review_date set yet.", UserWarning)
        return

    today = date.today()
    if today > review_date:
        days_overdue = (today - review_date).days
        warnings.warn(
            f"⚠️  Risk assessment review is {days_overdue} days overdue! "
            f"Was due: {review_date.isoformat()}",
            UserWarning,
        )
    # Test always passes - warning is just for visibility
