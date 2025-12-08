import sys
from src.main import run_workflow

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python Bora_Arda_Avci_YouTube_AI.py <url> <json|hash>")
        sys.exit(1)

    url = sys.argv[1]
    mode = sys.argv[2]

    try:
        output = run_workflow(url, mode)
        print(output)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
        