# RPG Name Genie
# RPG Name Generator

[![Version](https://img.shields.io/badge/Version-2.0.0.21-brightgreen.svg)](https://github.com/yourusername/your-repo)
[![Maintenance](https://img.shields.io/badge/Maintained-Actively%20Maintained-blue.svg)](https://github.com/yourusername/your-repo)

Generate captivating and immersive names for your RPG characters effortlessly. Unleash your imagination and enhance your storytelling with unique and fitting names.

## Usage

1. Clone the repository to your local environment.
2. Ensure you have PHP installed.
3. Import the included SQLite database or create your own using the provided data.
   - **Importing the Included Database:**
     - Locate the included `namegen_names.db` file in the repository.
     - Use a tool like [SQLiteStudio](https://sqlitestudio.pl/) or the SQLite command-line utility to import the database. For example, using the SQLite command-line:
       ```bash
       sqlite3 namegen_names.db < namegen_names.sql
       ```
4. Update the database connection configuration in `config.php`.
5. Start the PHP development server: `php -S localhost:8000`.
6. Access the RPG Name Generator at `http://localhost:8000/index.php`.
7. Choose the gender and click "Generate" to obtain a character name.
8. Optional: Add more names to the database using the "Add Names to the Database" link.

## Dependencies

- PHP (>= 7.0)
- SQLite3 extension for PHP

## Contributing

We welcome contributions to improve this RPG Name Generator. Please follow our [contribution guidelines](CONTRIBUTING.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Disclaimer:** Always respect privacy and copyrights when adding names to the database. This tool is for personal and non-commercial use.
