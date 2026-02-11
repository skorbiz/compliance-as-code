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
    review_date = _load_review_date()
    today = date.today()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        if today > review_date:
            warnings.warn(
                f"Risk assessment review overdue (was due {review_date.isoformat()}).",
                UserWarning,
            )
            assert len(caught) == 1
            assert "review overdue" in str(caught[0].message)
        else:
            assert len(caught) == 0
