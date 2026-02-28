from agent_scanner.llm.reasoning import generate_reasoning
from agent_scanner.scanner.ast_engine import scan_file_ast
from agent_scanner.scanner.rule_engine import scan_file
from agent_scanner.utils.file_walker import get_python_files
from agent_scanner.utils.repo_loader import load_repository
import typer
from rich import print

app = typer.Typer(help="Agentic Code Security Scanner")


def deduplicate_findings(findings):
    seen = set()
    unique = []

    for f in findings:
        key = (f["file"], f["line"], f["type"].split("(")[0])
        if key not in seen:
            seen.add(key)
            unique.append(f)

    return unique

@app.command()
def scan(
    target: str = typer.Argument(..., help="Local path or GitHub repo URL"),
    ai_only: bool = typer.Option(False, "--ai-only", help="Scan only AI-related vulnerabilities"),
    fix: bool = typer.Option(False, "--fix", help="Auto-apply fixes"),
):
    repo_path = load_repository(target)
    files = get_python_files(repo_path)
    print(f"[cyan]Found {len(files)} Python files[/cyan]")
    print(f"[bold green]Scanning repository:[/bold green] {repo_path}")
    all_findings = []

    for file in files:
        regex_findings = scan_file(file)
        ast_findings = scan_file_ast(file)

        if regex_findings:
            all_findings.extend(regex_findings)

        if ast_findings:
            all_findings.extend(ast_findings)

    all_findings = deduplicate_findings(all_findings)
    print(f"[red bold]Found {len(all_findings)} potential vulnerabilities[/red bold]\n")
    for finding in all_findings:
        print(f"[bold red]{finding['type']}[/bold red]")
        print(f"[yellow]{finding['file']}:{finding['line']}[/yellow]")

        reasoning = generate_reasoning(finding)

        if reasoning:
            print(f"[cyan]Attack Simulation:[/cyan] {reasoning.attack_simulation}")
            print(f"[cyan]Impact:[/cyan] {reasoning.impact}")
            print(f"[green]Secure Fix:[/green] {reasoning.secure_fix}")
            print(f"[bold]Severity:[/bold] {reasoning.severity}\n")
   


def main():
    app()


if __name__ == "__main__":
    main()
