from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.live import Live
from rich.align import Align
from rich.text import Text
from rich.tree import Tree
import time
import questionary
import psutil
import os
import sys

# Import our managers modules
from stats_manager import StatsManager
from maintenance_manager import MaintenanceManager
from network_tools import NetworkToolkit
from advanced_info import AdvancedSystemInfo
from security_manager import SecurityManager
from productivity_tools import ProductivityTools
from activity_tracker import ActivityTracker
from config_manager import ConfigManager
from file_tools import FileDoctor
from benchmark_tools import SystemBenchmark
from services_manager import ServicesManager

console = Console()
config = ConfigManager()
stats = StatsManager()
maintenance = MaintenanceManager()
network = NetworkToolkit()
adv_info = AdvancedSystemInfo()
security = SecurityManager()
productivity = ProductivityTools()
activity = ActivityTracker()
file_doctor = FileDoctor()
bench = SystemBenchmark()
services_mgr = ServicesManager()

# Init Settings
THEME_COLOR = config.get("theme_color")

def set_theme(color):
    global THEME_COLOR
    THEME_COLOR = color
    config.set("theme_color", color)

# --- DASHBOARD LOGIC START ---
def get_snapshot():
    return {
        "uptime": stats.get_uptime(),
        "boot_time": stats.get_boot_time(),
        "system": stats.get_system_info(),
        "cpu": stats.get_cpu_info(),
        "memory": stats.get_memory_info(),
        "processes": stats.get_running_processes_summary()
    }

def create_dashboard_layout(data_snapshot):
    from rich.layout import Layout
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=3)
    )
    layout["main"].split_row(Layout(name="left"), Layout(name="right"))
    layout["left"].split_column(Layout(name="system"), Layout(name="cpu"))
    layout["right"].split_column(Layout(name="memory"), Layout(name="processes"))

    # Header
    title_text = Text(f"SYSTEM MONITOR DASHBOARD - {data_snapshot['uptime']}", style=f"bold {THEME_COLOR} reverse")
    layout["header"].update(Panel(Align.center(title_text), box=box.ROUNDED))

    # System Info
    sys_info = data_snapshot['system']
    sys_text = f"[bold]OS:[/bold] {sys_info['System']} {sys_info['Release']}\n" \
               f"[bold]Node:[/bold] {sys_info['Node Name']}\n" \
               f"[bold]Boot:[/bold] {data_snapshot['boot_time']}"
    layout["system"].update(Panel(sys_text, title="System Info", border_style=THEME_COLOR, box=box.ROUNDED))

    # CPU
    cpu = data_snapshot['cpu']
    cpu_text = f"[bold]Usage:[/bold] {cpu['CPU Usage']}\n" \
               f"[bold]Freq:[/bold] {cpu['Current Frequency']}\n" \
               f"[bold]Cores:[/bold] {cpu['Physical Cores']} (Phys) / {cpu['Total Cores']} (Log)"
    layout["cpu"].update(Panel(cpu_text, title="CPU Stats", border_style=THEME_COLOR, box=box.ROUNDED))

    # Memory
    mem = data_snapshot['memory']
    mem_table = Table.grid(expand=True)
    mem_table.add_column("Key")
    mem_table.add_column("Value", justify="right")
    mem_table.add_row("Total:", mem['Total RAM'])
    mem_table.add_row("Used:", mem['Used RAM'])
    mem_table.add_row("Free:", mem['Available RAM'])
    mem_table.add_row("Swap:", mem['Used Swap'])
    layout["memory"].update(Panel(mem_table, title=f"Memory ({mem['RAM Percentage']})", border_style=THEME_COLOR, box=box.ROUNDED))

    # Processes
    proc = data_snapshot['processes']
    proc_table = Table.grid(expand=True)
    proc_table.add_column("Name")
    proc_table.add_column("CPU%", justify="right")
    for p in proc['Top CPU Processes']:
        proc_table.add_row(p['name'][:15], f"{p['cpu_percent']}%")
    
    layout["processes"].update(Panel(proc_table, title=f"Top CPU Processes (Total: {proc['Total Processes']})", border_style=THEME_COLOR, box=box.ROUNDED))
    layout["footer"].update(Align.center(Text("Press Ctrl+C to return to menu", style="italic white")))

    return layout

def show_live_dashboard():
    console.clear()
    try:
        with Live(create_dashboard_layout(get_snapshot()), refresh_per_second=config.get("refresh_rate"), screen=True) as live:
            while True:
                live.update(create_dashboard_layout(get_snapshot()))
                time.sleep(config.get("refresh_rate"))
    except KeyboardInterrupt:
        pass
# --- DASHBOARD LOGIC END ---


def show_detailed_info():
    console.clear()
    table = Table(title="General System Information", border_style=THEME_COLOR, box=box.ROUNDED)
    table.add_column("Category", style="cyan")
    table.add_column("Property", style="magenta")
    table.add_column("Value", style="green")

    sys_info = stats.get_system_info()
    for k, v in sys_info.items(): table.add_row("System", k, str(v))
    cpu = stats.get_cpu_info()
    for k, v in cpu.items(): table.add_row("CPU", k, str(v))
    mem = stats.get_memory_info()
    for k, v in mem.items(): table.add_row("Memory", k, str(v))
    net = stats.get_network_info()
    for k, v in net.items(): table.add_row("Network", k, str(v))
    
    # Disk IO
    disk_io = stats.get_disk_io()
    if disk_io:
        for k, v in disk_io.items():
            if "Bytes" in k:
                val = f"{v / (1024**3):.2f} GB"
            else:
                val = str(v)
            table.add_row("Disk I/O", k, val)
    
    console.print(table)
    questionary.press_any_key_to_continue().ask()

def show_advanced_hardware_menu():
    console.clear()
    console.print(Panel("[bold magenta]Advanced Hardware Inspection[/bold magenta]", box=box.ROUNDED, border_style=THEME_COLOR))
    
    # GPU
    gpus = adv_info.get_gpu_info()
    console.print("\n[bold underline]GPU Analysis[/bold underline]")
    for gpu in gpus:
        if "Status" in gpu:
             console.print(f"[yellow]{gpu['Status']}[/yellow]")
        else:
             table = Table(box=box.MINIMAL)
             for k,v in gpu.items():
                 table.add_row(k, str(v))
             console.print(table)
    
    # CPU Deep Dive
    cpu_d = adv_info.get_cpu_detailed_info()
    if cpu_d:
        console.print("\n[bold underline]CPU Deep Dive[/bold underline]")
        table = Table(show_header=False, box=box.MINIMAL)
        for k, v in cpu_d.items():
            table.add_row(k, str(v))
        console.print(table)

    questionary.press_any_key_to_continue().ask()

def show_network_menu():
    while True:
        console.clear()
        console.print(Panel("[bold green]Network Intelligence[/bold green]", box=box.ROUNDED, border_style=THEME_COLOR))
        
        choice = questionary.select(
            "Select Tool:",
            choices=[
                "Check Public IP & Geo Location",
                "Run Speedtest (Bandwidth)",
                "Scan Open Ports (Localhost)",
                "Flush DNS Cache",
                "Ping Test (Google DNS)",
                questionary.Separator(),
                "Back"
            ],
            style=questionary.Style([('question', f'fg:{THEME_COLOR} bold')])
        ).ask()
        
        if choice == "Back" or choice is None:
            break
            
        elif choice == "Check Public IP & Geo Location":
            with console.status("[bold cyan]Fetching IP info...[/bold cyan]"):
                ip = network.get_public_ip()
                geo = network.get_geoip_info()
            
            console.print(f"\n[bold]Public IP:[/bold] {ip}")
            if geo:
                console.print(f"[bold]Location:[/bold] {geo.get('city')}, {geo.get('country')}")
                console.print(f"[bold]ISP:[/bold] {geo.get('isp')}")
                console.print(f"[bold]Coordinates:[/bold] {geo.get('lat')}, {geo.get('lon')}")
            questionary.press_any_key_to_continue().ask()

        elif choice == "Run Speedtest (Bandwidth)":
            console.print("[yellow]Running speedtest... this may take 30 seconds.[/yellow]")
            with console.status("[bold green]Testing download/upload...[/bold green]"):
                res = network.run_speedtest()
            
            if "error" in res:
                console.print(f"[bold red]Error:[/bold red] {res['error']}")
            else:
                table = Table(title="Network Speed Results", box=box.ROUNDED, border_style=THEME_COLOR)
                table.add_column("Metric", style="cyan")
                table.add_column("Value", style="bold green")
                table.add_row("Download", res['download'])
                table.add_row("Upload", res['upload'])
                table.add_row("Ping", res['ping'])
                console.print(table)
            questionary.press_any_key_to_continue().ask()

        elif choice == "Scan Open Ports (Localhost)":
            with console.status("[bold magenta]Scanning common ports...[/bold magenta]"):
                ports = network.scan_common_ports()
            
            if ports:
                table = Table(title="Open Ports", box=box.SIMPLE)
                table.add_column("Port")
                table.add_column("Service")
                for p, s in ports:
                    table.add_row(str(p), s)
                console.print(table)
            else:
                console.print("[green]No common open ports found on localhost.[/green]")
            questionary.press_any_key_to_continue().ask()

        elif choice == "Flush DNS Cache":
            if maintenance.flush_dns():
                console.print("[green]DNS Cache Flushed![/green]")
            else:
                console.print("[red]Failed to flush DNS.[/red]")
            questionary.press_any_key_to_continue().ask()

        elif choice == "Ping Test (Google DNS)":
             with console.status("[bold cyan]Pinging 8.8.8.8...[/bold cyan]"):
                 result = maintenance.network_connectivity_test()
             console.print(f"Result: [bold]{result}[/bold]")
             questionary.press_any_key_to_continue().ask()

def show_security_menu():
    while True:
        console.clear()
        console.print(Panel("[bold red]Security Audit[/bold red]", box=box.ROUNDED, border_style=THEME_COLOR))
        
        choice = questionary.select(
            "Select Security Task:",
            choices=[
                "Scan Suspicious Processes (Heuristic)",
                "Identify Listening Ports",
                "Check Windows Firewall Status",
                "List Startup Apps",
                questionary.Separator(),
                "Back"
            ],
            style=questionary.Style([('question', f'fg:{THEME_COLOR} bold')])
        ).ask()
        
        if choice == "Back" or choice is None:
            break
            
        elif "Suspicious Processes" in choice:
            with console.status("[red]Scanning processes...[/red]"):
                suspicious = security.check_suspicious_processes()
            if suspicious:
                table = Table(title="Suspicious Processes Found", style="red")
                table.add_column("PID")
                table.add_column("Name")
                table.add_column("Reason")
                for s in suspicious:
                    table.add_row(str(s['pid']), s['name'], s['reason'])
                console.print(table)
            else:
                console.print("[green]No obvious suspicious processes found.[/green]")
            questionary.press_any_key_to_continue().ask()
            
        elif "Listening Ports" in choice:
            listeners = security.check_listening_ports()
            table = Table(title="Apps Listening for Connections", box=box.SIMPLE)
            table.add_column("PID")
            table.add_column("Port")
            table.add_column("IP")
            for l in listeners:
                 table.add_row(str(l['pid']), str(l['port']), l['ip'])
            console.print(table)
            questionary.press_any_key_to_continue().ask()
            
        elif "Firewall" in choice:
            console.print(Panel(security.check_firewall_status(), title="Firewall Status"))
            questionary.press_any_key_to_continue().ask()
            
        elif "Startup Apps" in choice:
            apps = security.list_startup_apps()
            for a in apps:
                console.print(f"- {a}")
            questionary.press_any_key_to_continue().ask()

def show_productivity_menu():
    while True:
        console.clear()
        console.print(Panel("[bold blue]Productivity Suite[/bold blue]", box=box.ROUNDED, border_style=THEME_COLOR))
        
        choice = questionary.select(
            "Select Tool:",
            choices=[
                "Start Focus Timer (Pomodoro)",
                "Quick Notes",
                questionary.Separator(),
                "Back"
            ],
            style=questionary.Style([('question', f'fg:{THEME_COLOR} bold')])
        ).ask()
        
        if choice == "Back" or choice is None:
            break
            
        elif "Focus Timer" in choice:
            mins = questionary.text("Enter minutes to focus:", default="25").ask()
            if mins and mins.isdigit():
                try:
                    m = int(mins)
                    console.print(f"[green]Starting timer for {m} minutes. Press Ctrl+C to stop.[/green]")
                    
                    def timer_print(t_str):
                        print(f"\rTime Remaining: {t_str}", end="")
                    
                    try:
                        productivity.start_pomodoro(m, timer_print)
                        print("\nDone!")
                        questionary.press_any_key_to_continue().ask()
                    except KeyboardInterrupt:
                        productivity.stop_timer()
                        print("\nTimer stopped.")
                except ValueError:
                    pass

        elif "Quick Notes" in choice:
            while True:
                console.clear()
                notes = productivity.get_notes()
                if notes:
                    console.print(Panel("".join(notes), title="Your Notes", box=box.SIMPLE))
                else:
                    console.print("[italic]No notes yet.[/italic]")
                
                action = questionary.select(
                    "Actions:", 
                    choices=["Add Note", "Clear Notes", "Back"]
                ).ask()
                
                if action == "Back":
                    break
                elif action == "Add Note":
                    n = questionary.text("Enter note:").ask()
                    if n:
                        productivity.save_note(n)
                elif action == "Clear Notes":
                    if questionary.confirm("Delete all notes?").ask():
                        productivity.clear_notes()

def show_process_list():
    while True:
        console.clear()
        
        # Enhanced Process List with Interactive Killing
        fresh_procs = []
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                fresh_procs.append(p.info)
            except:
                pass
        
        sorted_cpu = sorted(fresh_procs, key=lambda p: p['cpu_percent'], reverse=True)[:20]
        
        proc_choices = []
        for p in sorted_cpu:
            proc_choices.append(questionary.Choice(
                f"{p['name']} (PID: {p['pid']}) - CPU: {p['cpu_percent']}%",
                value=p['pid']
            ))
            
        proc_choices.append(questionary.Separator())
        proc_choices.append(questionary.Choice("Refresh List", value="refresh"))
        proc_choices.append(questionary.Choice("Back", value="back"))
        
        selection = questionary.select(
            "Select a process to inspect/kill:",
            choices=proc_choices,
            style=questionary.Style([('question', f'fg:{THEME_COLOR} bold')])
        ).ask()
        
        if selection == "back" or selection is None:
            break
        elif selection == "refresh":
            continue
        else:
            # PID selected
            pid = selection
            try:
                p = psutil.Process(pid)
                console.print(f"\n[bold]Process Details:[/bold]")
                console.print(f"Name: {p.name()}")
                console.print(f"Status: {p.status()}")
                console.print(f"Created: {time.ctime(p.create_time())}")
                
                action = questionary.select(
                    f"Action for PID {pid}:",
                    choices=["Kill Process", "Cancel"]
                ).ask()
                
                if action == "Kill Process":
                    if questionary.confirm(f"Are you sure you want to kill {p.name()}?").ask():
                        p.kill()
                        console.print("[red]Process Killed.[/red]")
                        time.sleep(1)
            except psutil.NoSuchProcess:
                console.print("[red]Process no longer exists.[/red]")
                time.sleep(1)
            except psutil.AccessDenied:
                console.print("[red]Access Denied. Run as Admin to kill this process.[/red]")
                time.sleep(2)

def show_maintenance_menu():
    while True:
        console.clear()
        # Temp file check (quick)
        temp_size, temp_count = maintenance.get_temp_size()
        temp_size_mb = temp_size / (1024*1024)
        
        console.print(Panel(f"[bold yellow]Maintenance & Debug[/bold yellow]\n"
                            f"[dim]Current Temp Files: {temp_count} ({temp_size_mb:.2f} MB)[/dim]", 
                            box=box.ROUNDED, border_style=THEME_COLOR))
        
        choice = questionary.select(
            "Select Task:",
            choices=[
                "Clear Temporary Files",
                "Run Disk Cleanup (Native)",
                "Optimize/Defrag Drives (Native)",
                "Open Task Manager",
                "Open Control Panel",
                "Windows Services Manager (New)",
                questionary.Separator(),
                "Back"
            ],
            style=questionary.Style([('question', f'fg:{THEME_COLOR} bold')]) 
        ).ask()
        
        if choice == "Back" or choice is None:
            break
            
        elif choice == "Windows Services Manager (New)":
            show_services_menu()
            
        elif choice == "Clear Temporary Files":
            confirm = questionary.confirm(f"Are you sure you want to delete {temp_count} temp files?").ask()
            if confirm:
                with console.status("[bold red]Deleting temp files...[/bold red]"):
                    count, size, errors = maintenance.clear_temp_files()
                    time.sleep(1)
                console.print(f"[green]Deleted {count} files ({size/(1024*1024):.2f} MB).[/green]")
                questionary.press_any_key_to_continue().ask()

        elif choice == "Run Disk Cleanup (Native)":
            if maintenance.run_disk_cleanup():
                console.print("[green]Launched successfully.[/green]")
            else:
                console.print("[red]Failed.[/red]")
            time.sleep(1)
            
        elif choice == "Optimize/Defrag Drives (Native)":
            if maintenance.run_drive_optimization():
                console.print("[green]Launched successfully.[/green]")
            else:
                console.print("[red]Failed.[/red]")
            time.sleep(1)
            
        elif choice == "Open Task Manager":
            maintenance.open_task_manager()
            
        elif choice == "Open Control Panel":
            maintenance.open_control_panel()

def show_activity_analytics():
    while True:
        console.clear()
        
        summary = activity.get_summary()
        top_apps = activity.get_top_apps(5)
        top_keys = activity.get_top_keys(5)
        
        status = "[bold green]Active[/bold green]" if activity.recording else "[bold red]Stopped[/bold red]"
        
        console.print(Panel(
            f"[bold cyan]User Activity Analytics[/bold cyan] - Status: {status}\n\n"
            f"Total Keys Typed: {summary['total_keys']}\n"
            f"Total Mouse Clicks: {summary['total_clicks']}\n"
            f"Apps Tracked in DB: {len(activity.stats.get('app_usage_seconds', {}))}",
            box=box.ROUNDED, border_style=THEME_COLOR
        ))
        
        # Visualize Stats
        if top_apps:
            table_apps = Table(title="Most Used Apps (Active Window Time)", box=box.SIMPLE)
            table_apps.add_column("App Name")
            table_apps.add_column("Time (approx sec)")
            for name, seconds in top_apps:
                table_apps.add_row(name, str(seconds))
            console.print(table_apps)
            
        if top_keys:
             table_keys = Table(title="Most Used Keys", box=box.SIMPLE)
             table_keys.add_column("Key")
             table_keys.add_column("Frequency")
             for k, count in top_keys:
                 table_keys.add_row(k, str(count))
             console.print(table_keys)
        
        
        choice = questionary.select(
            "Activity Actions:",
            choices=[
                "Start/Resume Recording (Background)",
                "Stop Recording",
                questionary.Separator(),
                "Refresh Stats",
                "Back"
            ],
            style=questionary.Style([('question', f'fg:{THEME_COLOR} bold')]) 
        ).ask()
        
        if choice == "Back" or choice is None:
            break
        elif "Start" in choice:
            activity.start_recording()
            console.print("[green]Activity recording started in background.[/green]")
            time.sleep(1)
        elif "Stop" in choice:
            activity.stop_recording()
            console.print("[red]Activity recording stopped.[/red]")
            time.sleep(1)
        elif "Refresh" in choice:
            activity.stats = activity.load_stats() # Reload from file or just refresh internal dict if running
            continue


def show_services_menu():
    while True:
        console.clear()
        counts = services_mgr.get_service_counts()
        console.print(Panel(f"[bold magenta]Windows Services Manager[/bold magenta]\n"
                            f"Running: {counts.get('Running', 0)} | Stopped: {counts.get('Stopped', 0)}",
                            box=box.ROUNDED, border_style=THEME_COLOR))
        
        choice = questionary.select(
            "Select Action:",
            choices=[
                "List Running Services",
                "Back"
            ]
        ).ask()
        
        if choice == "Back" or choice is None:
            break
            
        elif choice == "List Running Services":
             services = services_mgr.get_services()
             if services:
                 table = Table(title="System Services (Partial List)", box=box.SIMPLE)
                 table.add_column("Name")
                 table.add_column("Display Name")
                 table.add_column("State")
                 
                 for s in services[:20]: # Limit for display
                     table.add_row(s['Name'], s['DisplayName'][:30], s['State'])
                 console.print(table)
             else:
                 console.print("[red]Could not fetch services (Admin rights commonly needed).[/red]")
             questionary.press_any_key_to_continue().ask()

def show_file_tools_menu():
    while True:
        console.clear()
        console.print(Panel("[bold yellow]File Doctor[/bold yellow]", box=box.ROUNDED, border_style=THEME_COLOR))
        
        choice = questionary.select(
            "Select File Tool:",
            choices=[
                "Scan for Large Files (>100MB)",
                "Scan for Duplicate Files (Hash check)",
                "Directory Tree Visualizer",
                "Back"
            ],
            style=questionary.Style([('question', f'fg:{THEME_COLOR} bold')]) 
        ).ask()
        
        if choice == "Back" or choice is None:
            break
            
        elif choice == "Scan for Large Files (>100MB)":
            path = questionary.path("Select Directory to Scan:").ask()
            if path and os.path.exists(path):
                with console.status("[bold cyan]Scanning...[/bold cyan]"):
                    res = file_doctor.scan_large_files(path)
                
                table = Table(title=f"Large Files in {path}", box=box.SIMPLE)
                table.add_column("Path")
                table.add_column("Size (MB)")
                for p, size in res:
                    table.add_row(p, f"{size/1024/1024:.2f} MB")
                console.print(table)
                questionary.press_any_key_to_continue().ask()

        elif choice == "Scan for Duplicate Files (Hash check)":
            path = questionary.path("Select Directory to Scan:").ask()
            if path and os.path.exists(path):
                console.print("[yellow]Scanner started. This may take a while...[/yellow]")
                with console.status("[bold cyan]Hashing files...[/bold cyan]"):
                    dupes = file_doctor.find_duplicates(path)
                
                if dupes:
                    for size, paths in dupes:
                        console.print(f"[bold red]Duplicate Set ({size/1024:.2f} KB):[/bold red]")
                        for p in paths:
                            console.print(f" - {p}")
                else:
                    console.print("[green]No duplicates found.[/green]")
                questionary.press_any_key_to_continue().ask()
        
        elif choice == "Directory Tree Visualizer":
             path = questionary.path("Select Directory:").ask()
             if path and os.path.exists(path):
                 tree = Tree(path)
                 # Simple BFS for tree
                 try:
                     for root, dirs, files in os.walk(path):
                         base = os.path.basename(root)
                         if root == path:
                             branch = tree
                         else:
                            # Too complex to map generically for endless depth in rich quickly, 
                            # just showing top level for demo
                            continue 
                         for d in dirs[:10]:
                             branch.add(f"[bold cyan]{d}/[/bold cyan]")
                         for f in files[:10]:
                             branch.add(f"[green]{f}[/green]")
                         break # Just one level for speed demo
                 except: pass
                 console.print(tree)
                 questionary.press_any_key_to_continue().ask()

def show_benchmark_menu():
    while True:
        console.clear()
        console.print(Panel("[bold magenta]System Benchmarks[/bold magenta]", box=box.ROUNDED, border_style=THEME_COLOR))
        
        choice = questionary.select(
            "Select Benchmark:",
            choices=[
                "CPU Stress Test (Math Ops)",
                "Disk Write Speed Test (100MB)",
                "Memory Integrity Check (Quick)",
                "Back"
            ],
            style=questionary.Style([('question', f'fg:{THEME_COLOR} bold')]) 
        ).ask()
        if choice == "Back" or choice is None:
            break
            
        elif "CPU" in choice:
            with console.status("Running CPU Stress Test (5s)..."):
                score = bench.cpu_stress_test(5)
            console.print(f"[bold green]Result Score: {score} ops[/bold green]")
            questionary.press_any_key_to_continue().ask()
            
        elif "Disk" in choice:
            with console.status("Testing Disk Write Speed..."):
                res = bench.disk_write_speed()
            console.print(f"[bold green]Write Speed: {res}[/bold green]")
            questionary.press_any_key_to_continue().ask()
            
        elif "Memory" in choice:
            with console.status("Checking Memory..."):
                res = bench.memory_check()
            console.print(f"[bold green]Result: {res}[/bold green]")
            questionary.press_any_key_to_continue().ask()


def show_proper_settings():
    while True:
        console.clear()
        console.print(Panel("[bold]Configuration & Settings[/bold]", box=box.ROUNDED, border_style=THEME_COLOR))
        
        current_theme = config.get("theme_color")
        current_rate = config.get("refresh_rate")
        notifications = "ON" if config.get("enable_notifications") else "OFF"
        
        choice = questionary.select(
            "Change Setting:",
            choices=[
                f"Theme Color (Current: {current_theme})",
                f"Dashboard Refresh Rate (Current: {current_rate}s)",
                f"Notifications (Current: {notifications})",
                "Back"
            ]
        ).ask()
        
        if choice == "Back" or choice is None:
            break
            
        elif "Theme Color" in choice:
            colors = ["cyan", "magenta", "green", "blue", "red", "yellow"]
            c = questionary.select("Select Color:", choices=colors).ask()
            if c:
                set_theme(c)
                config.set("theme_color", c)
                
        elif "Refresh Rate" in choice:
            rates = ["0.5", "1.0", "2.0", "5.0"]
            r = questionary.select("Select Rate (seconds):", choices=rates).ask()
            if r:
                config.set("refresh_rate", float(r))
                
        elif "Notifications" in choice:
            val = not config.get("enable_notifications")
            config.set("enable_notifications", val)
