"""
CrewAI Multi-Agent Demo: Software Architecture Planning System
================================================================

This implementation uses AI agents to collaboratively design a complete
software architecture for an e-commerce platform.

Agents:
1. Requirements Analyst - Analyzes functional and non-functional requirements
2. System Architect - Designs microservices architecture
3. Database Designer - Plans data models and database strategy
4. DevOps Engineer - Designs deployment and infrastructure
5. Security Specialist - Identifies security requirements and solutions

Use Case: Design a scalable e-commerce platform architecture
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from crewai import Agent, Task, Crew
from crewai.tools import tool

# Add parent directory to path to import shared_config
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import shared configuration
from shared_config import Config, validate_config


# ============================================================================
# TOOLS
# ============================================================================

@tool
def research_architecture_patterns(pattern_type: str) -> str:
    """
    Research software architecture patterns and best practices.
    """
    return f"""
    Research task: Analyze {pattern_type} architecture patterns.

    Please research and provide:
    1. Common architectural patterns (microservices, event-driven, etc.)
    2. Industry best practices and standards
    3. Scalability considerations
    4. Technology stack recommendations
    5. Case studies of similar systems
    6. Performance and reliability patterns

    Focus on modern, production-ready architectures.
    """


@tool
def research_database_solutions(system_type: str) -> str:
    """
    Research database solutions and data modeling strategies.
    """
    return f"""
    Research task: Analyze database solutions for {system_type}.

    Please research and provide:
    1. Database types (SQL, NoSQL, NewSQL)
    2. Data modeling best practices
    3. Sharding and replication strategies
    4. Caching strategies (Redis, Memcached)
    5. Data consistency patterns
    6. Backup and disaster recovery

    Consider scalability, performance, and data integrity.
    """


@tool
def research_cloud_infrastructure(platform_type: str) -> str:
    """
    Research cloud infrastructure and deployment strategies.
    """
    return f"""
    Research task: Analyze cloud infrastructure for {platform_type}.

    Please research and provide:
    1. Cloud providers comparison (AWS, Azure, GCP)
    2. Container orchestration (Kubernetes, Docker Swarm)
    3. CI/CD pipeline design
    4. Monitoring and logging solutions
    5. Auto-scaling strategies
    6. Cost optimization techniques

    Focus on production-grade, scalable solutions.
    """


@tool
def research_security_practices(system_type: str) -> str:
    """
    Research security best practices and compliance requirements.
    """
    return f"""
    Research task: Analyze security requirements for {system_type}.

    Please research and provide:
    1. Authentication and authorization patterns (OAuth, JWT)
    2. Data encryption (at rest and in transit)
    3. API security best practices
    4. Compliance requirements (GDPR, PCI-DSS)
    5. Threat modeling and mitigation
    6. Security monitoring and incident response

    Focus on comprehensive, defense-in-depth approaches.
    """


# ============================================================================
# AGENT DEFINITIONS
# ============================================================================

def create_requirements_analyst(project_name: str):
    """Create the Requirements Analyst agent."""
    return Agent(
        role="Requirements Analyst",
        goal=f"Analyze and document comprehensive requirements for {project_name}, "
             f"including functional, non-functional, and technical constraints. "
             f"Identify key user stories and system capabilities.",
        backstory="You are an experienced business analyst who excels at understanding "
                  "complex systems and translating business needs into technical requirements. "
                  "You have worked on numerous e-commerce platforms and understand both "
                  "business and technical perspectives. You ask the right questions and "
                  "identify hidden requirements that others might miss.",
        tools=[research_architecture_patterns],
        verbose=True,
        allow_delegation=False
    )


def create_system_architect(project_name: str):
    """Create the System Architect agent."""
    return Agent(
        role="System Architect",
        goal=f"Design a scalable, maintainable microservices architecture for {project_name}, "
             f"defining services, APIs, communication patterns, and system boundaries. "
             f"Create a blueprint that addresses all identified requirements.",
        backstory="You are a senior system architect with 15+ years of experience designing "
                  "large-scale distributed systems. You have deep expertise in microservices, "
                  "event-driven architectures, and domain-driven design. You make pragmatic "
                  "decisions that balance technical excellence with business needs. "
                  "You've successfully architected systems that handle millions of users.",
        tools=[research_architecture_patterns],
        verbose=True,
        allow_delegation=False
    )


def create_database_designer(project_name: str):
    """Create the Database Designer agent."""
    return Agent(
        role="Database Designer",
        goal=f"Design comprehensive data models and database strategy for {project_name}, "
             f"including database selection, schema design, and data access patterns. "
             f"Ensure data integrity, performance, and scalability.",
        backstory="You are a database expert with deep knowledge of both SQL and NoSQL databases. "
                  "You understand data modeling, normalization, indexing strategies, and query "
                  "optimization. You have designed databases for high-traffic applications and "
                  "know how to handle complex data relationships, caching, and consistency. "
                  "You always consider performance, scalability, and maintainability.",
        tools=[research_database_solutions],
        verbose=True,
        allow_delegation=False
    )


def create_devops_engineer(project_name: str):
    """Create the DevOps Engineer agent."""
    return Agent(
        role="DevOps Engineer",
        goal=f"Design the deployment infrastructure and CI/CD pipeline for {project_name}, "
             f"including cloud platform selection, containerization, orchestration, "
             f"monitoring, and automation strategies.",
        backstory="You are a DevOps expert who has built and maintained production infrastructure "
                  "for large-scale applications. You have expertise in Kubernetes, Docker, "
                  "AWS/Azure/GCP, Terraform, and CI/CD tools. You understand how to build "
                  "reliable, self-healing systems with proper monitoring and alerting. "
                  "You prioritize automation, observability, and operational excellence.",
        tools=[research_cloud_infrastructure],
        verbose=True,
        allow_delegation=False
    )


def create_security_specialist(project_name: str):
    """Create the Security Specialist agent."""
    return Agent(
        role="Security Specialist",
        goal=f"Identify security requirements and design security architecture for {project_name}, "
             f"including authentication, authorization, data protection, and compliance measures. "
             f"Ensure the system is secure by design.",
        backstory="You are a cybersecurity expert with deep knowledge of application security, "
                  "network security, and compliance requirements. You have experience securing "
                  "e-commerce platforms and handling sensitive customer data. You understand "
                  "OWASP top 10, zero-trust architecture, and defense-in-depth strategies. "
                  "You think like both a defender and an attacker to identify vulnerabilities.",
        tools=[research_security_practices],
        verbose=True,
        allow_delegation=False
    )


# ============================================================================
# TASK DEFINITIONS
# ============================================================================

def create_requirements_task(analyst_agent, project_name: str, project_description: str):
    """Define the requirements analysis task."""
    return Task(
        description=f"Analyze and document comprehensive requirements for {project_name}. "
                   f"Project Description: {project_description}\n\n"
                   f"Your analysis should include:\n"
                   f"1. Functional Requirements:\n"
                   f"   - Core features and capabilities\n"
                   f"   - User stories and use cases\n"
                   f"   - Business workflows\n"
                   f"2. Non-Functional Requirements:\n"
                   f"   - Performance targets (response time, throughput)\n"
                   f"   - Scalability requirements (expected users, growth)\n"
                   f"   - Availability and reliability targets\n"
                   f"   - Security and compliance needs\n"
                   f"3. Technical Constraints:\n"
                   f"   - Integration requirements\n"
                   f"   - Technology preferences or limitations\n"
                   f"   - Budget and timeline considerations\n"
                   f"4. Key Success Metrics\n\n"
                   f"Provide a clear, structured analysis that will guide the architecture design.",
        agent=analyst_agent,
        expected_output=f"A comprehensive requirements document for {project_name} including "
                       f"functional requirements, non-functional requirements, technical constraints, "
                       f"and success metrics in a structured format"
    )


def create_architecture_task(architect_agent, project_name: str):
    """Define the system architecture design task."""
    return Task(
        description=f"Based on the requirements analysis, design a complete microservices "
                   f"architecture for {project_name}. Your design should include:\n\n"
                   f"1. System Architecture:\n"
                   f"   - High-level architecture diagram (conceptual)\n"
                   f"   - Microservices breakdown and responsibilities\n"
                   f"   - Service boundaries and domain models\n"
                   f"2. Communication Patterns:\n"
                   f"   - API design (REST, GraphQL, gRPC)\n"
                   f"   - Inter-service communication\n"
                   f"   - Event-driven patterns if applicable\n"
                   f"   - API Gateway strategy\n"
                   f"3. Technology Stack:\n"
                   f"   - Programming languages and frameworks\n"
                   f"   - Message queues and event streaming\n"
                   f"   - Caching layers\n"
                   f"4. Scalability and Resilience:\n"
                   f"   - Load balancing strategy\n"
                   f"   - Circuit breakers and fallbacks\n"
                   f"   - Service mesh considerations\n\n"
                   f"Provide detailed explanations for architectural decisions.",
        agent=architect_agent,
        expected_output=f"A detailed system architecture design for {project_name} including "
                       f"microservices breakdown, communication patterns, technology stack, "
                       f"and scalability/resilience strategies with clear rationale"
    )


def create_database_task(database_agent, project_name: str):
    """Define the database design task."""
    return Task(
        description=f"Based on the system architecture, design a comprehensive database "
                   f"strategy for {project_name}. Your design should include:\n\n"
                   f"1. Database Architecture:\n"
                   f"   - Database type selection (SQL vs NoSQL per service)\n"
                   f"   - Database-per-service pattern\n"
                   f"   - Data consistency strategies\n"
                   f"2. Data Models:\n"
                   f"   - Core entity relationships\n"
                   f"   - Schema design for key services\n"
                   f"   - Normalization vs denormalization decisions\n"
                   f"3. Performance Optimization:\n"
                   f"   - Indexing strategy\n"
                   f"   - Caching layers (Redis, Memcached)\n"
                   f"   - Query optimization approaches\n"
                   f"   - Read replicas and sharding\n"
                   f"4. Data Management:\n"
                   f"   - Backup and recovery strategy\n"
                   f"   - Data migration approach\n"
                   f"   - Data retention policies\n\n"
                   f"Provide rationale for database technology choices.",
        agent=database_agent,
        expected_output=f"A comprehensive database design for {project_name} including "
                       f"database selection, data models, performance optimization strategies, "
                       f"and data management approaches with clear justification"
    )


def create_devops_task(devops_agent, project_name: str):
    """Define the DevOps and infrastructure task."""
    return Task(
        description=f"Based on the system architecture and database design, create a "
                   f"comprehensive DevOps and infrastructure plan for {project_name}. "
                   f"Your plan should include:\n\n"
                   f"1. Cloud Infrastructure:\n"
                   f"   - Cloud provider recommendation (AWS/Azure/GCP)\n"
                   f"   - Infrastructure as Code approach (Terraform, CloudFormation)\n"
                   f"   - Environment strategy (dev, staging, prod)\n"
                   f"2. Containerization and Orchestration:\n"
                   f"   - Docker containerization strategy\n"
                   f"   - Kubernetes cluster design\n"
                   f"   - Service mesh considerations\n"
                   f"3. CI/CD Pipeline:\n"
                   f"   - Build and deployment automation\n"
                   f"   - Testing strategy (unit, integration, e2e)\n"
                   f"   - Rollback and blue-green deployment\n"
                   f"4. Monitoring and Observability:\n"
                   f"   - Logging aggregation (ELK, Splunk)\n"
                   f"   - Metrics and monitoring (Prometheus, Grafana)\n"
                   f"   - Distributed tracing\n"
                   f"   - Alerting strategy\n\n"
                   f"Provide cost estimates and optimization recommendations.",
        agent=devops_agent,
        expected_output=f"A complete DevOps and infrastructure plan for {project_name} including "
                       f"cloud infrastructure design, container orchestration, CI/CD pipeline, "
                       f"monitoring strategy, and cost considerations"
    )


def create_security_task(security_agent, project_name: str):
    """Define the security architecture task."""
    return Task(
        description=f"Based on the complete system design, create a comprehensive security "
                   f"architecture for {project_name}. Your security plan should include:\n\n"
                   f"1. Authentication and Authorization:\n"
                   f"   - User authentication strategy (OAuth 2.0, JWT)\n"
                   f"   - Role-based access control (RBAC)\n"
                   f"   - API authentication and authorization\n"
                   f"   - Session management\n"
                   f"2. Data Security:\n"
                   f"   - Encryption at rest and in transit (TLS/SSL)\n"
                   f"   - Sensitive data handling (PII, payment info)\n"
                   f"   - Key management strategy\n"
                   f"3. Application Security:\n"
                   f"   - Input validation and sanitization\n"
                   f"   - Protection against OWASP Top 10\n"
                   f"   - API rate limiting and DDoS protection\n"
                   f"   - Secrets management\n"
                   f"4. Compliance and Governance:\n"
                   f"   - GDPR compliance measures\n"
                   f"   - PCI-DSS for payment processing\n"
                   f"   - Audit logging and compliance reporting\n"
                   f"5. Security Operations:\n"
                   f"   - Vulnerability scanning and patching\n"
                   f"   - Incident response plan\n"
                   f"   - Security monitoring and SIEM\n\n"
                   f"Provide a security checklist for implementation.",
        agent=security_agent,
        expected_output=f"A comprehensive security architecture for {project_name} including "
                       f"authentication/authorization, data security, application security, "
                       f"compliance measures, and security operations with implementation checklist"
    )


# ============================================================================
# CREW ORCHESTRATION
# ============================================================================

def main(project_name: str = "E-Commerce Platform",
         project_description: str = "A modern e-commerce platform with user management, "
                                   "product catalog, shopping cart, order processing, "
                                   "payment integration, and admin dashboard. Expected to "
                                   "handle 100K concurrent users with 99.9% uptime."):
    """
    Main function to orchestrate the software architecture design crew.

    Args:
        project_name: Name of the software project
        project_description: Detailed description of the project requirements
    """

    print("=" * 80)
    print("CrewAI Multi-Agent Software Architecture Planning System")
    print(f"Designing Architecture for: {project_name}")
    print("=" * 80)
    print()
    print(f"📋 Project: {project_name}")
    print(f"📝 Description: {project_description}")
    print()

    # Validate configuration
    print("🔍 Validating configuration...")
    if not validate_config():
        print("❌ Configuration validation failed. Please set up your .env file.")
        exit(1)

    # Set environment variables for CrewAI
    os.environ["OPENAI_API_KEY"] = Config.API_KEY
    os.environ["OPENAI_API_BASE"] = Config.API_BASE
    
    if Config.USE_GROQ:
        os.environ["OPENAI_MODEL_NAME"] = Config.OPENAI_MODEL

    print("✅ Configuration validated successfully!")
    print()
    Config.print_summary()
    print()

    # Create agents
    print("[1/5] Creating Requirements Analyst Agent...")
    analyst_agent = create_requirements_analyst(project_name)

    print("[2/5] Creating System Architect Agent...")
    architect_agent = create_system_architect(project_name)

    print("[3/5] Creating Database Designer Agent...")
    database_agent = create_database_designer(project_name)

    print("[4/5] Creating DevOps Engineer Agent...")
    devops_agent = create_devops_engineer(project_name)

    print("[5/5] Creating Security Specialist Agent...")
    security_agent = create_security_specialist(project_name)

    print("\n✅ All agents created successfully!")
    print()

    # Create tasks
    print("Creating tasks for the crew...")
    requirements_task = create_requirements_task(analyst_agent, project_name, project_description)
    architecture_task = create_architecture_task(architect_agent, project_name)
    database_task = create_database_task(database_agent, project_name)
    devops_task = create_devops_task(devops_agent, project_name)
    security_task = create_security_task(security_agent, project_name)

    print("Tasks created successfully!")
    print()

    # Create the crew
    print("Forming the Software Architecture Crew...")
    print("Task Sequence: Requirements → Architecture → Database → DevOps → Security")
    print()

    crew = Crew(
        agents=[analyst_agent, architect_agent, database_agent, devops_agent, security_agent],
        tasks=[requirements_task, architecture_task, database_task, devops_task, security_task],
        verbose=True,
        process="sequential"
    )

    # Execute the crew
    print("=" * 80)
    print("Starting Crew Execution...")
    print(f"Designing Complete Architecture for {project_name}")
    print("=" * 80)
    print()

    try:
        result = crew.kickoff(inputs={
            "project_name": project_name,
            "project_description": project_description
        })

        print()
        print("=" * 80)
        print("✅ Architecture Design Completed Successfully!")
        print("=" * 80)
        print()
        print(f"COMPLETE SOFTWARE ARCHITECTURE FOR {project_name.upper()}:")
        print("-" * 80)
        print(result)
        print("-" * 80)

        # Save output to file
        output_filename = f"software_architecture_{project_name.lower().replace(' ', '_')}.txt"
        output_path = Path(__file__).parent / output_filename

        with open(output_path, "w", encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("Software Architecture Design Document\n")
            f.write(f"Project: {project_name}\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Project Description:\n{project_description}\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Generated by: CrewAI Multi-Agent System\n\n")
            f.write("ARCHITECTURE DESIGN:\n")
            f.write("-" * 80 + "\n")
            f.write(str(result))
            f.write("\n" + "-" * 80 + "\n")

        print(f"\n✅ Architecture document saved to {output_filename}")

    except Exception as e:
        print(f"\n❌ Error during crew execution: {str(e)}")
        print("\n🔍 Troubleshooting:")
        print("   1. Verify API key is valid")
        print("   2. Check API credits/quota")
        print("   3. Verify internet connection")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Example: Design an e-commerce platform
    main(
        project_name="E-Commerce Platform",
        project_description="A modern, scalable e-commerce platform with product catalog, "
                          "shopping cart, order management, payment processing, user accounts, "
                          "and admin dashboard. Must support 100K concurrent users, "
                          "handle $10M+ daily transactions, ensure 99.9% uptime, "
                          "and comply with PCI-DSS and GDPR requirements."
    )
    
    # You can try other projects by uncommenting:
    # main(
    #     project_name="Social Media Platform",
    #     project_description="A real-time social media platform with posts, comments, "
    #                       "likes, messaging, notifications, and content moderation."
    # )
