#!/usr/bin/env python3
"""
Quick runner for AgentWall Benchmark Suite
Standalone script that can be run from anywhere
"""

import asyncio
import sys
from pathlib import Path

# Add paths
root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root))
sys.path.insert(0, str(Path(__file__).parent))

from benchmark_suite import AgentWallBenchmark


async def run():
    print("🚀 Starting AgentWall Production Readiness Benchmark...")
    print("=" * 60)
    
    benchmark = AgentWallBenchmark()
    report = await benchmark.run_all()
    benchmark.print_summary(report)
    benchmark.save_report(report)
    
    return report.production_ready


if __name__ == "__main__":
    result = asyncio.run(run())
    sys.exit(0 if result else 1)
