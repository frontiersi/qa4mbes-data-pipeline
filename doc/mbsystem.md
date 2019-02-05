# Installing MB-system

Platform: Ubuntu Linux 18.10

Ensure dependencies:

`sudo apt update && sudo apt upgrade`

`sudo apt install libgmt libgmt-dev fftw-dev libnetcdf-dev`

Clone the source repository:

`git clone git@github.com:dwcaress/MB-System.git`

Create a separate build directory, using the source directory will mess with future `git pull` efforts. `.gitignore` should exclude all build products but doesn't.

`mkdir mbsystem-build && cd mbsystem-build`

Run `configure`:

`../MB-System/configure`

Build and install:

`make && sudo make install`

Investigate and possibly update prebuilt docker packages: https://github.com/ofrei/mbsystem-docker
