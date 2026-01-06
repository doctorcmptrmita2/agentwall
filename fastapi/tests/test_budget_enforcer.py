"""
Budget Enforcer Tests
Tests run-level, daily, and monthly budget enforcement
"""

import pytest
from decimal import Decimal
from middleware.budget_enforcer import BudgetPolicy, BudgetEnforcer


class TestBudgetPolicy:
    """Test budget policy configuration"""
    
    def test_policy_creation(self):
        """Test creating a budget policy"""
        policy = BudgetPolicy(
            per_run_limit=10.0,
            daily_limit=100.0,
            monthly_limit=3000.0,
            alert_threshold=5.0,
        )
        
        assert policy.per_run_limit == Decimal("10.0")
        assert policy.daily_limit == Decimal("100.0")
        assert policy.monthly_limit == Decimal("3000.0")
        assert policy.alert_threshold == Decimal("5.0")
    
    def test_exceeds_per_run_limit(self):
        """Test per-run limit check"""
        policy = BudgetPolicy(per_run_limit=10.0)
        
        assert not policy.exceeds_per_run_limit(Decimal("5.0"))
        assert not policy.exceeds_per_run_limit(Decimal("10.0"))
        assert policy.exceeds_per_run_limit(Decimal("10.01"))
        assert policy.exceeds_per_run_limit(Decimal("15.0"))
    
    def test_exceeds_daily_limit(self):
        """Test daily limit check"""
        policy = BudgetPolicy(daily_limit=100.0)
        
        assert not policy.exceeds_daily_limit(Decimal("50.0"))
        assert not policy.exceeds_daily_limit(Decimal("100.0"))
        assert policy.exceeds_daily_limit(Decimal("100.01"))
    
    def test_exceeds_monthly_limit(self):
        """Test monthly limit check"""
        policy = BudgetPolicy(monthly_limit=3000.0)
        
        assert not policy.exceeds_monthly_limit(Decimal("1500.0"))
        assert not policy.exceeds_monthly_limit(Decimal("3000.0"))
        assert policy.exceeds_monthly_limit(Decimal("3000.01"))
    
    def test_should_alert(self):
        """Test alert threshold check"""
        policy = BudgetPolicy(alert_threshold=5.0)
        
        assert not policy.should_alert(Decimal("2.0"))
        assert not policy.should_alert(Decimal("5.0"))
        assert policy.should_alert(Decimal("5.01"))


class TestBudgetEnforcer:
    """Test budget enforcement"""
    
    def test_enforcer_creation(self):
        """Test creating a budget enforcer"""
        policy = BudgetPolicy(per_run_limit=10.0)
        enforcer = BudgetEnforcer(policy)
        
        assert enforcer.policy == policy
    
    def test_per_run_budget_ok(self):
        """Test per-run budget check - OK"""
        policy = BudgetPolicy(per_run_limit=10.0)
        enforcer = BudgetEnforcer(policy)
        
        result = enforcer.check_run_budget(
            run_id="run_123",
            current_cost=Decimal("5.0"),
        )
        
        assert not result["should_kill"]
        assert result["reason"] is None
        assert result["exceeded_limit"] is None
    
    def test_per_run_budget_exceeded(self):
        """Test per-run budget check - EXCEEDED"""
        policy = BudgetPolicy(per_run_limit=10.0, auto_kill_enabled=True)
        enforcer = BudgetEnforcer(policy)
        
        result = enforcer.check_run_budget(
            run_id="run_123",
            current_cost=Decimal("15.0"),
        )
        
        assert result["should_kill"]
        assert "Per-run budget exceeded" in result["reason"]
        assert result["exceeded_limit"] == "per_run"
        assert result["current_cost"] == 15.0
        assert result["limit"] == 10.0
    
    def test_daily_budget_exceeded(self):
        """Test daily budget check - EXCEEDED"""
        policy = BudgetPolicy(
            per_run_limit=50.0,  # Increase to avoid per-run limit
            daily_limit=100.0,
            auto_kill_enabled=True
        )
        enforcer = BudgetEnforcer(policy)
        
        result = enforcer.check_run_budget(
            run_id="run_123",
            current_cost=Decimal("20.0"),
            daily_spent=Decimal("85.0"),
        )
        
        assert result["should_kill"]
        assert "Daily budget exceeded" in result["reason"]
        assert result["exceeded_limit"] == "daily"
    
    def test_monthly_budget_exceeded(self):
        """Test monthly budget check - EXCEEDED"""
        policy = BudgetPolicy(
            per_run_limit=200.0,  # Increase to avoid per-run limit
            monthly_limit=3000.0,
            auto_kill_enabled=True
        )
        enforcer = BudgetEnforcer(policy)
        
        result = enforcer.check_run_budget(
            run_id="run_123",
            current_cost=Decimal("100.0"),
            monthly_spent=Decimal("2950.0"),
        )
        
        assert result["should_kill"]
        assert "Monthly budget exceeded" in result["reason"]
        assert result["exceeded_limit"] == "monthly"
    
    def test_auto_kill_disabled(self):
        """Test auto-kill disabled"""
        policy = BudgetPolicy(per_run_limit=10.0, auto_kill_enabled=False)
        enforcer = BudgetEnforcer(policy)
        
        result = enforcer.check_run_budget(
            run_id="run_123",
            current_cost=Decimal("15.0"),
        )
        
        assert not result["should_kill"]  # Not killed, just warned
        assert result["exceeded_limit"] == "per_run"
    
    def test_get_remaining_budget(self):
        """Test getting remaining budget"""
        policy = BudgetPolicy(
            daily_limit=100.0,
            monthly_limit=3000.0,
            per_run_limit=10.0,
        )
        enforcer = BudgetEnforcer(policy)
        
        remaining = enforcer.get_remaining_budget(
            daily_spent=Decimal("30.0"),
            monthly_spent=Decimal("500.0"),
        )
        
        assert remaining["daily_remaining"] == 70.0
        assert remaining["daily_spent"] == 30.0
        assert remaining["monthly_remaining"] == 2500.0
        assert remaining["monthly_spent"] == 500.0
        assert remaining["per_run_limit"] == 10.0


class TestBudgetScenarios:
    """Test realistic budget scenarios"""
    
    def test_scenario_runaway_agent(self):
        """Scenario: Agent making expensive calls"""
        policy = BudgetPolicy(
            per_run_limit=10.0,
            daily_limit=100.0,
            auto_kill_enabled=True,
        )
        enforcer = BudgetEnforcer(policy)
        
        # First call: $5 - OK
        result1 = enforcer.check_run_budget("run_1", Decimal("5.0"))
        assert not result1["should_kill"]
        
        # Second call: $8 - OK
        result2 = enforcer.check_run_budget("run_1", Decimal("8.0"))
        assert not result2["should_kill"]
        
        # Third call: $12 - KILL (exceeds per-run limit)
        result3 = enforcer.check_run_budget("run_1", Decimal("12.0"))
        assert result3["should_kill"]
        assert result3["exceeded_limit"] == "per_run"
    
    def test_scenario_daily_budget_exhaustion(self):
        """Scenario: Multiple runs exhaust daily budget"""
        policy = BudgetPolicy(
            per_run_limit=50.0,
            daily_limit=100.0,
            auto_kill_enabled=True,
        )
        enforcer = BudgetEnforcer(policy)
        
        # Run 1: $40 - OK
        result1 = enforcer.check_run_budget("run_1", Decimal("40.0"), daily_spent=Decimal("0"))
        assert not result1["should_kill"]
        
        # Run 2: $50 - OK (total $90)
        result2 = enforcer.check_run_budget("run_2", Decimal("50.0"), daily_spent=Decimal("40.0"))
        assert not result2["should_kill"]
        
        # Run 3: $20 - KILL (would be $110 total)
        result3 = enforcer.check_run_budget("run_3", Decimal("20.0"), daily_spent=Decimal("90.0"))
        assert result3["should_kill"]
        assert result3["exceeded_limit"] == "daily"
