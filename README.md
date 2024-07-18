
# Fooocus Lightning AI

**Fooocus Lightning AI** is a sophisticated project developed to significantly enhance focus and productivity through the use of advanced AI technologies. This repository provides comprehensive setup and configuration instructions for deploying and running the Fooocus AI system efficiently.

## Table of Contents

- [Installation](#installation)
- [Model Downloads](#model-downloads)
  - [Loras Models](#loras-models)
  - [Checkpoints](#checkpoints)
- [Troubleshooting](#troubleshooting)
  - [Fooocus UI Blank Error](#fooocus-ui-blank-error)

## Installation

To get started with Fooocus Lightning AI, please follow the steps below:

### 1. Clone the Repository

Begin by cloning the repository to your local machine. Open your terminal and execute:

```sh
git clone https://github.com/epic-miner/fooocus-lightning-ai.git
cd fooocus-lightning-ai
```

This command will create a local copy of the repository and navigate you into the project directory.

### 2. Start the Application

Next, initiate the application by running the provided startup script:

```sh
sh start.sh
```

This script will set up the necessary environment and launch the Fooocus AI system. Monitor the terminal for any prompts or error messages during this process.

## Model Downloads

To fully utilize Fooocus Lightning AI, you need to download various models. Follow the instructions below based on the type of model you need:

### Loras Models

To download Loras models, navigate to the `models/loras` directory:

```sh
cd fooocus-lightning-ai/Fooocus/models/loras
```

Here you will find instructions or scripts to download the Loras models required for the system.

### Checkpoints

For downloading checkpoints, move to the `models/checkpoints` directory:

```sh
cd fooocus-lightning-ai/Fooocus/models/checkpoints
```

This directory contains the necessary checkpoint files. Follow the provided guidelines or scripts for downloading these files.

## Troubleshooting

If you experience issues with the Fooocus user interface, such as a blank screen, follow these troubleshooting steps to resolve the problem:

### Fooocus UI Blank Error

1. **Update the Repository**

   Ensure you have the latest version of the repository by updating it:

   ```sh
   cd fooocus-lightning-ai/
   git fetch origin main   # Fetch the latest changes from the remote main branch
   git merge origin/main   # Merge the fetched changes into your current branch
   ```

   This will synchronize your local repository with the latest updates.

2. **Restart the Application**

   After updating, restart the application:

   ```sh
   sh start.sh
   ```

   Allow some time for the application to restart and confirm if the issue persists.

3. **Open a New Terminal**

   If the UI issue continues, open a new terminal window.

   ![Fooocus Web UI](https://github.com/epic-miner/image/blob/main/Screenshot%202024-07-18%20124725.png)

4. **Run the Cloudflared Command**

   Execute the following command to establish a tunnel:

   ![Fooocus Command](https://github.com/epic-miner/image/blob/main/Screenshot%202024-07-18%20124827.png)
   ```sh
   cloudflared tunnel --url localhost:7865
   ```

   This command will create a secure tunnel to the local server.

5. **Access the Fooocus Web UI**

   After running the command, scroll through the terminal output to find a URL. Click on this URL to access the Fooocus web UI.

   ![Fooocus Web UI](https://github.com/epic-miner/image/blob/main/Screenshot%202024-07-18%20101016.png)

   If you encounter any additional issues, refer to the documentation or reach out to the support team for further assistance.
