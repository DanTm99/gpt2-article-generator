GPT2 Article Generator

An application to allow for generating news articles using OpenAI GPT-2 text generator.


Setup

The repository can be cloned as normal using this command:
git clone https://github.com/DanTm99/gpt2-article-generator.git

The model this program uses is hosted separately on Google Drive and can be downloaded from here: https://drive.google.com/open?id=1Lmh7JBRkbC0jEvGtoZwVL30PT8PIt9qm
The contents of this archive should be extracted to the "gpt2-article-generator" folder so that the "checkpoint" is in the "gpt2-article-generator" folder.

Navigate into the folder using this command:
cd gpt2-article-generator

To use this with your GPU you must have and NVIDIA GPU with a CUDA Compute Capability 3.5 or higher.
If you have the required hardware you must install the required software on your system as shown here: https://www.tensorflow.org/install/gpu#software_requirements

Install the required packages as normal to use this with GPU support using this command:
pip3 install -r requirements.txt

To use this without GPU support use the following command instead using this command:
pip3 install -r requirements-no-gpu.txt


Usage

To open the GUI use the following command:
python3 ArticleGenerator.py

This application can also be used via the command line. For detailed help use the following command:
python3 ArticleGenerator.py -h
