If you're installing this app on a new server:

1. Navigate to where you want the repository
2. Download it by running: 
    git clone https://github.com/levavft-eam/The-Premian-AI-API.git
3. Navigate into the repository by running:
    cd The-Premian-AI-API
4. Check if conda/ miniconda are installed by running:
    conda
5. Install conda if it isn't installed
6. check if ffmpeg is installed by running:
    ffmpeg
7. Install ffmpeg if it isn't installed by running:
    sudo apt install ffmpeg
8. Create a new conda environment by running:
    conda create --name the-premium-ai-api
9. Activate the environment by running:
    conda activate the-premium-ai-api
10. Install pip for conda by running:
    conda install pip
11. Install all the requirements for this app by running:
    pip install -r requirements.txt
12. Copy the '.env' file manually from a different installation, as it can't be commited to git (sensitive information). Make sure to put it directly inside The-Premian-AI-API.
    If you're in a production environment, make sure 'ENV=prod' is in .env and not 'ENV=dev'.


If you're running this app in development (debug) mode:

1. Activate the conda environment by running:
    conda activate the-premium-ai-api
2. Run in development (debug) mode with:
    flask --app src/app.py run

If you're running this app in production mode:

1. Activate the conda environment by running:
    conda activate the-premium-ai-api
2. Run in production mode:
    gunicorn -w 4 src.app:app

Extra gunicorn flags:
    --reload: Restart workers when code changes.

List running gunicorn process:
    ps aux | grep -v grep | grep -E "(gunicorn|PID)"

List PID's only of running gunicorn process:
    ps aux | grep -v grep | grep -E "gunicorn" | awk '//{print $2}'

Kill the gunicorn process:
    pkill gunicorn



Links that may help improve this project:
https://github.com/bajcmartinez/flask-api-starter-kit/tree/master
https://auth0.com/blog/best-practices-for-flask-api-development/