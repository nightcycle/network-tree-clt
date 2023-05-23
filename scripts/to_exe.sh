source .env/Scripts/Activate
pyinstaller --onefile src/__init__.py -n network-tree --additional-hooks-dir=hooks --add-data "src/data/Packages.zip;data/"