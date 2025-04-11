import subprocess
import os

# Get the root folder of the project
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# List of scripts to run in order (only one needed in your current setup)
scripts = [
    os.path.join(base_dir, "scripts", "hr_first_filtered_workflow.py")
]

# Run each script
for script in scripts:
    print(f"\n🚀 Running: {script}")
    try:
        subprocess.run(["python", script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error while running {script}:")
        print(e)

print("\n✅ All scripts completed successfully.")
