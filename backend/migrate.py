import os
import sys
import subprocess

def run_migrations():
    """Run database migrations using Alembic"""
    print("Running database migrations...")
    
    # Check environment
    environment = os.getenv("FLASK_ENV", "development")
    
    if environment == "development":
        # Development: Auto-generate migrations if none exist
        versions_dir = os.path.join('migrations', 'versions')
        if not os.path.exists(versions_dir) or len(os.listdir(versions_dir)) == 0:
            print("Creating initial migration...")
            subprocess.run([sys.executable, '-m', 'alembic', 'revision', '--autogenerate', '-m', 'Initial migration'])
    else:
        # Production: Only run existing migrations, never auto-generate
        print("Production environment detected, running existing migrations only")
    
    # Run the migrations (both environments)
    subprocess.run([sys.executable, '-m', 'alembic', 'upgrade', 'head'])
    print("Migrations completed successfully!")

if __name__ == "__main__":
    run_migrations()