# Contribution guidelines

First of all, thanks for thinking of contributing to this project. :smile:

Before sending a Pull Request, please make sure that you're assigned the task on a GitHub issue.

- If a relevant issue already exists, discuss on the issue and get it assigned to yourself on GitHub.
- If no relevant issue exists, open a new issue and get it assigned to yourself on GitHub.

Please proceed with a Pull Request only after you're assigned. It'd be sad if your Pull Request (and your hardwork) isn't accepted just because it isn't idealogically compatible.

# Developing the gem

1. Clone this repository and install all the required gem dependencies.

    ```sh
    git clone https://github.com/athityakumar/btp.git
    cd btp
    gem install bundler
    bundle install
    ```

2. Checkout to a different git branch (say, `adds-format-importer`).

3. Add tests to `spec/btp/language_spec.rb`.

4. Run the rspec test-suite.
    ```sh
    # Runs test suite for whole codebase
    bundle exec rspec
    ```

5. Run the rubocop for static code quality comments.

    ```sh
    # Runs rubocop test for whole codebase
    bundle exec rubocop
    ```

6. Send a Pull Request back to this repository. :tada:
