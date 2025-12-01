# Manadash
 
![image](https://github.com/user-attachments/assets/fea1fc56-4efb-4e40-b72a-a68ebde8936f)


[Manadash](https://www.manadash.app/entry_screen) is a web application built with Flask that integrates interactive Dash applications for data visualization. It features user authentication, responsive design with Bootstrap, and custom backend functionality for managing player data. The project is designed to provide an engaging and intuitive interface for users to interact with various datasets and dashboards. You can take a look here: https://www.manadash.app/

## Features

- **Dash Integration**: Interactive dashboards for "commander" and "vintage" applications.
- **Bootstrap Styling**: Responsive, mobile-first design using Bootstrap.
- **Modular Routing**: Clear separation of routes and functionalities for easier maintenance.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/GuySchnidrig/ManaDash.git
    cd ManaDash
    ```

2. **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the application**:
    ```bash
    python routing.py
    ```

    By default, the application runs on `http://0.0.0.0:5000`.

# Project Structure
```bash
manadash/
├── app.py                    # Main Flask application
├── backend/
│   └── player.py             # Backend functions for player management
├── dash_application_commander.py   # Dash application for commander dashboard
├── dash_application_vintage.py     # Dash application for vintage dashboard
├── templates/
│   ├── login.html            # Login page template
│   └── entry_screen.html     # Entry screen template
├── static/                   # Static files (CSS, JS, images)
└── requirements.txt          # Python dependencies

```
## Usage

- **Dashboards**: Access the commander and vintage dashboards from their respective routes once logged in.

## Deployment

To deploy Manadash in a production environment, make sure to:
- Update Flask's debug mode to `False`.
- Configure the server to run on a production-ready WSGI server such as Gunicorn or uWSGI.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the contributors and the open-source community for their support and inspiration.
- [Flask](https://flask.palletsprojects.com/) - The web framework used.
- [Dash](https://dash.plotly.com/) - For creating interactive dashboards.

---

Feel free to reach out if you have any questions or suggestions!
