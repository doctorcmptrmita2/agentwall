"""
Public Status Page for AgentWall API

Endpoint: /status
Shows real-time system health for public visibility

Performance: Cached results, <50ms response
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from datetime import datetime, timedelta
import asyncio
import logging

from config import settings
from api.v1.health import _check_dependencies

logger = logging.getLogger(__name__)
router = APIRouter()

# Track uptime
_start_time = datetime.utcnow()


def _get_uptime() -> dict:
    """Calculate uptime since service start"""
    now = datetime.utcnow()
    delta = now - _start_time
    
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    return {
        "started_at": _start_time.isoformat() + "Z",
        "uptime_seconds": int(delta.total_seconds()),
        "uptime_human": f"{days}d {hours}h {minutes}m {seconds}s"
    }


def _status_badge(status: str) -> str:
    """Return colored badge HTML for status"""
    colors = {
        "healthy": ("bg-green-500", "Operational"),
        "configured": ("bg-green-500", "Configured"),
        "degraded": ("bg-yellow-500", "Degraded"),
        "unhealthy": ("bg-red-500", "Down"),
        "unconfigured": ("bg-gray-500", "Not Configured"),
    }
    color, label = colors.get(status, ("bg-gray-500", status))
    return f'<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium {color} text-white">{label}</span>'


def _service_row(name: str, icon: str, check: dict) -> str:
    """Generate HTML row for a service"""
    status = check.get("status", "unknown")
    badge = _status_badge(status)
    error = check.get("error", "")
    error_html = f'<p class="text-sm text-gray-500 mt-1">{error}</p>' if error else ""
    
    return f'''
    <div class="flex items-center justify-between p-4 bg-white rounded-lg shadow-sm border border-gray-100">
        <div class="flex items-center space-x-3">
            <span class="text-2xl">{icon}</span>
            <div>
                <h3 class="font-medium text-gray-900">{name}</h3>
                {error_html}
            </div>
        </div>
        {badge}
    </div>
    '''


@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
async def status_page(request: Request):
    """
    Public status page showing system health
    Beautiful HTML page with real-time status
    """
    # Get health checks
    checks = await _check_dependencies(force=False)
    uptime = _get_uptime()
    
    # Calculate overall status
    statuses = [c.get("status") for c in checks.values()]
    if all(s in ["healthy", "configured"] for s in statuses):
        overall_status = "operational"
        overall_color = "text-green-600"
        overall_bg = "bg-green-50"
        overall_icon = "✅"
    elif any(s == "unhealthy" for s in statuses):
        overall_status = "partial outage"
        overall_color = "text-red-600"
        overall_bg = "bg-red-50"
        overall_icon = "❌"
    else:
        overall_status = "degraded"
        overall_color = "text-yellow-600"
        overall_bg = "bg-yellow-50"
        overall_icon = "⚠️"
    
    # Build service rows
    services_html = ""
    services_html += _service_row("AgentWall API", "🛡️", {"status": "healthy"})
    services_html += _service_row("Redis (Run Tracking)", "🔴", checks.get("redis", {}))
    services_html += _service_row("ClickHouse (Analytics)", "📊", checks.get("clickhouse", {}))
    services_html += _service_row("OpenAI Connection", "🤖", checks.get("openai", {}))
    
    html = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AgentWall Status</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🛡️</text></svg>">
    <meta http-equiv="refresh" content="30">
</head>
<body class="bg-gray-50 min-h-screen">
    <div class="max-w-2xl mx-auto py-12 px-4">
        <!-- Header -->
        <div class="text-center mb-8">
            <h1 class="text-3xl font-bold text-gray-900 flex items-center justify-center gap-2">
                🛡️ AgentWall Status
            </h1>
            <p class="text-gray-500 mt-2">Guard the Agent, Save the Budget</p>
        </div>
        
        <!-- Overall Status -->
        <div class="{overall_bg} rounded-xl p-6 mb-8 text-center">
            <div class="text-4xl mb-2">{overall_icon}</div>
            <h2 class="text-2xl font-bold {overall_color} capitalize">{overall_status}</h2>
            <p class="text-gray-600 mt-1">All systems are functioning normally</p>
        </div>
        
        <!-- Uptime -->
        <div class="bg-white rounded-lg shadow-sm border border-gray-100 p-4 mb-6">
            <div class="flex justify-between items-center">
                <span class="text-gray-600">Uptime</span>
                <span class="font-mono text-gray-900">{uptime['uptime_human']}</span>
            </div>
        </div>
        
        <!-- Services -->
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Services</h3>
        <div class="space-y-3">
            {services_html}
        </div>
        
        <!-- Footer -->
        <div class="mt-8 text-center text-sm text-gray-500">
            <p>Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC</p>
            <p class="mt-1">Auto-refreshes every 30 seconds</p>
            <p class="mt-4">
                <a href="https://api.agentwall.io/docs" class="text-blue-600 hover:underline">API Documentation</a>
                &nbsp;•&nbsp;
                <a href="https://api.agentwall.io/status/json" class="text-blue-600 hover:underline">Status JSON</a>
                &nbsp;•&nbsp;
                <a href="https://agentwall.io/admin" class="text-blue-600 hover:underline">Dashboard</a>
            </p>
        </div>
    </div>
</body>
</html>
'''
    return HTMLResponse(content=html)


@router.get("/json")
async def status_json():
    """
    Status page data as JSON
    For programmatic access and monitoring tools
    """
    checks = await _check_dependencies(force=False)
    uptime = _get_uptime()
    
    # Calculate overall status
    statuses = [c.get("status") for c in checks.values()]
    if all(s in ["healthy", "configured"] for s in statuses):
        overall = "operational"
    elif any(s == "unhealthy" for s in statuses):
        overall = "partial_outage"
    else:
        overall = "degraded"
    
    return {
        "status": overall,
        "uptime": uptime,
        "services": {
            "api": {"status": "healthy", "name": "AgentWall API"},
            "redis": {**checks.get("redis", {}), "name": "Redis (Run Tracking)"},
            "clickhouse": {**checks.get("clickhouse", {}), "name": "ClickHouse (Analytics)"},
            "openai": {**checks.get("openai", {}), "name": "OpenAI Connection"},
        },
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
