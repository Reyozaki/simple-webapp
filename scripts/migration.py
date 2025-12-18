import subprocess
import sys


def main() -> None:
    try:
        result = subprocess.run(
            ["uv", "run", "alembic", "upgrade", "head"],
            cwd=".",
            check=True,
            capture_output=True,
            text=True,
        )
        print(result.stdout)
    except subprocess.CalledProcessError as err:
        print(f"Error: {err.stderr}")
    except Exception as err:
        print(f"Error occurred: {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
