# GPT2 Project

An application to allow for generating news articles using [OpenAI](https://openai.com)'s [GPT-2 text generator](https://openai.com/blog/better-language-models/).

## Setup

This project uses [git-lfs](https://git-lfs.github.com/) due to the size of the model. Because of this you must install it before cloning the repository.

After you install git-lfs the repository can be cloned as normal:
```shell
git clone https://github.com/DanTm99/gpt2-project.git
```

Navigate into the folder:
```shell
cd gpt2-bot
```

Install the required packages:
```shell
pip3 install -r requirements.txt
```

To use this without GPU support use the following command instead:
```shell
pip3 install -r requirements-no-gpu.txt
```

## Usage

To use this with your GPU you must have and NVIDIA GPU with a CUDA Compute Capability 3.5 or higher.

If you have the required hardware you must install the required software on your system as shown [here](https://www.tensorflow.org/install/gpu#software_requirements).

To open the GUI use the following command:
```shell
python3 ArticleGenerator.py
```

This application can also be used via the command line. For detailed help use the following command:
```shell
python3 ArticleGenerator.py -h
```