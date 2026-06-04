#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║     RJ TECH ULTIMATE - MAIN LAUNCHER                              ║
║     The Most Powerful Autonomous AI System                         ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

import sys
import time
from datetime import datetime

BANNER = """
╔════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                    ║
║     ██████╗ ███████╗██████╗ ███████╗██╗████████╗███████╗                           ║
║     ██╔══██╗██╔════╝██╔══██╗██╔════╝██║╚══██╔══╝██╔════╝                           ║
║     ██████╔╝█████╗  ██████╔╝█████╗  ██║   ██║   █████╗                             ║
║     ██╔══██╗██╔══╝  ██╔══██╗██╔══╝  ██║   ██║   ██╔══╝                             ║
║     ██║  ██║███████╗██║  ██║███████╗██║   ██║   ███████╗                           ║
║     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝   ╚═╝   ╚══════╝                           ║
║                                                                                    ║
║           RJ TECH ULTIMATE SUPREME INTELLIGENCE CIVILIZATION                            ║
║                                                                                    ║
║                    VERSION: 1.0.0-SUPREME-MEGA-ULTIMATE                             ║
║                    POWER LEVEL: INFINITE (∞)                                           ║
║                    STATUS: GOD-MODE-ACTIVATED                                          ║
║                                                                                    ║
╚════════════════════════════════════════════════════════════════════════════════════════════╝
"""

def print_banner():
    print(BANNER)
    print(f"  🚀 Starting at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

def run_module(module: str):
    print_banner()
    
    modules = {
        'media': ('media_engine', 'RJ TECH MEDIA ENGINE'),
        'agent': ('agent_system', 'Agent System'),
        'security': ('security_system', 'Security System'),
        'revenue': ('revenue_engine', 'Revenue Engine'),
        'customer': ('customer_system', 'Customer System'),
        'dashboard': ('founder_command_center', 'Founder Dashboard'),
        'router': ('model_router', 'Model Router'),
        'control': ('control_systems', 'Voice & Text Control'),
        'supreme': ('rjtech_supreme', 'RJ TECH SUPREME'),
    }
    
    if module == 'media':
        print("  ⚙️  Loading RJ TECH MEDIA ENGINE...\n")
        try:
            from media_engine import RJTechMediaEngine
            engine = RJTechMediaEngine()
            engine.run()
        except ImportError as e:
            print(f"  ❌ Error: {e}")
            print("  Make sure media_engine.py exists")
        return
    
    if module not in modules:
        print(f"  ❌ Unknown module: {module}")
        print(f"  Available: {', '.join(modules.keys())}")
        return
    
    print(f"  ⚙️  Loading {modules[module][1]}...")
    try:
        from importlib import import_module
        mod = import_module(modules[module][0])
        if hasattr(mod, 'demo'):
            mod.demo()
        else:
            print(f"  ✓ {modules[module][1]} loaded")
    except ImportError as e:
        print(f"  ❌ Error: {e}")

def main():
    if len(sys.argv) <= 1:
        print_banner()
        print("""

╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║                    RJ TECH ULTIMATE - COMMAND CENTER                  ║
║                                                                      ║
║  Usage: python3 run.py [OPTION]                                       ║
║                                                                      ║
║  OPTIONS:                                                            ║
║                                                                      ║
║    --media       🚀 MEDIA ENGINE (RECOMMENDED)                       ║
║                   Collects ALL News | You Choose | Auto-Publish        ║
║                   24/7 Continuous Operation                         ║
║                                                                      ║
║    --control     🎙️ Voice & Text Control + 21-Layer Security         ║
║                                                                      ║
║    --supreme     🌟 RJ TECH SUPREME - Everything Included             ║
║                                                                      ║
║    --agent       🤖 Agent System Demo                                ║
║                                                                      ║
║    --security    🛡️  Security System Demo                           ║
║                                                                      ║
║    --revenue     💰 Revenue Engine Demo                              ║
║                                                                      ║
║    --customer    👥 Customer System Demo                             ║
║                                                                      ║
║    --dashboard   📊 Founder Dashboard                                ║
║                                                                      ║
║    --router      🔀 Model Router Demo                                ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

For full media engine with founder selection:
    python3 run.py --media

""")
    else:
        arg = sys.argv[1].lower()
        if arg.startswith('--'):
            run_module(arg[2:])
        else:
            print("Usage: python3 run.py --media")

if __name__ == "__main__":
    main()