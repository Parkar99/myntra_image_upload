# Upload images to Myntra (unstable)

### `config.py` constants
`EMAIL = 'email'`  
`PASS = 'pass'`  
`DIR = 'directory_with_images'`  
`BRAND = 'brand_name_as_on_myntra'`  

- Make sure the directory in `DIR` is at the same level as the `app.py` file. Each SKU should be in it's own folder. Folder names are used as SKU names in the **VAN** field.
- Make sure brand name in `BRAND` is exactly as on Myntra.

### `color_list.json` (will be created when run)

Contains array of strings of color names to choose from.

### `progress.log` (will be created when run)

Logs each SKU when done in case of failure.

### Setup

- Install dependencies via the Pipfile using pipenv
- Make sure you have the chrome driver for selenium. [More info](https://selenium-python.readthedocs.io/installation.html)
- Works with Chrome only. You'll have to manually change the driver to use another browser if you so wish.