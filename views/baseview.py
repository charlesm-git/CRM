from rich import print
from rich.console import Console
from rich.table import Table

from utils.formatter import object_formatter


def is_created():
    print("[bold green]Ressource created successfully[/bold green]")


def is_updated():
    print("[bold green]Ressource updated successfully[/bold green]")


def is_deleted():
    print("[bold green]Ressource deleted successfully[/bold green]")


def is_not_found_error():
    print("[bold red]Ressource not found[/bold red]")


def invalid_format_error():
    print("[yellow]Invalid format, try again.[/yellow]")


def can_not_be_empty_error():
    print("[yellow]This field can't be empty.[/yellow]")


def update_message():
    print(
        "[magenta]Enter the information to update. [bold]Just press Enter to "
        "leave unchanged.[/bold][/magenta]"
    )


def display_object(obj):
    """Display a single object in a table"""
    console = Console()

    # Create the table
    table = Table(
        title=obj.__class__.__name__,
        show_header=True,
        header_style="bold magenta",
    )

    # Add columns for attribute and value
    table.add_column("Attribute", style="cyan", justify="left")
    table.add_column("Value", style="green", justify="left")

    data = object_formatter(obj)

    # Populate table with attributes and values
    for line in data:
        column, value = line
        table.add_row(column, str(value))

    # Print the table
    console.print(table)
