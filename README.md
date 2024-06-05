# soccer-stonks
or just call it RON STONKSS

![Alt text](imgs/rondoGuy.png)

## Setting up the Virtual Enviroments

 **Create a Virtual Environment:**
    ```
    python -m venv venv
    ```
### Windows

 **Activate the Virtual Environment:**
    ```
    .\venv\Scripts\activate
    ```

### macOS

**Activate the Virtual Environment:**
    ```
    source venv/bin/activate
    ```

### Installing Dependencies

Once the virtual environment is activated, install the required dependencies:
```
pip install -r requirements.txt
```

- To run kedro `kedro run`
- To run streamlit `streamlit run streamlit_app.py`

## How to work with Kedro and notebooks

> Note: Using `kedro jupyter` or `kedro ipython` to run your notebook provides these variables in scope: `catalog`, `context`, `pipelines` and `session`.
>
> Jupyter, JupyterLab, and IPython are already included in the project requirements by default, so once you have run `pip install -r requirements.txt` you will not need to take any extra steps before you use them.

### Jupyter
To use Jupyter notebooks in your Kedro project, you can start a local notebook server:

```
kedro jupyter notebook
```

### JupyterLab
To use JupyterLab:

```
kedro jupyter lab
```

### IPython
And if you want to run an IPython session:

```
kedro ipython
```
