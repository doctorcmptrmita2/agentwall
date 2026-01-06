"""
Budget Enforcement Middleware
Enforces run-level, daily, and monthly budget limits
"""

import logging
from typing import Optional
from decimal import Decimal
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class BudgetPolicy:
    """Budget policy configuration"""
    
    def __init__(
        self,
        per_run_limit: float = 10.0,
        daily_limit: float = 100.0,
        monthly_limit: float = 3000.0,
        alert_threshold: float = 5.0,
        auto_kill_enabled: bool = True,
    ):
        self.per_run_limit = Decimal(str(per_run_limit))
        self.daily_limit = Decimal(str(daily_limit))
        self.monthly_limit = Decimal(str(monthly_limit))
        self.alert_threshold = Decimal(str(alert_threshold))
        self.auto_kill_enabled = auto_kill_enabled

    def exceeds_per_run_limit(self, cost: Decimal) -> bool:
        """Check if cost exceeds per-run limit"""
        return cost > self.per_run_limit

    def exceeds_daily_limit(self, daily_spent: Decimal) -> bool:
        """Check if daily spending exceeds limit"""
        return daily_spent > self.daily_limit

    def exceeds_monthly_limit(self, monthly_spent: Decimal) -> bool:
        """Check if monthly spending exceeds limit"""
        return monthly_spent > self.monthly_limit

    def should_alert(self, cost: Decimal) -> bool:
        """Check if cost exceeds alert threshold"""
        return cost > self.alert_threshold


class BudgetEnforcer:
    """Enforces budget policies on agent runs"""

    def __init__(self, policy: Optional[BudgetPolicy] = None):
        self.policy = policy or BudgetPolicy()
        self.run_costs = {}  # run_id -> cost
        self.daily_costs = {}  # date -> total_cost
        self.monthly_costs = {}  # month -> total_cost

    def check_run_budget(
        self,
        run_id: str,
        current_cost: Decimal,
        daily_spent: Decimal = Decimal("0"),
        monthly_spent: Decimal = Decimal("0"),
    ) -> dict:
        """
        Check if run should be killed based on budget
        
        Returns:
            {
                "should_kill": bool,
                "reason": str,
                "exceeded_limit": str (per_run|daily|monthly),
                "current_cost": float,
                "limit": float,
            }
        """
        
        # Check per-run limit
        if self.policy.exceeds_per_run_limit(current_cost):
            logger.warning(
                f"Run {run_id} exceeded per-run budget: "
                f"${current_cost} > ${self.policy.per_run_limit}"
            )
            return {
                "should_kill": self.policy.auto_kill_enabled,
                "reason": f"Per-run budget exceeded: ${current_cost} > ${self.policy.per_run_limit}",
                "exceeded_limit": "per_run",
                "current_cost": float(current_cost),
                "limit": float(self.policy.per_run_limit),
            }

        # Check daily limit
        if self.policy.exceeds_daily_limit(daily_spent + current_cost):
            logger.warning(
                f"Run {run_id} would exceed daily budget: "
                f"${daily_spent + current_cost} > ${self.policy.daily_limit}"
            )
            return {
                "should_kill": self.policy.auto_kill_enabled,
                "reason": f"Daily budget exceeded: ${daily_spent + current_cost} > ${self.policy.daily_limit}",
                "exceeded_limit": "daily",
                "current_cost": float(current_cost),
                "limit": float(self.policy.daily_limit),
            }

        # Check monthly limit
        if self.policy.exceeds_monthly_limit(monthly_spent + current_cost):
            logger.warning(
                f"Run {run_id} would exceed monthly budget: "
                f"${monthly_spent + current_cost} > ${self.policy.monthly_limit}"
            )
            return {
                "should_kill": self.policy.auto_kill_enabled,
                "reason": f"Monthly budget exceeded: ${monthly_spent + current_cost} > ${self.policy.monthly_limit}",
                "exceeded_limit": "monthly",
                "current_cost": float(current_cost),
                "limit": float(self.policy.monthly_limit),
            }

        # All checks passed
        return {
            "should_kill": False,
            "reason": None,
            "exceeded_limit": None,
            "current_cost": float(current_cost),
            "limit": None,
        }

    def get_remaining_budget(
        self,
        daily_spent: Decimal = Decimal("0"),
        monthly_spent: Decimal = Decimal("0"),
    ) -> dict:
        """Get remaining budget for today and this month"""
        return {
            "daily_remaining": float(self.policy.daily_limit - daily_spent),
            "daily_limit": float(self.policy.daily_limit),
            "daily_spent": float(daily_spent),
            "monthly_remaining": float(self.policy.monthly_limit - monthly_spent),
            "monthly_limit": float(self.policy.monthly_limit),
            "monthly_spent": float(monthly_spent),
            "per_run_limit": float(self.policy.per_run_limit),
        }


# Global budget enforcer instance
budget_enforcer = BudgetEnforcer()
