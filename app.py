import sys
import questionary
from interface import show_live_dashboard, show_detailed_info, show_process_list
from rich.console import Console

console = Console()

def main():
    while True:
        console.clear()
        # Custom style for a "premium" feel
        custom_style = questionary.Style([
            ('qmark', 'fg:#00ffff bold'),
            ('question', 'bold fg:#ffffff'),
            ('answer', 'fg:#00ffff bold'),
            ('pointer', 'fg:#00ffff bold'),
            ('highlighted', 'fg:#00ffff bold'),
            ('selected', 'fg:#00ffff'),
            ('separator', 'fg:#666666'),
            ('instruction', 'fg:#666666 italic'),
            ('text', ''),
            ('disabled', 'fg:#858585 italic')
        ])

        action = questionary.select(
            "Main Menu",
            choices=[
                questionary.Choice("Dashboard (Live Stats)"),
                questionary.Choice("Detailed System Info"),
                questionary.Choice("Advanced Hardware Info"),
                questionary.Choice("Network Tools"),
                questionary.Choice("Activity Analytics (Key/Mouse Tracking)"),
                questionary.Choice("File Doctor (Large/Duplicate Files)"),
                questionary.Choice("System Benchmarks"),
                questionary.Choice("Process Monitor (Interactive)"),
                questionary.Choice("Security Audit"),
                questionary.Choice("Productivity Suite"),
                questionary.Choice("Start Maintenance & Debug"),
                questionary.Choice("Settings"),
                questionary.Separator(),
                questionary.Choice("Exit")
            ],
            style=custom_style,
            use_indicator=True,
            instruction="(Use arrow keys to navigate, Enter to select)"
        ).ask()

        if action == "Dashboard (Live Stats)":
            show_live_dashboard()
        elif action == "Detailed System Info":
            show_detailed_info()
        elif action == "Advanced Hardware Info":
            from interface import show_advanced_hardware_menu
            show_advanced_hardware_menu()
        elif action == "Network Tools":
            from interface import show_network_menu
            show_network_menu()
        elif action == "Activity Analytics (Key/Mouse Tracking)":
            from interface import show_activity_analytics
            show_activity_analytics()
        elif action == "File Doctor (Large/Duplicate Files)":
            from interface import show_file_tools_menu
            show_file_tools_menu()
        elif action == "System Benchmarks":
            from interface import show_benchmark_menu
            show_benchmark_menu()
        elif action == "Process Monitor (Interactive)":
            show_process_list()
        elif action == "Security Audit":
            from interface import show_security_menu
            show_security_menu()
        elif action == "Productivity Suite":
            from interface import show_productivity_menu
            show_productivity_menu()
        elif action == "Start Maintenance & Debug":
            from interface import show_maintenance_menu
            show_maintenance_menu()
        elif action == "Settings":
            from interface import show_proper_settings
            show_proper_settings()
        elif action == "Exit" or action is None:
            console.print("[bold cyan]Goodbye![/bold cyan]")
            sys.exit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Exiting...[/bold red]")
