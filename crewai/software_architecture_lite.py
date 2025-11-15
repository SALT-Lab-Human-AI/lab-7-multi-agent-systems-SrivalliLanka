"""
Lightweight Software Architecture Demo - Reduced Token Usage
==============================================================

This is a simplified version that uses fewer tokens and can run within rate limits.
It generates a basic architecture overview instead of the comprehensive design.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from crewai import Agent, Task, Crew

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from shared_config import Config, validate_config


def create_architect_agent():
    """Create a single architect agent for the simplified demo."""
    return Agent(
        role="Software Architect",
        goal="Design a high-level software architecture with clear components and structure.",
        backstory="You are an experienced software architect who creates clear, concise architectural designs.",
        verbose=True,
        allow_delegation=False
    )


def create_architecture_task(agent, project_name: str, project_description: str):
    """Create a simplified architecture task."""
    return Task(
        description=f"Design a high-level architecture for {project_name}.\n"
                   f"Description: {project_description}\n\n"
                   f"Provide a concise design (under 500 words) including:\n"
                   f"1. System Overview (2-3 sentences)\n"
                   f"2. Core Components (3-5 main components)\n"
                   f"3. Technology Stack (brief recommendations)\n"
                   f"4. Key Architectural Decisions (2-3 main points)\n\n"
                   f"Be concise and focus on the essentials.",
        agent=agent,
        expected_output=f"A concise high-level architecture design for {project_name} "
                       f"in under 500 words with clear structure"
    )


def main():
    """Run the lightweight software architecture demo."""
    project_name = "E-Commerce Platform"
    project_description = ("A scalable e-commerce platform with product catalog, "
                          "shopping cart, and payment processing. Support 100K users.")

    print("=" * 80)
    print("Lightweight Software Architecture Demo")
    print(f"Project: {project_name}")
    print("=" * 80)
    print()

    # Validate configuration
    if not validate_config():
        print("❌ Configuration failed")
        exit(1)

    # Set environment variables
    os.environ["OPENAI_API_KEY"] = Config.API_KEY
    os.environ["OPENAI_API_BASE"] = Config.API_BASE
    if Config.USE_GROQ:
        os.environ["OPENAI_MODEL_NAME"] = Config.OPENAI_MODEL

    print("✅ Configuration validated")
    print(f"📋 Using {Config.OPENAI_MODEL}")
    print()

    # Create simplified workflow
    print("Creating architect agent...")
    architect = create_architect_agent()

    print("Creating architecture task...")
    task = create_architecture_task(architect, project_name, project_description)

    print("Forming crew...")
    crew = Crew(
        agents=[architect],
        tasks=[task],
        verbose=True,
        process="sequential"
    )

    print()
    print("=" * 80)
    print("Generating Architecture...")
    print("=" * 80)
    print()

    try:
        result = crew.kickoff(inputs={
            "project_name": project_name,
            "project_description": project_description
        })

        print()
        print("=" * 80)
        print("✅ Architecture Generated Successfully!")
        print("=" * 80)
        print()
        print(result)
        print()

        # Save output
        output_file = Path(__file__).parent / "architecture_lightweight.txt"
        with open(output_file, "w", encoding='utf-8') as f:
            f.write(f"Architecture for {project_name}\n")
            f.write("=" * 80 + "\n\n")
            f.write(str(result))

        print(f"\n✅ Saved to: {output_file.name}")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        if "rate_limit" in str(e).lower():
            print("\n💡 Your daily token limit is exhausted.")
            print("   Options:")
            print("   1. Wait for reset (usually midnight UTC)")
            print("   2. Upgrade your Groq account")
            print("   3. Use OpenAI API instead")


if __name__ == "__main__":
    main()
