import os
import subprocess

def init():
    """
    Initializes the environment and retrieves information about NVIDIA GPUs.

    This function executes the 'nvidia-smi' command to query information about
    the available NVIDIA GPUs in the current environment. It prints the GPU names,
    total memory, and free memory in a comma-separated format without headers.

    The function is designed for use in Google Colab notebooks but can also work
    in other Jupyter environments.

    Note:
    - The 'nvidia-smi' command must be available in the environment to execute
      this function successfully.
    - If executed outside Google Colab, the function may not retrieve GPU
      information if 'nvidia-smi' is not available or GPUs are not present.

    Returns:
    None: The function prints the GPU information directly.

    Example:
    >>> init()
    GPU 0, Tesla K80, 11441 MiB, 11338 MiB
    GPU 1, Tesla K80, 11441 MiB, 11338 MiB
    GPU 2, Tesla K80, 11441 MiB, 11338 MiB
    """
    sub_p_res = subprocess.run(['nvidia-smi', '--query-gpu=name,memory.total,memory.free',
                                '--format=csv,noheader'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    print(sub_p_res)

def define_paths():
    """
    Asks the user to define paths for model and output directories.

    This function allows the user to specify local paths for model and output directories.
    Optionally, it provides the option to mount Google Drive and set specific directories on Google Drive
    for storing models and output files.

    Returns:
        None. The function creates the specified directories based on user input.

    Usage:
        - Run this function to define paths for model and output directories interactively in a Colab notebook.
        - The user can choose between local paths or mount Google Drive for storing data.
        - If Google Drive is mounted, the function will ask for specific directories on Google Drive.

    Parameters:
        None. The function uses Colab's special parameters (`@param`) to ask for user input.

    Example:
        >>> define_paths()
        Local Path Variables:
        ...
        models_path: /content/models
        output_path: /content/output
        ...
    """
    # @markdown **Model and Output Paths**
    # ask for the link
    print("Local Path Variables:\n")

    models_path = "/content/models"  # @param {type:"string"}
    output_path = "/content/output"  # @param {type:"string"}

    # @markdown **Google Drive Path Variables (Optional)**
    mount_google_drive = True  # @param {type:"boolean"}
    force_remount = False

    if mount_google_drive:
        from google.colab import drive  # type: ignore
        try:
            drive_path = "/content/drive"
            drive.mount(drive_path, force_remount=force_remount)
            # @param {type:"string"}
            models_path_gdrive = "/content/drive/MyDrive/AI/models"
            # @param {type:"string"}
            output_path_gdrive = "/content/drive/MyDrive/AI/StableDiffusion"
            models_path = models_path_gdrive
            output_path = output_path_gdrive
        except:
            print("...error mounting drive or with drive path variables")
            print("...reverting to default path variables")

    os.makedirs(models_path, exist_ok=True)
    os.makedirs(output_path, exist_ok=True)

    print(f"models_path: {models_path}")
    print(f"output_path: {output_path}")

def setup_environment():
    """
    Set up the environment with necessary packages and repositories.

    This function allows the user to install specific versions of PyTorch and other essential
    libraries required for the project. It also clones various GitHub repositories for
    additional code and resources. The function provides the option to print the output of
    each subprocess for better visibility.

    Parameters:
        None

    Returns:
        None

    Notes:
        The function uses Colab's special parameters (e.g., `@param`) to ask for user input
        related to setting up the environment.

    Example:
        >>> setup_environment()
        Setting up environment...
        Environment set up in X seconds
    """
    # @markdown **Setup Environment**
    setup_environment = True  # @param {type:"boolean"}
    print_subprocess = False  # @param {type:"boolean"}

    if setup_environment:
        import subprocess
        import time
        print("Setting up environment...")
        start_time = time.time()
        all_process = [
            ['pip', 'install', 'torch==1.12.1+cu113', 'torchvision==0.13.1+cu113',
                '--extra-index-url', 'https://download.pytorch.org/whl/cu113'],
            ['pip', 'install', 'omegaconf==2.2.3', 'einops==0.4.1', 'pytorch-lightning==1.7.4',
                'torchmetrics==0.9.3', 'torchtext==0.13.1', 'transformers==4.21.2', 'kornia==0.6.7'],
            ['git', 'clone', 'https://github.com/deforum/stable-diffusion'],
            ['pip', 'install', '-e',
                'git+https://github.com/CompVis/taming-transformers.git@master#egg=taming-transformers'],
            ['pip', 'install', '-e', 'git+https://github.com/openai/CLIP.git@main#egg=clip'],
            ['pip', 'install', 'accelerate', 'ftfy', 'jsonmerge',
                'matplotlib', 'resize-right', 'timm', 'torchdiffeq'],
            ['git', 'clone', 'https://github.com/shariqfarooq123/AdaBins.git'],
            ['git', 'clone', 'https://github.com/isl-org/MiDaS.git'],
            ['git', 'clone', 'https://github.com/MSFTserver/pytorch3d-lite.git'],
        ]
        for process in all_process:
            running = subprocess.run(
                process, stdout=subprocess.PIPE).stdout.decode('utf-8')
            if print_subprocess:
                print(running)

        print(subprocess.run(['git', 'clone', 'https://github.com/deforum/k-diffusion/'],
            stdout=subprocess.PIPE).stdout.decode('utf-8'))
        with open('k-diffusion/k_diffusion/__init__.py', 'w') as f:
            f.write('')

        end_time = time.time()
        print(f"Environment set up in {end_time-start_time:.0f} seconds")
