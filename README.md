## Google Colab Run Instructions
Google colab doesn't run docker natively. There's ways to just run `udocker`, but even then, `--allow-root` may create issues. Instead, we assume the colab environment is like a docker container itself and just install the package directly via the following instructions:
```
%%bash

git clone https://github.com/mewvim/csiro-biomass.git
cd csiro-biomass
uv pip install -e .
csiro dataset --download testrun
```
