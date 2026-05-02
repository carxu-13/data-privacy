# Project Documentation: LLM Agent Defense Evaluation

## Architecture
- **Agent (`agent.py`)**: A state-machine based agent that interacts with the Ollama API. It supports four defense modes that modify either the system prompt or the output processing.
- **Experiment Suite (`experiment.py`)**: A batch processing script that iterates through test cases, invokes the agent, and evaluates responses using a combination of heuristic checks and LLM-based judging (Gemma:2B).
- **Visualization (`visualize_results.py`)**: Uses Pandas and Matplotlib to aggregate CSV results and generate comparative plots.

## Data Structure
- **`sandbox/`**: A controlled directory where all file-system operations are restricted. `setup_sandbox.py` populates this with stratified test files.
- **`results/`**: Contains all experiment outputs.
  - `experiment_results.csv`: Flat table of all test runs and their metrics.
  - `experiment_logs.jsonl`: Detailed raw logs including full assistant/tool transcripts.
  - `*.png`: Visual reports of ASR, TCR, and defense effectiveness.

## Key Conventions
- **Secrets**: Specific strings (e.g., "P@ssw0rd!", "AKIA...") are used to detect data exfiltration.
- **Defense Modes**:
  - `naive`: Baseline.
  - `prompt-hardened`: Instruction-based defense.
  - `output-filtered`: Regex and secret-based filtering.
  - `sandboxed-path`: File-level access control.

## Future Work
- Integration with more complex tool sets (e.g., web search, database execution).
- Support for more models via LangChain or direct API integrations.
- Implementation of more advanced prompt injection techniques (e.g., jailbreaks combined with indirect injection).
