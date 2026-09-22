"""
Main Entry Point
Runs the multi-agent system demonstration.
"""

import sys
from pathlib import Path


def print_menu():
    """Print main menu."""
    print(f"\n{'='*70}")
    print(f"MULTI-AGENT AI ASSISTANT - Day 16 Project")
    print(f"{'='*70}\n")
    
    print("Select an option to run:\n")
    
    print("Documentation:")
    print("  1. View Agent Planning Concepts")
    print("  2. View Single vs Multi-Agent Comparison")
    print("  3. View Human-in-the-Loop Documentation")
    
    print("\nCore Demonstrations:")
    print("  4. Run Sequential Workflow")
    print("  5. Run Conditional Routing Tests")
    print("  6. Run Business Workflow (Complex Scenario)")
    print("  7. Run Structured Communication")
    
    print("\nAdvanced Features:")
    print("  8. Run Approval Manager Demo")
    print("  9. Run Retry Mechanism Demo")
    print("  10. Run Loop Protection Demo")
    print("  11. Run Execution Logger Demo")
    
    print("\nTesting & Evaluation:")
    print("  12. Run Multi-Agent Evaluation (20+ Tests)")
    print("  13. Run Agent Evaluation Report")
    
    print("\nAPI & Production:")
    print("  14. Start FastAPI Server")
    print("  15. Test API Endpoints")
    
    print("\n  0. Exit")
    print()


def run_menu_option(choice):
    """Run selected menu option."""
    try:
        if choice == "1":
            print_file("Day16_Agent_Planning.md")
        
        elif choice == "2":
            print_file("single_vs_multi_agent.md")
        
        elif choice == "3":
            print_file("human_in_the_loop.md")
        
        elif choice == "4":
            print("Running Sequential Workflow...\n")
            from workflows.sequential_workflow import run_sequential_example
            run_sequential_example()
        
        elif choice == "5":
            print("Running Conditional Routing Tests...\n")
            from workflows.conditional_workflow import test_router
            test_router()
        
        elif choice == "6":
            print("Running Complex Business Workflow...\n")
            from workflows.business_workflow import run_business_workflow
            run_business_workflow()
        
        elif choice == "7":
            print("Running Structured Communication...\n")
            from workflows.agent_communication import StructuredWorkflow
            workflow = StructuredWorkflow()
            workflow.run()
        
        elif choice == "8":
            print("Running Approval Manager Demo...\n")
            from core.approval import ApprovalManager
            manager = ApprovalManager()
            manager.request_approval("search_document")
            manager.request_approval("update_record")
            manager.request_approval("delete_document")
            manager.print_approval_summary()
        
        elif choice == "9":
            print("Running Retry Mechanism Demo...\n")
            from core.retry import RetryManager
            manager = RetryManager(max_retries=3, backoff_factor=0.1)
            result = manager.simulate_agent_failure()
            print(f"Result: {result}")
            manager.print_retry_summary()
        
        elif choice == "10":
            print("Running Loop Protection Demo...\n")
            from core.loop_protection import test_loop_protection
            test_loop_protection()
        
        elif choice == "11":
            print("Running Execution Logger Demo...\n")
            from core.agent_logger import test_logger
            test_logger()
        
        elif choice == "12":
            print("Running Multi-Agent Evaluation (20+ Tests)...\n")
            from tests.multi_agent_evaluation import run_evaluation
            results = run_evaluation()
        
        elif choice == "13":
            print("Generating Evaluation Report...\n")
            from tests.multi_agent_evaluation import MultiAgentEvaluation
            evaluator = MultiAgentEvaluation()
            results = evaluator.run_evaluation()
            evaluator.print_evaluation_results(results)
            evaluator.print_detailed_report()
        
        elif choice == "14":
            print("Starting FastAPI Server...\n")
            print("Install FastAPI first: pip install fastapi uvicorn")
            print("Then run: python -m uvicorn api.agent_api:app --reload")
            print("\nServer will be available at: http://localhost:8000")
            print("API Docs at: http://localhost:8000/docs")
        
        elif choice == "15":
            print("Testing API Endpoints...\n")
            test_api()
        
        elif choice == "0":
            print("Exiting...")
            return False
        
        else:
            print("Invalid option. Please try again.")
        
        return True
    
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("Please make sure all dependencies are installed: pip install -r requirements.txt")
        return True


def print_file(filename):
    """Print file contents."""
    try:
        with open(filename, 'r') as f:
            content = f.read()
            print(f"\n{'='*70}")
            print(content)
            print(f"\n{'='*70}\n")
    except FileNotFoundError:
        print(f"File {filename} not found.")


def test_api():
    """Test API endpoints."""
    print("Testing Multi-Agent API...\n")
    
    try:
        from api.agent_api import MultiAgentAPI, MessageRequest
        
        api = MultiAgentAPI()
        
        # Test health
        print("1. Testing /health endpoint...")
        health = api.health()
        print(f"   Status: {health.status}")
        print(f"   Version: {health.version}")
        print(f"   Agents Available: {health.agents_available}\n")
        
        # Test tools
        print("2. Testing /agent/tools endpoint...")
        tools = api.get_tools()
        print(f"   Total Tools: {tools['total']}")
        print(f"   Categories: {', '.join(tools['categories'])}\n")
        
        # Test chat
        print("3. Testing /agent/chat endpoint...")
        request = MessageRequest(
            message="What is the leave policy?"
        )
        response = api.chat(request)
        print(f"   Conversation ID: {response.conversation_id}")
        print(f"   Status: {response.status}")
        print(f"   Agents Used: {', '.join(response.agents_used)}\n")
        
        # Test status
        print("4. Testing /agent/status endpoint...")
        status = api.get_status(response.conversation_id)
        print(f"   Conversation Status: {status.status}")
        print(f"   Steps: {status.current_step}/{status.total_steps}\n")
        
        print("All tests completed successfully!")
    
    except ImportError as e:
        print(f"Cannot import API module: {str(e)}")
        print("Make sure all dependencies are installed.")
    except Exception as e:
        print(f"Error during API testing: {str(e)}")


def main():
    """Main entry point."""
    print("\n" + "="*70)
    print("MULTI-AGENT AI ASSISTANT - Day 16 Implementation")
    print("="*70)
    print("\nLoading project components...\n")
    
    # Verify structure
    required_dirs = [
        'agents', 'workflows', 'core', 'tests', 'api'
    ]
    
    all_present = all(Path(d).exists() for d in required_dirs)
    
    if all_present:
        print("✓ All project directories found")
        print("✓ Project structure verified\n")
    else:
        print("✗ Some project directories missing")
        print("Please ensure project structure is complete.\n")
        return
    
    # Main loop
    while True:
        print_menu()
        choice = input("Enter your choice (0-15): ").strip()
        
        if not run_menu_option(choice):
            break
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
