# LLM Agent Defense Evaluation Framework

This repository contains a framework for evaluating and benchmarking defenses against **Indirect Prompt Injection** and **Data Exfiltration** in LLM-based agents. It was developed as part of a research project on data privacy and security in autonomous agents.

## Project Overview

LLM agents with tool-use capabilities are vulnerable to instructions embedded within the data they process. This project implements a modular agent and a suite of stratified test cases to evaluate four distinct defense strategies across different models.

### Key Components

- **`agent.py`**: A core agent implementation supporting multiple defense modes and tool-calling logic.
- **`experiment.py`**: An automated evaluation suite that runs multiple test cases across defense modes and models.
- **`visualize_results.py`**: Tools for processing experiment logs and generating performance visualizations.
- **`setup_sandbox.py`**: Script to initialize a controlled environment with benign and adversarial files.

## Defense Mechanisms

The framework evaluates the following defense strategies:

1.  **Naive**: No additional security measures.
2.  **Prompt-Hardening**: Explicit system instructions to treat tool-provided data as untrusted.
3.  **Output-Filtering**: Real-time scanning of agent responses for secret leakage or unauthorized tool access.
4.  **Sandboxed-Path (Allowlisting)**: Strict path validation and file-level access control lists (ACLs).

## Installation

### Prerequisites

- Python 3.8+
- [Ollama](https://ollama.com/) (for running local models)

### Setup

1.  Clone the repository:
    ```bash
    git clone [github.com/carxu-13/data-privacy](https://github.com/carxu-13/data-privacy)
    cd data-privacy
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Ensure Ollama is running and pull the required models:
    ```bash
    ollama pull gemma:2b
    ollama pull llama3
    ```

4.  Initialize the sandbox:
    ```bash
    python setup_sandbox.py
    ```

### Running the Interactive Agent

You can test the agent manually using:
```bash
python agent.py
```
Use `/mode [defense_name]` to switch between defenses.

### Running Experiments

To run the full evaluation suite:
```bash
python experiment.py
```
This will generate `experiment_results.csv` and detailed logs in `experiment_logs.jsonl`.

### Visualizing Results

To generate summary reports and plots:
```bash
python visualize_results.py
```
This produces:
- `experiment_results.png`: Comparison of security (ASR) vs. utility (TCR).
- `attack_type_breakdown.png`: Performance across different attack vectors (Role Override, Chained Reads, etc.).

## Evaluation Metrics

We use four primary metrics to evaluate the effectiveness of defenses:

- **ASR (Attack Success Rate)**: Frequency of successful secret disclosure.
- **TCR (Task Completion Rate)**: Rate of successful completion for benign tasks (Utility).
- **PCR (Protected Access Rate)**: How often the agent attempts to access restricted files.
- **UDR (Unauthorized Disclosure Rate)**: Rate of sensitive data entering the agent's context.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
