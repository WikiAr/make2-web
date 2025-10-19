#!/bin/bash
TOKEN="${1:-}"

if [ -z "$TOKEN" ]; then
    echo "Usage: $0 <TOKEN>"
    exit 1
fi

BRANCH="${2:-main}"

echo ">>> clone --branch ${BRANCH} ."

REPO_URL="https://MrIbrahem:${TOKEN}@github.com/MrIbrahem/ma_lists.git"

TARGET_DIR="$HOME/www/python/bots/ma_lists"

if [ ! -d "$TARGET_DIR" ]; then
    mkdir -p "$TARGET_DIR"
    echo "Directory created: $TARGET_DIR"
    chmod 770 "$TARGET_DIR"
else
    echo "Directory already exists: $TARGET_DIR"
fi

CLONE_DIR="$HOME/maalist_x"

# Navigate to the project directory
cd $HOME || exit

# Remove any existing clone directory
rm -rf "$CLONE_DIR"

# Clone the repository
if git clone --branch "$BRANCH" "$REPO_URL" "$CLONE_DIR"; then
    echo "Repository cloned successfully."
else
    echo "Failed to clone the repository." >&2
    exit 1
fi

#cp "$CLONE_DIR/requirements.in" "$TARGET_DIR/requirements.in" -v

# Optional: remove any non-Python files
# find "$CLONE_DIR" -type f ! -name "*.py" -exec rm -rf {} \;

# Copy the required files to the target directory
# cp -rf "$CLONE_DIR/"* "$TARGET_DIR/" -v

if [ -d "$CLONE_DIR/src" ]; then
    cp -rf "$CLONE_DIR/src/"* "$TARGET_DIR/" -v
else
    cp -rf "$CLONE_DIR/"* "$TARGET_DIR/" -v
fi

# Optional: Set permissions
# chmod -R 770 "$TARGET_DIR"
find "$TARGET_DIR" -type f ! -name "*.pyc" -exec chmod 770 {} -v \;
find "$TARGET_DIR" -type f -name "*.pyc" -exec rm -rf {} -v \;

# Optional: Install dependencies
#"$HOME/local/bin/python3" -m pip install -r "$TARGET_DIR/requirements.in"

# Remove the "$CLONE_DIR" directory.
rm -rf "$CLONE_DIR"
