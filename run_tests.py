import sys
import subprocess
import os


def main():
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except AttributeError:
            pass
    print("🚀 Starting QuoteAI Test Suite...")
    print("=================================")
    print("\n📦 Running full test suite with pytest...")
    pytest_result = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"])
    if pytest_result.returncode == 0:
        print("\n✅ All tests passed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Check logs above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
