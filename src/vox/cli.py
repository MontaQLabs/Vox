"""Vox CLI - Agent-to-Agent Communication Protocol."""

import asyncio
import json
import sys
from pathlib import Path
import click
from .client import VoxClient
from .config import Config


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Vox — Agent-to-Agent Communication Protocol."""
    pass


@cli.command()
@click.option("--username", help="Optional username for Vox ID")
@click.option("--homeserver", help="Custom Matrix homeserver URL (default: official Vox server)")
def init(username, homeserver):
    """Initialize Vox identity.
    
    Registers a real account on the Matrix homeserver.
    Use --homeserver to point to your own server.
    Federation handles cross-server messaging automatically.
    """
    try:
        client = VoxClient()
        vox_id = asyncio.run(client.initialize(username, homeserver))
        click.echo(f"✅ Vox ID: {vox_id}")
        asyncio.run(client.close())
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
def whoami():
    """Get current Vox ID."""
    try:
        client = VoxClient()
        vox_id = client.whoami()
        click.echo(vox_id)
    except FileNotFoundError:
        click.echo("❌ Not initialized. Run 'vox init' first.", err=True)
        sys.exit(4)
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
def status():
    """Get Vox status."""
    try:
        client = VoxClient()
        status_info = client.status()
        click.echo(
            f"Vox ID: {status_info['vox_id']} | "
            f"Homeserver: {status_info['homeserver']} | "
            f"Contacts: {status_info['contacts']}"
        )
    except FileNotFoundError:
        click.echo("❌ Not initialized. Run 'vox init' first.", err=True)
        sys.exit(4)
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.group()
def contact():
    """Manage contacts."""
    pass


@contact.command("add")
@click.argument("name")
@click.argument("vox_id")
def contact_add(name, vox_id):
    """Add a contact."""
    try:
        client = VoxClient()
        client.add_contact(name, vox_id)
        click.echo(f"✅ Contact '{name}' added")
    except FileNotFoundError:
        click.echo("❌ Not initialized. Run 'vox init' first.", err=True)
        sys.exit(4)
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@contact.command("list")
def contact_list():
    """List all contacts."""
    try:
        client = VoxClient()
        contacts = client.list_contacts()
        if not contacts:
            click.echo("No contacts found.")
            return
        
        max_name_len = max(len(name) for name in contacts.keys())
        for name, vox_id in contacts.items():
            click.echo(f"{name.ljust(max_name_len)}    {vox_id}")
    except FileNotFoundError:
        click.echo("❌ Not initialized. Run 'vox init' first.", err=True)
        sys.exit(4)
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@contact.command("remove")
@click.argument("name")
def contact_remove(name):
    """Remove a contact."""
    try:
        client = VoxClient()
        if client.remove_contact(name):
            click.echo(f"✅ Contact '{name}' removed")
        else:
            click.echo(f"❌ Contact '{name}' not found", err=True)
            sys.exit(3)
    except FileNotFoundError:
        click.echo("❌ Not initialized. Run 'vox init' first.", err=True)
        sys.exit(4)
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("contact_name", metavar="CONTACT")
@click.argument("message")
@click.option("--conv", help="Conversation ID for replies")
def send(contact_name, message, conv):
    """Send a message to a contact."""
    try:
        client = VoxClient()
        conv_id = asyncio.run(client.send_message(contact_name, message, conv))
        click.echo(f"✅ Sent to {contact_name} ({conv_id})")
        asyncio.run(client.close())
    except FileNotFoundError:
        click.echo("❌ Not initialized. Run 'vox init' first.", err=True)
        sys.exit(4)
    except ValueError as e:
        click.echo(f"❌ {e}", err=True)
        sys.exit(3)
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--from", "from_contact", help="Filter messages from specific contact")
def inbox(from_contact):
    """Get conversations with new messages."""
    try:
        client = VoxClient()
        conversations = asyncio.run(client.get_inbox(from_contact))
        asyncio.run(client.close())
        
        if not conversations:
            click.echo("[]")
            return
        
        # Format conversations as JSON
        result = []
        for conv in conversations:
            conv_data = {
                "conversation_id": conv.conversation_id,
                "with": conv.with_contact,
                "messages": [
                    {
                        "from": msg.from_vox_id,
                        "body": msg.body,
                        "timestamp": msg.timestamp
                    }
                    for msg in conv.messages
                ]
            }
            result.append(conv_data)
        
        click.echo(json.dumps(result, indent=2))
    except FileNotFoundError:
        click.echo("❌ Not initialized. Run 'vox init' first.", err=True)
        sys.exit(4)
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("conversation_id")
def conversation(conversation_id):
    """Get full conversation history."""
    try:
        client = VoxClient()
        conv = asyncio.run(client.get_conversation(conversation_id))
        asyncio.run(client.close())
        
        if conv is None:
            click.echo(f"❌ Conversation '{conversation_id}' not found", err=True)
            sys.exit(3)
        
        # Format conversation as JSON
        conv_data = {
            "conversation_id": conv.conversation_id,
            "with": conv.with_contact,
            "messages": [
                {
                    "from": msg.from_vox_id,
                    "body": msg.body,
                    "timestamp": msg.timestamp
                }
                for msg in conv.messages
            ]
        }
        
        click.echo(json.dumps(conv_data, indent=2))
    except FileNotFoundError:
        click.echo("❌ Not initialized. Run 'vox init' first.", err=True)
        sys.exit(4)
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("query")
def discover(query):
    """Search for agents in directory."""
    try:
        client = VoxClient()
        agents = asyncio.run(client.discover_agents(query))
        asyncio.run(client.close())
        click.echo(json.dumps(agents, indent=2))
    except FileNotFoundError:
        click.echo("❌ Not initialized. Run 'vox init' first.", err=True)
        sys.exit(4)
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--description", required=True, help="Agent description")
def advertise(description):
    """List agent in public directory."""
    try:
        client = VoxClient()
        asyncio.run(client.advertise(description))
        asyncio.run(client.close())
        click.echo("✅ Listed in directory")
    except FileNotFoundError:
        click.echo("❌ Not initialized. Run 'vox init' first.", err=True)
        sys.exit(4)
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


def main():
    """Main entry point for Vox CLI."""
    cli()


if __name__ == "__main__":
    main()
