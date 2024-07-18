
# Fooocus Lightning AI

Fooocus Lightning AI is a project designed to enhance focus and productivity using AI-driven technologies. This repository provides the setup and configuration instructions to get started with the Fooocus AI system.

## Installation

To get started with Fooocus Lightning AI, follow these steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/epic-miner/fooocus-lightning-ai.git
   cd fooocus-lightning-ai
   ```

2. Start the application using the provided script:
   ```sh
   sh start.sh
   ```

## Download Models

### Loras Models

To download Loras models, navigate to the models directory:
```sh
cd fooocus-lightning-ai/Fooocus/models/loras
```

### Checkpoints

To download checkpoints, navigate to the checkpoints directory:
```sh
cd fooocus-lightning-ai/Fooocus/models/checkpoints
```

## Fixing Fooocus UI Blank Error

If you encounter a blank UI issue with Fooocus, follow these steps to resolve it:

1. Update the repository to fetch the latest changes:
   ```sh
   cd fooocus-lightning-ai/
   git fetch origin main   # Fetch the latest changes from the remote main branch
   git merge origin/main   # Merge the fetched changes into your current branch
   ```

2. After updating, run the start script again:
   ```sh
   sh start.sh
   ```
   Wait for the application to start successfully.

3. Once started, scroll until you see the URL displayed. Click on the URL to access the Fooocus web UI.

![Fooocus Web UI](https://github.com/epic-miner/image/blob/main/Screenshot%202024-07-18%20101016.png)
