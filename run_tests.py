import subprocess
import sys


def main() -> None:
    print("Starting QuoteAI test suite")
    print("=" * 40)
    result = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"])
    if result.returncode == 0:
        print("All tests passed")
        sys.exit(0)

    print("Some tests failed. Check logs above.")
    sys.exit(1)


if __name__ == "__main__":
    main()
