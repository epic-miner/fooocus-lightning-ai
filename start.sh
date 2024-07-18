#!/bin/bash

# Set this variable to false to ensure installation in permanent storage.
install_in_temp_dir=false

# Check if the Fooocus repository exists, if not clone it
if [ ! -d "Fooocus" ]
then
  git clone https://github.com/lllyasviel/Fooocus.git
fi
cd Fooocus
git pull

# Set the installation folder
echo "Installation folder: ~/.conda/envs/fooocus"
if [ -L ~/.conda/envs/fooocus ]
then
  rm ~/.conda/envs/fooocus
fi

eval "$(conda shell.bash hook)"

# Check if the conda environment already exists
if conda info --envs | grep -q '^fooocus'; then
    echo "The fooocus environment already exists. Skipping installation."
else
    echo "Installing"
    conda env create -f environment.yaml
    conda activate fooocus
    pwd
    ls
    pip install -r requirements_versions.txt
    pip install torch torchvision --force-reinstall --index-url https://download.pytorch.org/whl/cu117
    pip install opencv-python-headless
    
    # Install ngrok
    pip install pyngrok
    
    # Install openssh for pinggy
    #conda config --add channels conda-forge
    #conda config --set channel_priority strict
    #conda install openssh -y
    
    # Install zrok
    #mkdir /home/studio-lab-user/zrok
    #wget https://github.com/openziti/zrok/releases/download/v0.4.23/zrok_0.4.23_linux_amd64.tar.gz -O /home/studio-lab-user/zrok/zrok.tar.gz
    #tar -xvf /home/studio-lab-user/zrok/zrok.tar.gz -C /home/studio-lab-user/zrok
    #chmod a+x /home/studio-lab-user/zrok/zrok 
    
    rm -f /opt/conda/.condarc
    conda install -y conda-forge::glib
    rm -rf ~/.cache/pip

    # Download and setup Cloudflared
    wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O cloudflared
    chmod +x cloudflared
    sudo mv cloudflared /usr/local/bin/
fi

# Removed the section for configuring checkpoints-real-folder
# Because the file manager in Sagemaker Studio Lab ignores the folder called "checkpoints"
# we need to move checkpoint files into a folder with a different name
# current_folder=$(pwd)
# model_folder=${current_folder}/models/checkpoints-real-folder
# if [ ! -e config.txt ]
# then
#   json_data="{ \"path_checkpoints\": \"$model_folder\" }"
#   echo "$json_data" > config.txt
#   echo "JSON file created: config.txt"
# else
#   echo "Updating config.txt to use checkpoints-real-folder"
#   jq --arg new_value "$model_folder" '.path_checkpoints = $new_value' config.txt > config_tmp.txt && mv config_tmp.txt config.txt
# fi

# If the checkpoints folder exists, move it to the new checkpoints-real-folder
# if [ ! -L models/checkpoints ]
# then
#     mv models/checkpoints models/checkpoints-real-folder
#     ln -s models/checkpoints-real-folder models/checkpoints
# fi

conda activate fooocus
cd ..
if [ $# -eq 0 ]
then
  python Fooocus/entry_with_update.py --always-high-vram & cloudflared tunnel --url localhost:7865
elif [ $1 = "reset" ]
then
  python Fooocus/entry_with_update.py --always-high-vram --reset & cloudflared tunnel --url localhost:7865
fi
