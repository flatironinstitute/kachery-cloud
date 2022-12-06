## Conda environments

A conda environment is a separate and isolated working space that allows you to have different versions of Python or other packages installed on your system without affecting the other environments. You can use conda environments to easily switch between different projects that have different package requirements.

To create a new conda environment with Python, you can use the following command:

```bash
conda create --name my_env python=3.9
```

This will create a new conda environment called "my_env". To activate this environment, you can use the following command:

```bash
conda activate my_env
```

Once the environment is activated, you can use the conda command to install packages into the environment, for example:

```bash
conda install numpy
```

You can also use pip to install Python packages within the isolated environment.

This will install the numpy package into the environment. To deactivate the environment, you can use the following command:

```bash
conda deactivate
```

And to delete the environment, you can use the following command:

```bash
conda env remove --name my_env
```

This will remove the "my_env" environment from your system.

## Installing Miniconda in Linux

To install Miniconda on Linux, you can follow these steps:

Open a terminal and download the Miniconda installer by running the following command:

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

Make the downloaded shell script executable by running the following command:

```bash
chmod +x Miniconda3-latest-Linux-x86_64.sh
```

Run the installer by using the following command:

```bash
./Miniconda3-latest-Linux-x86_64.sh
```

Follow the instructions in the installer to complete the installation process.

Once the installation is complete, you can verify that Miniconda has been installed successfully by running the conda command in the terminal. This should display the list of available conda commands. You can also use the `conda --version` command to check the version of Miniconda that you have installed.

> This page was created with help from OpenAI