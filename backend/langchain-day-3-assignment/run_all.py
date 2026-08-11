"""Run all LangChain Day-3 assignment demos."""

from assignment1_confused_agent_routing import main as run_assignment_1
from assignment2_agent_resilience import main as run_assignment_2
from assignment3_lost_context_rag import main as run_assignment_3


if __name__ == "__main__":
    print("=" * 80)
    run_assignment_1()
    print("=" * 80)
    run_assignment_2()
    print("=" * 80)
    run_assignment_3()
