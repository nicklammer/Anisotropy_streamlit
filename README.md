# Anisotropy/Polarization Fitting and Plotting

A Streamlit app for fitting and plotting fluorescence anisotropy and polarization binding data.

## Getting Started

The easiest way to run this app is with Docker Desktop.

### 1. Install Docker Desktop

Download and install Docker Desktop for your operating system:
- **Mac**: https://docs.docker.com/desktop/install/mac-install/
- **Windows**: https://docs.docker.com/desktop/install/windows-install/

Open Docker Desktop and let it finish starting up before continuing.

### 2. Pull the image

In Docker Desktop, open the built-in terminal by clicking the **Terminal** button in the bottom bar. Copy the command below, paste it into the terminal, and press Enter.

- **Mac**: `Cmd + V` to paste
- **Windows**: `Ctrl + Shift + V` to paste

```
docker pull ghcr.io/nicklammer/anisotropy_streamlit/anisotropy_streamlit:latest
```

This downloads the app image. You only need to do this once (or again later to get updates). It will use about 1.2 GB of space.

### 3. Run the container

In Docker Desktop, go to the **Images** tab, find `anisotropy-streamlit`, and click **Run**.

In the dialog that appears, expand **Optional settings** and set:
- **Host port**: `8501`

Click **Run**. The container will start.

Open your browser and go to:
```
http://localhost:8501
```

### 4. Stop the container

In Docker Desktop, go to the **Containers** tab, find the running container, and click the **Stop** button (square icon). You can start it again from the same tab whenever you need it.


## Usage

Each page has a help button in the top-right corner that displays instructions for use. You can also refer to the `docs/` folder above.