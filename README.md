
# Switch Screenshot Downloader

This is a tool for automatically downloading images uploaded to Twitter from a
Nintendo Switch (although it works for all images, but is specifically designed
for Switch screenshots).

Since the Switch uploads screenshots as JPEGs, the tool assumes all images are
JPEGs.

## What You'll Need

- A Twitter account (personally I use a separate account just for screenshots)
- A set of Twitter API keys, as described [here][api_keys]

## Installation

1. [Download the tool as a ZIP][download] and unzip
2. `pip install -r requirements.txt`
3. Set your API keys as environment variables: `SSDL_CONSUMER_KEY`,
   `SSDL_CONSUMER_SECRET`, `SSDL_ACCESS_TOKEN_KEY`, `SSDL_ACCESS_TOKEN_SECRET`
4. `python switch_dl.py your_username /path/to/screenshots/directory`

## Command Line Arguments

`python switch_dl.py your_username /path/to/screenshots/directory` will download
the latest image from @your_username and store it in the given output directory.

There are also a handful of optional arguments. `python switch_dl.py -h` will
tell you everything you need, but here are the available arguments:

- `--latest` / `-l` : Saves a copy of the most recent tweet's image to the top
  level of the output directory, named `latest.jpg`.
- `--number` / `-n` : Specify a number to download that many images. If there
  are tweets with no images, or that do not match the required hastag (see `-t`),
  that tweet will not count towards the number.
- `--no_subfolders` / `-s` : By default, any hashtags in the tweet will be used
  as a subfolder path to save each image to. For example, a tweet with
  "#BreathoftheWild #BossFight #Ganon" will have its image saved to the path
  `output_dir/breathofthewild/bossfight/ganon/2017-03-03 at 12-00-00.jpg`. Pass
  `-s` to disable this behaviour.
- `--require_tag` / `-t` : Specify a hashtag that must be present in a tweet for
  that tweet's image to be downloaded. Tweets not containing that hashtag are not
  downloaded and do not count towards the image count specified by `-n`.


[api_keys]: https://python-twitter.readthedocs.io/en/latest/getting_started.html
[download]: https://github.com/jobbogamer/SwitchScreenshotDownloader/archive/master.zip
