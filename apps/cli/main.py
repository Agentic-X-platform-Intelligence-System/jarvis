"""Jarvis CLI — Typer + Rich chat (M1 stub)."""

from __future__ import annotations

import typer

app = typer.Typer(help="Jarvis CLI — AXIS flagship orchestrator")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """Jarvis CLI entry point (stub)."""
    if ctx.invoked_subcommand is None:
        typer.echo("Jarvis CLI is not implemented yet. See agentic-ai-ideas/scope.md M1 checklist.")
        raise typer.Exit(code=0)


if __name__ == "__main__":
    app()
