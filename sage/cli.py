#!/usr/bin/env python3
"""
MAXIMUS Personal Assistant - CLI Interface
===========================================

Command-line interface for the TRUE AI Personal Assistant

Usage:
    sage                  # Interactive mode
    sage --version        # Show version
    sage --help           # Show help
    mpa                         # Short alias
"""

import os
import sys
import asyncio
import argparse
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from sage.core.maximus_pa import Sage


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="MAXIMUS Personal Assistant - TRUE AI PA",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    sage                      # Start interactive mode
    sage --status             # Show status only
    sage --execute roadmap.md # Execute roadmap

Environment Variables:
    ANTHROPIC_API_KEY     - Required: Anthropic API key
    CLICKUP_API_TOKEN     - Optional: ClickUp API token
    MAXIMUS_CORE_URL      - Optional: MAXIMUS Core URL (default: http://localhost:8150)
    MABA_URL              - Optional: MABA URL (default: http://localhost:8152)
    GITHUB_USERNAME       - Optional: GitHub username (default: JuanCS-Dev)

For more information, see: docs/QUICKSTART.md
        """
    )

    parser.add_argument(
        "--version",
        action="version",
        version="MAXIMUS Personal Assistant v2.0.0"
    )

    parser.add_argument(
        "--status",
        action="store_true",
        help="Show status and exit"
    )

    parser.add_argument(
        "--execute",
        metavar="ROADMAP",
        help="Execute a roadmap file"
    )

    parser.add_argument(
        "--performance",
        action="store_true",
        help="Show performance metrics and exit"
    )

    parser.add_argument(
        "--api-key",
        help="Anthropic API key (overrides env var)"
    )

    parser.add_argument(
        "--clickup-token",
        help="ClickUp API token (overrides env var)"
    )

    parser.add_argument(
        "--github-user",
        help="GitHub username (overrides env var)"
    )

    return parser.parse_args()


async def main():
    """Main CLI entry point"""

    args = parse_args()

    # Print header
    print("\n" + "="*75)
    print("🧠 MAXIMUS PERSONAL ASSISTANT - TRUE AI PA v2.0")
    print("="*75)
    print("\n✨ Consciência + Desempenho + Execução Autônoma\n")

    # Load credentials
    api_key = args.api_key or os.getenv("ANTHROPIC_API_KEY")
    clickup_token = args.clickup_token or os.getenv(
        "CLICKUP_API_TOKEN",
        "pk_242682821_6R1EU8ILGDZWKS76401IW32JSJCLYUHN"
    )
    github_username = args.github_user or os.getenv("GITHUB_USERNAME", "JuanCS-Dev")
    core_url = os.getenv("MAXIMUS_CORE_URL", "http://localhost:8150")
    maba_url = os.getenv("MABA_URL", "http://localhost:8152")

    if not api_key:
        print("❌ ANTHROPIC_API_KEY não configurada!")
        print("\nConfigure com:")
        print("    export ANTHROPIC_API_KEY='sua-key-aqui'\n")
        sys.exit(1)

    # Initialize assistant
    print("🔄 Inicializando MAXIMUS Personal Assistant...")
    assistant = Sage(
        api_key,
        clickup_token,
        github_username,
        core_url,
        maba_url
    )

    # Show status
    status = await assistant.get_status()
    print(f"\n✅ {status['agent']} inicializado!")
    print(f"\n🧠 Consciência: {'✅ ATIVA' if status['consciousness']['enabled'] else '❌ INATIVA'}")
    print(f"   Core disponível: {'✅' if status['consciousness']['core_available'] else '❌'}")
    print(f"\n🔌 Integrações:")
    print(f"   ClickUp: {'✅' if status['integrations']['clickup'] else '❌'}")
    print(f"   GitHub: {'✅' if status['integrations']['github'] else '❌'}")
    print(f"   MABA: {'✅' if status['integrations']['maba'] else '❌'}")
    print(f"   Core: {'✅' if status['integrations']['core'] else '❌'}")

    # Handle command-line modes
    if args.status:
        import json
        print(f"\n{json.dumps(status, indent=2)}\n")
        await assistant.close()
        return

    if args.performance:
        perf = assistant.performance.get_report()
        print(f"\n📊 Performance Report:")
        print(f"   Tasks: {perf['tasks_completed']} completed, {perf['tasks_failed']} failed")
        print(f"   Success Rate: {perf['success_rate']}")
        print(f"   Avg Task Time: {perf['avg_task_time']}")
        print(f"   Consciousness Checks: {perf['consciousness_checks']['passed']} passed, {perf['consciousness_checks']['failed']} failed")
        print()
        await assistant.close()
        return

    if args.execute:
        roadmap_path = args.execute
        if not os.path.exists(roadmap_path):
            print(f"\n❌ Roadmap não encontrado: {roadmap_path}\n")
            await assistant.close()
            sys.exit(1)

        print(f"\n🚀 Executando roadmap: {roadmap_path}")
        result = await assistant.load_and_execute_roadmap(roadmap_path, auto_execute=True)
        print(f"\n✅ Execução concluída: {result['total_steps']} etapas\n")
        await assistant.close()
        return

    # Interactive mode
    print("\n📋 Comandos disponíveis:")
    print("  - Converse normalmente para interação consciente")
    print("  - execute <roadmap> - Executar roadmap com validação")
    print("  - status - Ver status e performance")
    print("  - performance - Relatório de desempenho")
    print("  - quit - Sair")
    print()

    try:
        while True:
            user_input = input("Você: ").strip()

            if not user_input:
                continue

            if user_input.lower() == 'quit':
                print("\n👋 Até logo!\n")
                break

            elif user_input.lower() == 'status':
                import json
                status = await assistant.get_status()
                print(f"\n{json.dumps(status, indent=2)}\n")

            elif user_input.lower() == 'performance':
                perf = assistant.performance.get_report()
                print(f"\n📊 Performance Report:")
                print(f"   Tasks: {perf['tasks_completed']} completed, {perf['tasks_failed']} failed")
                print(f"   Success Rate: {perf['success_rate']}")
                print(f"   Avg Task Time: {perf['avg_task_time']}")
                print(f"   Consciousness Checks: {perf['consciousness_checks']['passed']} passed, {perf['consciousness_checks']['failed']} failed")
                print()

            elif user_input.lower().startswith('execute '):
                roadmap_path = user_input[8:].strip()
                if not os.path.exists(roadmap_path):
                    print(f"\n❌ Roadmap não encontrado: {roadmap_path}\n")
                    continue

                print(f"\n🚀 Executando roadmap com validação consciente...")
                result = await assistant.load_and_execute_roadmap(roadmap_path, auto_execute=True)
                print(f"\n✅ Execução concluída: {result['total_steps']} etapas\n")

            else:
                # Conversação consciente
                response = await assistant.think_consciously(user_input)
                print(f"\n🧠 MAXIMUS: {response}\n")

    except KeyboardInterrupt:
        print("\n\n👋 Interrompido pelo usuário. Até logo!\n")

    finally:
        await assistant.close()


def cli_main():
    """Entry point for console script"""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Interrompido pelo usuário.\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    cli_main()
