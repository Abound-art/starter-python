# ABOUND Starter Repo - Python

This is a starter repository for an ABOUND algorithm written in [Python](https://www.python.org/).

* Unsure on what ABOUND is? Check out https://abound.art
* Looking for another language? Check out our other options for starter repos [here](https://abound.art/artists)
* New to Python? Get started [here](https://www.python.org/about/gettingstarted/).

## What is in this repo

This repo includes all of the scaffolding to build an algorithm for ABOUND. That means:

1. Reading in the JSON configuration for a run
2. Generating art (using a [Lorenz attractor](https://en.wikipedia.org/wiki/Lorenz_system) as an example)
3. Writing the output to a file

In short, this repo does everything except implement your art algorithm, which
will generally look like this:

```python
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from PIL import Image

@dataclass_json
@dataclass
class Config:
	"""Class for holding configuration for a single algo run."""
	beta: float
	rho: float
	sigma: float
	dt: float
	iterations: int
	result_size: int

def run(cfg: Config) -> Image:
  # Your algorithm goes here
```

## Run locally + Testing your code

```bash
export ABOUND_CONFIG_PATH=example_input.json
export ABOUND_OUTPUT_PATH=output.png
python3 main.py
```

Will generate a piece of art at `output.png` that looks like this:

![An example output of the Lorenz attractor algorithm, a blue and green spiral](/example_output.png)

To start implementing your algorithm, replace the `Config` struct and `run`
function in [`algo.py`](/algo.py) with your own. It's also worth noting
that the example algorithm produces raster images, meaning they're made of
pixels and are output as [PNG](https://en.wikipedia.org/wiki/PNG) files, but
you can also write algorithms that produce vector images, meaning they're made
of geometric shapes and are output as
[SVG](https://en.wikipedia.org/wiki/SVG) files.

### As a Docker container

To test the algorithm in a Docker container, run:

```bash
./scripts/build_image.sh
./scripts/run_image.sh <config path> <output path>
```

Where `<config path>` defaults to `example_input.json` and `<output path>`
defaults to `output.png`.

## Packaging for Deployment

Algorithms are uploaded to ABOUND as Docker containers. The example algo can be
built by running:

```bash
./scripts/build_image.sh
```

Which will build the example image and tag it `abound-starter-python`.

## Deploying on ABOUND 

Head to https://abound.art/artists for the most recent instructions on how to upload
your algorithm once it is written. Make sure to read through the constraints carefully
to make sure that your algorithm conforms to them prior to submission.

Once you're ready to upload, tag and push the image with:

```bash
docker tag <local tag> <image name given by ABOUND>
docker push <image name given by ABOUND>
```

If you haven't changed the example configuration in this repo, the `<local
tag>` defaults to `abound-starter-python`.

The `docker push` command will fail if you aren't already authenticated with
your ABOUND credentials.
