from supervisor import supervisor

def run_test(query, expected_agent, description):
    print(f"\n--- Test: {description} ---")
    print(f"Query: {query}")
    result = supervisor(query)
    print(f"Answer: {result['answer']}")
    return result

if __name__ == "__main__":
    # Test 1: Clear text/document question -> should go to Search Agent
    run_test(
        "What was the revenue growth?",
        "search",
        "Text question should route to Search Agent and answer correctly"
    )

    # Test 2: Clear image/chart question -> should go to Vision Agent
    run_test(
        "Show me the sales chart",
        "vision",
        "Image question should route to Vision Agent"
    )

    # Test 3: Unanswerable text question -> Search Agent should refuse gracefully
    run_test(
        "What is the CEO's name?",
        "search",
        "Unanswerable question should not hallucinate"
    )

    # Test 4: Empty query -> should not crash
    try:
        run_test("", "search", "Empty query should not crash the system")
    except Exception as e:
        print(f"System crashed on empty query: {e}")

    # Test 5: Very long/nonsense query -> should not crash
    run_test(
        "asdkj askjd " * 20,
        "search",
        "Long nonsense query should not crash the system"
    )