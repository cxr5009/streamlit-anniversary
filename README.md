# Anniversary Calculator

An easy-to-use Streamlit application to calculate and display anniversaries based on start dates. Ideal for organizations looking to track important milestones such as work anniversaries.

## Features

- **Add Individuals Manually**: Input names and start dates directly into the app.
- **Bulk Upload**: Upload a CSV file containing names and start dates for multiple individuals.
- **Select Anniversary Types**: Choose from predefined anniversary milestones (e.g., 1 Year, 5 Years).
- **Date Navigation**: Navigate between months to view anniversaries in different periods.
- **Data Overview**: View all added individuals and their start dates.
- **Session State Management**: Data persists during your session for seamless interaction.

## Installation

### Prerequisites

- Python 3.7 or higher
- [pip](https://pip.pypa.io/en/stable/installation/)

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/cxr5009/streamlit-anniversary.git
   cd streamlit-anniversary
   ```

2. **Create a Virtual Environment (Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the Streamlit app:

```bash
streamlit run st-anniversary.py
```

This will start the app, and you can access it in your web browser at `http://localhost:8501`.

## How to Use

### 1. Select Anniversary Types

- Use the multiselect widget at the top to choose which anniversary milestones you want to track (e.g., 1 Year, 5 Years).

### 2. Add People

- **Manually**: In the "Add people here" section, input the individual's name and start date.
- **Bulk Upload**: Upload a CSV file with columns `Name` and `Start Date` to add multiple individuals at once.

### 3. View Anniversaries

- The main section displays anniversaries for the selected month.
- Use the "Prev. Month," "Current Month," and "Next Month" buttons to navigate between months.
- Anniversaries matching your criteria will be displayed in a table.

### 4. View All People

- Expand the "People" section at the bottom to see a table of all individuals you've added.

## CSV File Format

When uploading a CSV file, ensure it follows this format:

- **Columns**: `Name`, `Start Date`
- **Date Format**: `YYYY-MM-DD` or any format recognized by pandas.

#### Example:

```csv
Name,Start Date
Alice Johnson,2019-06-23
Bob Smith,2023-09-15
John Doe,2023-11-01
```

## Dependencies

- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License.