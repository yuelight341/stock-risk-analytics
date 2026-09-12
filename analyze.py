import subprocess
import sys

def run_step(command):
    cmd_str = ' '.join(command)
    print(f"\n{'='*60}")
    print(f"RUNNING: {cmd_str}")
    print(f"{'='*60}")
    
    try:
        subprocess.run([sys.executable] + command, check=True)
    except subprocess.CalledProcessError:
        print(f"\nERROR: Failed at step -> {cmd_str}")
        print("Fix the error above and try again.")
        sys.exit(1)

def main():
    user_args = sys.argv[1:]

    run_step(["get_data.py"] + user_args)

    run_step(["optimal_portfolio.py"])

    run_step(["run_queries.py"])

    run_step(["graphs.py"])

    print("\n" + "🥮"*30)
    print("🥮"*13 + "COMPLETE" + "🥮"*13)
    print("🥮"*30 + "\n")

if __name__ == "__main__":
    main()