import subprocess
import os
class PipelineManager:
    """Manages and executes the data processing pipeline steps."""

    def __init__(self):
        self.steps = [
            os.path.abspath(os.path.join(os.path.dirname(__file__), "../pipeline/discard_non_valid.py")),
            os.path.abspath(os.path.join(os.path.dirname(__file__), "../pipeline/discard_bad_words.py")),
            os.path.abspath(os.path.join(os.path.dirname(__file__), "../pipeline/discard_internal_redundant.py")),
            os.path.abspath(os.path.join(os.path.dirname(__file__), "../pipeline/discard_external_redundant.py")),
            os.path.abspath(os.path.join(os.path.dirname(__file__), "../pipeline/discard_commercial_activities.py")),
            os.path.abspath(os.path.join(os.path.dirname(__file__), "../pipeline/discard_crafts.py")),
            os.path.abspath(os.path.join(os.path.dirname(__file__), "../pipeline/generate_final_output.py")),

        ]

    def run_step(self, script_name):
        """Runs a Python script as a subprocess and prints the output."""
  
        result = subprocess.run(["python", script_name], capture_output=True, text=True)

        if result.returncode == 0:
            pass
        else:
            pass

    def run_pipeline(self):
        """Executes all steps of the data processing pipeline in order."""
        for step in self.steps:
            self.run_step(step)

        
# Run the pipeline
if __name__ == "__main__":
    manager = PipelineManager()
    manager.run_pipeline()
