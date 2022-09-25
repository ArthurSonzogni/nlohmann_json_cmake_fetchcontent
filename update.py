#!/usr/bin/env python3

import sys, os
import json
import subprocess
import urllib.request
import hashlib

# Go to the directory this script is stored in
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Download release data
releases = json.loads(str(urllib.request.urlopen('https://api.github.com/repos/nlohmann/json/releases').read(), 'utf-8'))

# Fetch all releases and the corresponding URL
release_url_map = []
for release in releases:
  for asset in release['assets']:
    if asset['name'] == 'json.hpp':
      release_url_map.append((release['tag_name'], asset['browser_download_url'], release['body']))

# List all git tags
process = subprocess.Popen(['git', 'tag'], stdout=subprocess.PIPE)
tags, _ = process.communicate()
tags = set(filter(None, str(tags, 'utf-8').split("\n")))
print("Releases already contained in this repository are " + str(tags))

# Go over the release_url_map in reverse order; if a release is not yet a Git
# tag, download the file, commit and add a tag
for tag, url, body in release_url_map[::-1]:
  if tag in tags:
    continue

  print("Downloading release " + tag)
  if tag >= "v3.10.5":
      os.system("rm -rf ./tmp")
      os.system("rm -rf ./include")
      os.system("git clone https://github.com/nlohmann/json ./tmp --depth 1 --branch {}".format(tag));
      os.system("cp -rf ./tmp/single_include .")
      os.system("cp -rf ./tmp/include/nlohmann/json_fwd.hpp ./single_include/nlohmann/")
      os.system("cp -rf ./tmp/cmake .")
      os.system("cp -rf ./tmp/CMakeLists.txt .")
      os.system("cp -rf ./tmp/meson.build .")
      os.system("cp -rf ./tmp/LICENSE.MIT .")
      os.system("rm -rf ./tmp")
      os.makedirs('./cmake', mode=0o777, exist_ok=True)
      os.makedirs('./test', mode=0o777, exist_ok=True)
      with open("./cmake/ci.cmake", "w") as f:
        f .write("message(FATAL_ERROR \"The JSON_CI option is not available" \
                 "when using the nlohmann_json_cmake_fetchcontent repository.\")")
      with open("./test/CMakeLists.txt", "w") as f:
        f.write("message(FATAL_ERROR \"The JSON_CI option is not available" \
                "when using the nlohmann_json_cmake_fetchcontent repository.\")")
      os.system("git add .")
  else:
      os.makedirs('./include', mode=0o777, exist_ok=True)
      os.makedirs('./include/nlohmann', mode=0o777, exist_ok=True)
      data = urllib.request.urlopen(url).read();
      with open('./include/nlohmann/json.hpp', 'wb') as f:
        f.write(data)

      # Try to download the json_fwd.hpp header -- only exists since release
      # v3.1.0
      has_json_fwd = False
      try:
        json_fwd_url = 'https://github.com/nlohmann/json/raw/{}/include/nlohmann/json_fwd.hpp'.format(tag);
        print("Trying to download " + json_fwd_url)
        data = urllib.request.urlopen(json_fwd_url).read();
        with open('./include/nlohmann/json_fwd.hpp', 'wb') as f:
          f.write(data)
        has_json_fwd = True
      except:
        pass

      subprocess.call(['git', 'add', './include/nlohmann/json.hpp'])
      if has_json_fwd:
        subprocess.call(['git', 'add', './include/nlohmann/json_fwd.hpp'])
  # Update the nlohman json options.
  subprocess.call([ 'sed', '-i', '-e', 's/library.\" ON/library.\" OFF/g', './CMakeLists.txt'])
  subprocess.call(['git', 'add', './CMakeLists.txt'])

  # Update the README.md:
  subprocess.call([ 'sed', '-i', '-e', 's/GIT_TAG .*)/GIT_TAG '+ tag + ')/g', './README.md'])
  subprocess.call(['git', 'add', './README.md'])

  # Commit:
  subprocess.call(['git', 'commit', '-m', 'Upstream release ' + tag])
  subprocess.call(['git', 'tag', '-a', tag, '-m', body])
