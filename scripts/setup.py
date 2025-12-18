import subprocess
import sys
import time

COMPOSE_CMD = ["docker", "compose", "-f", "docker/compose.dev.yaml"]


def run_command(cmd):
    print(f"Executing: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def setup(server_only=False):
    try:
        # build app image and run docker container for postgres
        run_command([*COMPOSE_CMD, "up", "-d"])

        if not server_only:
            print("Running migrations and adding admin data...")

            # let postgres database run first
            print("Waiting for posgres...")
            time.sleep(5)

            # execute database migrations once
            run_command(
                [
                    *COMPOSE_CMD,
                    "exec",
                    "app",
                    "uv",
                    "run",
                    "python",
                    "scripts/migration.py",
                ]
            )

            # add one admin data to the database
            run_command(
                [
                    *COMPOSE_CMD,
                    "exec",
                    "app",
                    "uv",
                    "run",
                    "python",
                    "scripts/add_admin.py",
                ]
            )
        else:
            print("Starting fastapi server.")
        print("\nPress <CRTL+c> to stop the server and compose down docker containers")

        subprocess.run([*COMPOSE_CMD, "logs", "-f"])

    except KeyboardInterrupt:
        print("\nStopping server and cleaning containers...")
    except Exception as err:
        print(f"\nError: {err}")
    finally:
        subprocess.run([*COMPOSE_CMD, "down"])
        print("\n---Done---")


if __name__ == "__main__":
    fastapi_server = "--server-only" in sys.argv
    setup(server_only=fastapi_server)
